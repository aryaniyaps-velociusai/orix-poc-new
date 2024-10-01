import logging
from openai import OpenAI, AzureOpenAI, AsyncAzureOpenAI, AsyncOpenAI
from dotenv import load_dotenv
import os
import json

from utils.decorators import log_execution_time, log_execution_time_async

load_dotenv()

GPT_4_TURBO = "gpt-4-turbo"
GPT_4_OMNI = "gpt-4o"

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION= os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')

logger = logging.getLogger('orix-poc-logger')


async def extract_data_openai(user_prompt):
    # print('\nOpenAI data extraction started... \n')
    OPENAI_CLIENT = AsyncOpenAI()

    response = await OPENAI_CLIENT.chat.completions.create(
        model=GPT_4_OMNI,
        response_format={"type": "json_object"},
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a highly accurate accounting assistant skilled at processing Balance Sheet and/or Income Statement information from provided text data."},
            {"role": "user", "content": user_prompt},
            # {"role": "user", "content":"If you are unable to map fields to a CoA, return list of such unmapped fields, give reasons for doing so, guidelines taken into consideration, additional instructions/guidelines required in additional json fields in the json output"}
        ]
    )

    openai_response = response.choices[0].message.content

    print(openai_response)

    usage = response.usage
    print(f'''\nprompt_tokens: {usage.prompt_tokens}, completion_tokens: {
        usage.completion_tokens}, total_tokens: {usage.total_tokens}\n''')
    return openai_response, usage

@log_execution_time_async
async def extract_data_azure_openai(user_prompt,extracted_text,user_feedback):
    client = AsyncAzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        max_retries=2,
    )

    response = await client.chat.completions.create(
        model=GPT_4_OMNI,
        response_format={"type": "json_object"},
        temperature=0.2,
        messages=[
            {"role": "system", "content": user_prompt},
            {"role": "user", "content": f'''## extracted Balance Sheet Text: 
                            ```{extracted_text}``` 
                        Additionally, please consider the following user feedback while extracting the data:
                            {user_feedback}'''  },
            # {"role": "user", "content":"If you are unable to map fields to a CoA, return list of such unmapped fields, give reasons for doing so, guidelines taken into consideration, additional instructions/guidelines required in additional json fields in the json output"}
        ]
    )

    openai_response = response.choices[0].message.content
    usage = response.usage
    print(f'''\nprompt_tokens: {usage.prompt_tokens}, completion_tokens: {
        usage.completion_tokens}, total_tokens: {usage.total_tokens}\n''')
    # logger.info(f'''\n\n{"%"*60}\n\nprompt_tokens: {usage.prompt_tokens}, completion_tokens: {
    #     usage.completion_tokens}, total_tokens: {usage.total_tokens}\n''')
    return openai_response, usage


@log_execution_time_async
async def generate_updated_prompt(original_prompt, user_modifications):
    try:
        client = AsyncAzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_OPENAI_DEPLOYMENT,
            max_retries=2,
        )
        # Simulate API interaction with the LLM
        response = await client.chat.completions.create(
            model=GPT_4_OMNI,  # Replace with the correct model name if necessary
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": '''You are an assistant that helps with prompt modification and generation.
                    Your task is to modify an original prompt with user-provided input while keeping the same structure and type.
                    The changes should focus on updating specific data points requested by the user.
                    The final result should be provided in JSON format, where the modified prompt is included.'''
                },
                {
                    "role": "user",
                    "content": f'''Original Prompt:
                    {json.dumps(original_prompt)}

                    User Feedback:
                    {json.dumps(user_modifications)}

                    Please modify the original prompt by updating the specific data points according to the user feedback.
                    Return the result in the following JSON format:
                    {{
                        "updated_prompt": "Updated Prompt Here"
                    }}
                    '''
                }
            ]
        )

        # Extract the response from the LLM
        print("response", response)
        data_string = response.choices[0].message.content

        # Attempt to load the JSON response from the LLM output
        try:
            extracted_json = json.loads(data_string) if data_string else {}
            print("extracted_json", extracted_json)
            return extracted_json.get('updated_prompt', 'N/A')
        except json.JSONDecodeError as e:
            # Handle the case where the returned data is not valid JSON
            print(f"JSON decoding error: {e}, raw response: {data_string}")
            return data_string  # Return the raw string if JSON parsing fails

    except Exception as e:
        print(f"Error while generating updated prompt: {e}")
        return None