import asyncio
from azure.cosmos import CosmosClient, exceptions
from azure.core.pipeline.transport import RequestsTransport
import certifi

from services.openai_request import generate_updated_prompt

from config import DefaultConfig
CONFIG = DefaultConfig()

DATABASE_URI = CONFIG.DATABASE_URI
DATABASE_KEY = CONFIG.KEY
DATABASE_ID = CONFIG.DATABASE_ID
CONTAINER_ID_PROMPT = CONFIG.CONTAINER_ID_PROMPT
ENV = CONFIG.ENVIRONMENT

def simplify_json(data):
    for key in list(data.keys()):
        if isinstance(data[key], dict):
            simplify_json(data[key])
        elif key == "fields":
            del data[key]
    return data

def filter_non_empty_feedback(data):
    # Helper function to filter based on non-empty feedback
    def filter_fields(fields):
        return {k: v for k, v in fields.items() if v.get("user_feedback")}
    
    if "balance_sheet" in data:
        for section, fields in data["balance_sheet"].items():
            data["balance_sheet"][section] = filter_fields(fields)
    
    if "income_statement" in data:
        for section, fields in data["income_statement"].items():
            data["income_statement"][section] = filter_fields(fields)
    
    return data

async def process_balance_sheet(container, data, balance_sheet_user_prompt):
    try:
        """
        This function handles reading and updating or creating the balance sheet item.
        Returns the updated prompt for the balance sheet.
        """
        balance_sheet_id = "balance_sheet"
        # Try to read the balance sheet item
        balance_sheet_item = container.read_item(balance_sheet_id, partition_key=ENV)

        # Update the balance_sheet field with the new data
        data = filter_non_empty_feedback(data)
        balance_sheet_item["user_feedback"] = data.get("balance_sheet", {})
        prompt = balance_sheet_user_prompt

        # Update the prompt asynchronously
        updated_prompt = await generate_updated_prompt(prompt, balance_sheet_item["user_feedback"])
        balance_sheet_item['updated_prompt'] = updated_prompt
        balance_sheet_item['prompt'] = balance_sheet_user_prompt
        print("Balance Sheet updated_prompt:", updated_prompt)
        # Upsert the (new or updated) balance sheet item
        container.upsert_item(balance_sheet_item)

        # Return the updated or initial prompt
        return updated_prompt
    except Exception as e:
        print(f"Error occured in : {process_balance_sheet} ", e)
        raise e

async def process_income_statement(container, data, income_statement_user_prompt):
    try:
        """
        This function handles reading and updating or creating the income statement item.
        Returns the updated prompt for the income statement.
        """
        income_statement_id = "income_statement"
        # Try to read the income statement item
        income_statement_item = container.read_item(income_statement_id, partition_key=ENV)

        # Update the income_statement field with the new data
        data = filter_non_empty_feedback(data)
        income_statement_item["user_feedback"] = data.get("income_statement", {})
        prompt = income_statement_user_prompt

        # Update the prompt asynchronously
        updated_prompt = await generate_updated_prompt(prompt, income_statement_item["user_feedback"])
        income_statement_item['updated_prompt'] = updated_prompt
        income_statement_item['prompt'] = prompt
        print("Income Statement updated_prompt:", updated_prompt)
        # Upsert the (new or updated) income statement item
        container.upsert_item(income_statement_item)

        # Return the updated or initial prompt
        return updated_prompt
    except Exception as e:
        print(f"Error occured in : {process_income_statement} ", e)
        raise e

async def get_financial_items():
    """
    This function checks if balance_sheet and/or income_statement are present, 
    and creates or updates the respective items in Cosmos DB.
    Returns the updated prompts for both balance_sheet and income_statement.
    """
    try:

        
        # Create a custom transport with SSL settings using certifi
        transport = RequestsTransport(connection_verify=certifi.where())

        # Initialize the CosmosClient with the custom transport
        client = CosmosClient(DATABASE_URI, credential=DATABASE_KEY, transport=transport)
        database = client.get_database_client(DATABASE_ID)
        container = database.get_container_client(CONTAINER_ID_PROMPT)

        income_statement_id = "income_statement"
        # Try to read the income statement item
        income_statement_item = container.read_item(income_statement_id, partition_key=ENV)

        updated_income_statement_prompt = income_statement_item.get("updated_prompt", "")
        income_statement_user_feedback = income_statement_item.get("user_feedback", {})


        balance_sheet_id = "balance_sheet"
        # Try to read the income statement item
        balance_sheet_item = container.read_item(balance_sheet_id, partition_key=ENV)

        updated_balance_sheet_prompt = balance_sheet_item.get("updated_prompt", "")
        balance_sheet_user_feedback = balance_sheet_item.get("user_feedback", {})

        return {
            "updated_income_statement_prompt": updated_income_statement_prompt,
            "income_statement_user_feedback": income_statement_user_feedback,
            "updated_balance_sheet_prompt": updated_balance_sheet_prompt,
            "balance_sheet_user_feedback": balance_sheet_user_feedback,
        }


    except Exception as e:
        print(f"Exception in {get_financial_items.__name__}: {e}")
        raise e


async def upsert_financial_items(data, balance_sheet_user_prompt, income_statement_user_prompt):
    """
    This function checks if balance_sheet and/or income_statement are present, 
    and creates or updates the respective items in Cosmos DB.
    Returns the updated prompts for both balance_sheet and income_statement.
    """
    try:
        simplified_data = simplify_json(data)
        # Create a custom transport with SSL settings using certifi
        transport = RequestsTransport(connection_verify=certifi.where())

        # Initialize the CosmosClient with the custom transport
        client = CosmosClient(DATABASE_URI, credential=DATABASE_KEY, transport=transport)
        database = client.get_database_client(DATABASE_ID)
        container = database.get_container_client(CONTAINER_ID_PROMPT)

        # Prepare the tasks for concurrent execution
        tasks = []
        task_info = []  # List to keep track of which task is for which prompt

        # If balance_sheet is present, process it and track the task
        if data.get("is_balance_sheet_present") == "Yes":
            tasks.append(process_balance_sheet(container, simplified_data, balance_sheet_user_prompt))
            task_info.append("balance_sheet")

        # If income_statement is present, process it and track the task
        if data.get("is_income_statement_present") == "Yes":
            tasks.append(process_income_statement(container, simplified_data, income_statement_user_prompt))
            task_info.append("income_statement")

        # Run both tasks concurrently and capture the updated prompts
        balance_sheet_prompt = None
        income_statement_prompt = None

        if tasks:
            results = await asyncio.gather(*tasks)
            # Iterate over the task info to map results correctly
            for i, task_type in enumerate(task_info):
                if task_type == "balance_sheet":
                    balance_sheet_prompt = results[i]
                elif task_type == "income_statement":
                    income_statement_prompt = results[i]

        return {
            "balance_sheet_prompt": balance_sheet_prompt,
            "income_statement_prompt": income_statement_prompt
        }

    except Exception as e:
        print(f"Exception in upsert_financial_items: {e}")
        raise e