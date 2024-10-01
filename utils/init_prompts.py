from azure.cosmos import CosmosClient, exceptions
from azure.core.pipeline.transport import RequestsTransport
import certifi

from utils.prompt import balance_sheet_prompt,income_statement_prompt
from services.openai_request import generate_updated_prompt
from config import DefaultConfig

CONFIG = DefaultConfig()

CURRENT_PROMPT_VERSION = "v1.01"

NEW_BALANCE_SHEET_PROMPT = balance_sheet_prompt
NEW_INCOME_STATEMENT_PROMPT = income_statement_prompt


# Initialize Cosmos DB parameters (to be imported from config or environment variables)
DATABASE_URI = CONFIG.DATABASE_URI
DATABASE_KEY = CONFIG.KEY
DATABASE_ID = CONFIG.DATABASE_ID
CONTAINER_ID_PROMPT = CONFIG.CONTAINER_ID_PROMPT
ENV = CONFIG.ENVIRONMENT


async def initialize_prompts():
    """
    This function runs once at startup to ensure the prompt in the database
    is updated with the current version from the code.
    """
    try:
        # Create a custom transport with SSL settings using certifi
        transport = RequestsTransport(connection_verify=certifi.where())

        # Initialize the CosmosClient with the custom transport
        client = CosmosClient(DATABASE_URI, credential=DATABASE_KEY, transport=transport)
        database = client.get_database_client(DATABASE_ID)
        container = database.get_container_client(CONTAINER_ID_PROMPT)

        # Check and update the balance sheet prompt
        await check_and_update_prompt(
            container, "balance_sheet", NEW_BALANCE_SHEET_PROMPT, CURRENT_PROMPT_VERSION, "balance_sheet"
        )

        # Check and update the income statement prompt
        await check_and_update_prompt(
            container, "income_statement", NEW_INCOME_STATEMENT_PROMPT, CURRENT_PROMPT_VERSION, "income_statement"
        )

    except Exception as e:
        print(f"Exception in initialize_prompts: {e}")


async def check_and_update_prompt(container, item_id, new_prompt, current_version, job_id):
    """
    This function checks if the prompt in the database matches the current version.
    If not, it updates the database with the new prompt and version.
    """
    try:
        # Try to read the item from the database
        item = container.read_item(item_id, partition_key=ENV)

        # Check if the current version matches the one in the database
        if item.get("prompt_version") != current_version:
            # If not, update the prompt and the version
            item["prompt"] = new_prompt
            item["prompt_version"] = current_version
            user_feedback = item['user_feedback']
            updated_prompt = await generate_updated_prompt(new_prompt,user_feedback)
            item['updated_prompt'] = updated_prompt
            # Upsert the updated item to the database
            container.upsert_item(item)
            print(f"Updated {job_id} prompt to version {current_version}.")

    except exceptions.CosmosResourceNotFoundError:
        # If the item does not exist, create it with the new prompt and version
        item = {
            "id": item_id,
            "environment": ENV,
            "user_feedback": None,
            "job_id": job_id,
            "prompt": new_prompt,
            "updated_prompt":new_prompt,
            "prompt_version": current_version
        }
        container.upsert_item(item)
        print(f"Created new {job_id} prompt with version {current_version}.")
    except Exception as e:
        print(f"Exception while updating {job_id} prompt: {e}")

