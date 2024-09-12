import logging
from openai import OpenAI, AzureOpenAI, AsyncAzureOpenAI, AsyncOpenAI
from dotenv import load_dotenv
import os

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
            {"role": "system", "content": "You are a highly accurate assistant skilled at processing Balance Sheet and/or Income Statement information from provided text data."},
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
async def extract_data_azure_openai(user_prompt):
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
            {"role": "system", "content": "You are a highly accurate assistant skilled at processing Balance Sheet and/or Income Statement information from provided text data."},
            {"role": "user", "content": user_prompt},
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
