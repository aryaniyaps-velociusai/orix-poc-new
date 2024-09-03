from azure.cosmos.aio import CosmosClient
import azure.cosmos.exceptions as exceptions
from azure.identity import DefaultAzureCredential

from config import DefaultConfig

CONFIG = DefaultConfig()


def get_jobs_obj(data):
    data["environment"] = CONFIG.PARTITION_ENV
    return data
    # return {
    #     "id": data["job_id"],
    #     "job_date": data["job_date"],
    #     "loantransfer_name": data["loantransfer_name"],
    #     "user": data["user"],
    #     "loantransfer_staging_info": data["loantransfer_staging_info"],
    #     "report_location_info": data["report_location_info"],
    #     "status": data["status"],
    #     "environment": CONFIG.ENV,
    # }


# 'CosmosClient' object does not support the context manager protocol


async def create_record(data):
    try:
        # if CONFIG.ENVIRONMENT == "local":
        client = CosmosClient(CONFIG.DATABASE_URI, credential=CONFIG.KEY)
        # else:
        #     credential = DefaultAzureCredential()
        #     client = CosmosClient(CONFIG.DATABASE_URI, credential=credential)

        print('client ok')

        database = client.get_database_client(CONFIG.DATABASE_ID)

        print(database)
        container = database.get_container_client(CONFIG.CONTAINER_ID)
        print(container.database_link)
        print(container.container_link)
        item = get_jobs_obj(data)

        

        res = await container.create_item(item)
        await client.close()
        return res["id"]
    except Exception as e:
        print("Exception while creating a record", e)
    return None


async def get_records_with_status(status):
    records = []
    try:
        # if CONFIG.ENVIRONMENT == "local":
        client = CosmosClient(CONFIG.DATABASE_URI, credential=CONFIG.KEY)
        # else:
        #     credential = DefaultAzureCredential()
        #     client = CosmosClient(CONFIG.DATABASE_URI, credential=credential)

        database = client.get_database_client(CONFIG.DATABASE_ID)
        container = database.get_container_client(CONFIG.CONTAINER_ID)

        query = f"SELECT * FROM {CONFIG.CONTAINER_ID} dj WHERE dj.status='{status}' and dj.environment='{CONFIG.PARTITION_ENV}'"

        results = container.query_items(query=query)

        async for item in results:
            records.append(item)

    except Exception as e:
        print("Exception while creating a record", e)
    finally:
        await client.close()
    return records


async def get_item_by_id(job_id):
    try:
        # if CONFIG.ENVIRONMENT == "local":
        client = CosmosClient(CONFIG.DATABASE_URI, credential=CONFIG.KEY)
        # else:
        #     credential = DefaultAzureCredential()
        #     client = CosmosClient(CONFIG.DATABASE_URI, credential=credential)

        database = client.get_database_client(CONFIG.DATABASE_ID)
        container = database.get_container_client(CONFIG.CONTAINER_ID)

        try:
            item = await container.read_item(job_id, partition_key=CONFIG.PARTITION_ENV)
            return item
        except exceptions.CosmosResourceNotFoundError as e:
            print(e.reason)
            return -1
        finally:
            await client.close()
    except Exception as e:
        print("Exception while getting a record", e)
    return None


async def update_item(item):
    try:
        # if CONFIG.ENVIRONMENT == "local":
        client = CosmosClient(CONFIG.DATABASE_URI, credential=CONFIG.KEY)
        # else:
        #     credential = DefaultAzureCredential()
        #     client = CosmosClient(CONFIG.DATABASE_URI, credential=credential)

        database = client.get_database_client(CONFIG.DATABASE_ID)
        container = database.get_container_client(CONFIG.CONTAINER_ID)

        try:
            # response = await container.upsert_item(item)
            response = await container.replace_item(item=item, body=item)
            return response

        except Exception as e:
            print("Error while updating the item", item)
            print(e)
            raise
            return -1
        finally:
            await client.close()

    except Exception as e:
        print("Exception in update_item", e)
    return None