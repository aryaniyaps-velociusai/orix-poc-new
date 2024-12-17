import aiosqlite  # Import the async SQLite library
from config import DefaultConfig

CONFIG = DefaultConfig()


def get_jobs_obj(data):
    data["environment"] = CONFIG.PARTITION_ENV
    return data


async def create_record(data):
    try:
        async with aiosqlite.connect(CONFIG.DATABASE_URI) as conn:
            async with conn.cursor() as cursor:
                item = get_jobs_obj(data)

                # Insert the record into the database
                await cursor.execute(
                    """
                    INSERT INTO jobs (job_id, job_date, loantransfer_name, user, loantransfer_staging_info, report_location_info, status, environment)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item["job_id"],
                        item["job_date"],
                        item["loantransfer_name"],
                        item["user"],
                        item["loantransfer_staging_info"],
                        item["report_location_info"],
                        item["status"],
                        item["environment"],
                    ),
                )

                await conn.commit()
                job_id = cursor.lastrowid  # Get the last inserted row ID
                return job_id
    except Exception as e:
        print("Exception while creating a record:", e)
    return None


async def get_records_with_status(status):
    records = []
    try:
        async with aiosqlite.connect(CONFIG.DATABASE_URI) as conn:
            async with conn.cursor() as cursor:
                query = """
                SELECT * FROM jobs WHERE status = ? AND environment = ?
                """
                await cursor.execute(query, (status, CONFIG.PARTITION_ENV))
                records = await cursor.fetchall()  # Asynchronously fetch all records

    except Exception as e:
        print("Exception while fetching records:", e)

    return records


async def get_item_by_id(job_id):
    try:
        async with aiosqlite.connect(CONFIG.DATABASE_URI) as conn:
            async with conn.cursor() as cursor:
                query = """
                SELECT * FROM jobs WHERE job_id = ? AND environment = ?
                """
                await cursor.execute(query, (job_id, CONFIG.PARTITION_ENV))
                item = await cursor.fetchone()  # Asynchronously fetch a single record

                if item:
                    # Assuming the table has columns matching the dict format
                    return dict(zip([column[0] for column in cursor.description], item))
                else:
                    return -1
    except Exception as e:
        print("Exception while getting a record:", e)
    return None


async def update_item(item):
    try:
        async with aiosqlite.connect(CONFIG.DATABASE_URI) as conn:
            async with conn.cursor() as cursor:
                query = """
                UPDATE jobs
                SET job_date = ?, loantransfer_name = ?, user = ?, loantransfer_staging_info = ?, 
                    report_location_info = ?, status = ?, environment = ?
                WHERE job_id = ? AND environment = ?
                """
                await cursor.execute(
                    query,
                    (
                        item["job_date"],
                        item["loantransfer_name"],
                        item["user"],
                        item["loantransfer_staging_info"],
                        item["report_location_info"],
                        item["status"],
                        item["environment"],
                        item["job_id"],
                        item["environment"],
                    ),
                )

                await conn.commit()
                return item
    except Exception as e:
        print("Exception in update_item:", e)
    return None
