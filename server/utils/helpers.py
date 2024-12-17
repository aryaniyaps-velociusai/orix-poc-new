import logging
import os
import re
import shutil
import uuid
from datetime import datetime

import aiohttp
import boto3
import fitz
import pandas as pd
import xlsxwriter
from azure.identity import DefaultAzureCredential
from constants import Method
from PIL import Image

logger = logging.getLogger("orix-poc-logger")

METHOD = Method()


async def api_call(method, url, headers, data=None):
    response = None
    status_code = None
    msg = "Error encounterred during json fetch"
    async with aiohttp.ClientSession() as session:
        if method == METHOD.GET:
            async with session.get(url, headers=headers) as resp:
                status_code = resp.status
                reason = resp.reason
                try:
                    response = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError as e:
                    logger.info(f"{msg}, {reason}, {e}")
                if status_code not in [200, 201, 202, 203]:
                    logger.info(f"{await resp.text()}")
        if method == METHOD.DELETE:
            async with session.delete(url, headers=headers) as resp:
                status_code = resp.status
                reason = resp.reason
                if status_code != 204:
                    logger.info(f"{await resp.text()}")
        elif method == METHOD.POST:
            async with session.post(url, headers=headers, json=data) as resp:
                status_code = resp.status
                reason = resp.reason
                try:
                    response = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError as e:
                    logger.info(f"{msg}, {reason}, {e}")
                if status_code not in [200, 201]:
                    logger.info(f"{await resp.text()}")
        elif method == METHOD.PUT:
            async with session.put(url, headers=headers, data=data) as resp:
                status_code = resp.status
                reason = resp.reason
                try:
                    response = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError as e:
                    logger.info(f"{msg}, {reason}, {e}")
                if status_code not in [200, 201]:
                    logger.info(f"{await resp.text()}")

    return status_code, reason, response


def get_token():
    default_cred = DefaultAzureCredential()
    scope = "https://graph.microsoft.com/.default"
    return default_cred.get_token(scope).token


def extract_link_from_html(html_content: str) -> str:
    pattern = r'href="([^"]+)"'
    matches = re.search(pattern, html_content)
    if matches:
        return matches.group(1)
    return ""


def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.info(f"Failed to delete {file_path}. Reason: {e}")


def tif_to_pdf(input_path):
    output_path = os.path.splitext(input_path)[0] + ".pdf"
    with Image.open(input_path) as img:
        pdf_pages = []
        for i in range(img.n_frames):
            img.seek(i)
            if img.mode != "RGB":
                pdf_pages.append(img.convert("RGB"))
            else:
                pdf_pages.append(img.copy())

        pdf_pages[0].save(output_path, save_all=True, append_images=pdf_pages[1:])

    return output_path


def pdf_to_single_pages(pdf_path, output_folder):
    single_page_pdf_folder = os.path.join(output_folder, "single_page_pdf")
    if not os.path.exists(single_page_pdf_folder):
        os.makedirs(single_page_pdf_folder)
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    for page_num in range(total_pages):
        output_file = os.path.join(single_page_pdf_folder, f"{page_num + 1}.pdf")
        single_page_doc = fitz.open()  # create a new empty PDF
        single_page_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        single_page_doc.save(output_file)
        single_page_doc.close()

    doc.close()


def get_number_of_pages(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    doc.close()
    return num_pages


def upload_to_s3(pdf_path, bucket):
    s3_client = boto3.client("s3")
    object_name = os.path.basename(pdf_path)
    s3_client.upload_file(pdf_path, bucket, object_name)
    return object_name


def convert_to_markdown_table(df):
    """Convert a DataFrame to a markdown table format."""
    df = df.fillna("Null")
    return df.to_markdown(index=False)


def create_separator(text):
    """Create a separator line based on the longest line in the text."""
    max_length = max(len(line) for line in text.split("\n"))
    return "-" * max_length


def parse_data_string(data_str):
    try:
        # Regular expression to match each list inside the main list
        list_pattern = re.compile(r"\[([^\[\]]*)\]")
        # Find all matches
        matches = list_pattern.findall(data_str)
        # Split each match by commas and strip extra whitespace and quotes
        parsed_data = [
            re.split(r',(?![^"]*"(?:[^"]*"[^"]*")*[^"]*$)', match) for match in matches
        ]
        parsed_data = [
            [item.strip().strip("'").strip() for item in row] for row in parsed_data
        ]
        return parsed_data
    except Exception as e:
        logger.info(f"Error parsing the data: {e}")
        return []


def generate_job_id():
    uuid_without_dashes = str(uuid.uuid4()).replace("-", "")
    ans = uuid_without_dashes.upper()
    return ans


def iso_date_conversion(iso_date_string):
    iso_date = datetime.fromisoformat(iso_date_string)
    return iso_date.strftime("%m/%d/%Y")
