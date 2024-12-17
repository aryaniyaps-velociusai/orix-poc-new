import logging

from config import settings
from dotenv import load_dotenv
from instrumentation import log_execution_time_async
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_azure_ai import AzureAIChatCompletionsModel
from langchain_openai import ChatAzureOpenAI, ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Model Constants
GPT_4_TURBO = "gpt-4-turbo"
GPT_4_OMNI = "gpt-4o"


# Logging Setup
logger = logging.getLogger("orix-poc-logger")


# Function to get the current LLM client based on the configured provider
def get_llm_client(provider="azure"):
    if provider == "openai":
        # Default OpenAI LLM client
        return ChatOpenAI(model=GPT_4_OMNI, temperature=0.2)
    elif provider == "azure":
        # Azure OpenAI LLM client
        return ChatAzureOpenAI(
            openai_api_key=settings.AZURE_OPENAI_API_KEY,
            openai_api_base=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_version=settings.AZURE_OPENAI_API_VERSION,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT,
            model=GPT_4_OMNI,
            temperature=0.2,
        )
    elif provider == "phi4":
        return AzureAIChatCompletionsModel(
            endpoint=settings.AZURE_INFERENCE_ENDPOINT,
            credential=settings.AZURE_INFERENCE_CREDENTIAL,
            model_name="phi-4",
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Function for handling extraction from OpenAI
async def extract_data_llm(user_prompt, provider="openai"):
    llm_client = get_llm_client(provider)

    prompt_template = PromptTemplate(
        input_variables=["user_prompt"],
        template="You are a highly accurate accounting assistant skilled at processing Balance Sheet and/or Income Statement information from provided text data. {user_prompt}",
    )

    llm_chain = LLMChain(llm=llm_client, prompt=prompt_template)

    response = await llm_chain.apredict(user_prompt=user_prompt)

    print(response)
    return response


# Async function for handling extraction from Azure OpenAI
@log_execution_time_async
async def extract_data_azure_openai(user_prompt, extracted_text, user_feedback):
    llm_client = get_llm_client(provider="azure")

    prompt_template = PromptTemplate(
        input_variables=["user_prompt", "extracted_text", "user_feedback"],
        template="""\
        You are a highly accurate accounting assistant skilled at processing Balance Sheet and/or Income Statement information from provided text data.
        {user_prompt}
        ## extracted Balance Sheet Text: 
        ```{extracted_text}```
        Additionally, please consider the following user feedback while extracting the data:
        {user_feedback}
        """,
    )

    llm_chain = LLMChain(llm=llm_client, prompt=prompt_template)

    response = await llm_chain.apredict(
        user_prompt=user_prompt,
        extracted_text=extracted_text,
        user_feedback=user_feedback,
    )

    print(response)
    return response


# Test run of the extraction function
async def main():
    user_prompt = (
        "Extract the relevant financial information from the following balance sheet."
    )
    extracted_text = "Assets: $1M, Liabilities: $500K, Equity: $500K"
    user_feedback = "Make sure to account for all liabilities."

    # Example using OpenAI (GPT-4)
    await extract_data_llm(user_prompt, provider="openai")

    # Example using Azure OpenAI (GPT-4)
    await extract_data_azure_openai(user_prompt, extracted_text, user_feedback)


# If running as the main script
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
