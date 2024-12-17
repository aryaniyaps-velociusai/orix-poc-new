import asyncio
import sqlite3

from config import DefaultConfig

CONFIG = DefaultConfig()


def get_jobs_obj(data):
    data["environment"] = CONFIG.PARTITION_ENV
    return data


async def create_record(data):
    try:
        conn = sqlite3.connect(
            CONFIG.DATABASE_URI
        )  # SQLite connection (assuming the database is a file)
        cursor = conn.cursor()

        item = get_jobs_obj(data)
        # Assuming there's a table named 'jobs' in SQLite with the relevant columns
        cursor.execute(
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

        conn.commit()
        job_id = cursor.lastrowid  # SQLite provides the last inserted row ID
        conn.close()
        return job_id
    except Exception as e:
        print("Exception while creating a record", e)
    return None


async def get_records_with_status(status):
    records = []
    try:
        conn = sqlite3.connect(CONFIG.DATABASE_URI)
        cursor = conn.cursor()

        query = """
            SELECT * FROM jobs WHERE status = ? AND environment = ?
        """
        cursor.execute(query, (status, CONFIG.PARTITION_ENV))
        records = cursor.fetchall()

        conn.close()
    except Exception as e:
        print("Exception while fetching records", e)

    return records


async def get_item_by_id(job_id):
    try:
        conn = sqlite3.connect(CONFIG.DATABASE_URI)
        cursor = conn.cursor()

        query = """
            SELECT * FROM jobs WHERE job_id = ? AND environment = ?
        """
        cursor.execute(query, (job_id, CONFIG.PARTITION_ENV))
        item = cursor.fetchone()  # This will return the first matched row or None

        conn.close()

        if item:
            # Assuming the table has columns matching the dict format
            return dict(zip([column[0] for column in cursor.description], item))
        else:
            return -1
    except Exception as e:
        print("Exception while getting a record", e)
    return None


async def update_item(item):
    try:
        conn = sqlite3.connect(CONFIG.DATABASE_URI)
        cursor = conn.cursor()

        # Assuming 'job_id' is the unique identifier for the job
        query = """
            UPDATE jobs
            SET job_date = ?, loantransfer_name = ?, user = ?, loantransfer_staging_info = ?, 
                report_location_info = ?, status = ?, environment = ?
            WHERE job_id = ? AND environment = ?
        """
        cursor.execute(
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

        conn.commit()
        conn.close()
        return item
    except Exception as e:
        print("Exception in update_item", e)
    return None
