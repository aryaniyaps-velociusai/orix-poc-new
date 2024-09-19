import json
import logging
import random
import sys
import threading
import time
import pandas as pd
import pickle
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
from PIL import Image
import subprocess
from textractor import Textractor
from textractor.data.constants import TextractFeatures
import asyncio
import shutil
import os
import math
import re
import platform
from dotenv import load_dotenv
from .openai_request import extract_data_azure_openai, extract_data_openai
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

AZURE_DI_ENDPOINT_1 = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT_1')
AZURE_DI_KEY_1 = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY_1')
AZURE_DI_ENDPOINT_2 = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT_2')
AZURE_DI_KEY_2 = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY_2')

MAX_RETRY_COUNT = 2
RETRY_DELAY = 5
GS_PATH = 'gs'

logger = logging.getLogger('orix-poc-logger')

if platform.system() == 'Windows':
    GS_PATH = r"C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe"

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


def tif_to_jpeg(input_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    Image.MAX_IMAGE_PIXELS = None
    with Image.open(input_path) as img:
        for i in range(img.n_frames):
            img.seek(i)
            if img.mode != "RGB":
                frame = img.convert("RGB")
            else:
                frame = img.copy()
            output_path = os.path.join(
                output_folder, f"output_page-{i + 1}.jpeg")
            frame.save(output_path, "JPEG", dpi=(300, 300))


def convert_to_jpeg(input_path, output_folder, file_index=1):
    Image.MAX_IMAGE_PIXELS = None

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with Image.open(input_path) as img:

        if img.mode != "RGB":
            img = img.convert("RGB")
        output_path = os.path.join(
            output_folder, f"output_page-{file_index}.jpeg")

        img.save(output_path, "JPEG", dpi=(300, 300))


def process_image(input_path, output_folder, max_size_mb=4, quality=95):
    # Processed image prefix for saving
    processed_image_prefix = os.path.join(
        output_folder, "processed_images", "processed_page"
    )

    Image.MAX_IMAGE_PIXELS = None
    # Open and process the image
    img = Image.open(input_path)
    img = img.convert("L")
    img = img.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # Output path construction
    output_path = (
            processed_image_prefix + "-" +
            os.path.basename(input_path).split("-")[-1]
    )

    # Initially save the image with the specified quality
    img.save(output_path, quality=quality)

    img = Image.open(output_path)

    # Adjust the image size
    width, height = img.size

    # Check if the saved image exceeds the maximum size limit
    if os.path.getsize(output_path) > max_size_mb * 1024 * 1024 or width > 10000 or height > 10000:
        # while os.path.getsize(output_path) > max_size_mb * 1024 * 1024 and width > 0 and height > 0:
        while (os.path.getsize(output_path) > max_size_mb * 1024 * 1024) or (width > 10000 or height > 10000):
            # Reduce the dimensions
            width -= width // 10
            height -= height // 10
            img = img.resize((width, height), Image.Resampling.LANCZOS)

            # Try saving again with reduced dimensions
            img.save(output_path, quality=quality)

            # If still too large, reduce quality
            if os.path.getsize(output_path) > max_size_mb * 1024 * 1024:
                quality -= 5
                img.save(output_path, quality=quality)

    return output_path

def pdf_to_images(pdf_path, image_folder):
    output_prefix = os.path.join(image_folder, "output_page")

    subprocess.call(
        [
            GS_PATH,
            "-dNOPAUSE",
            "-r300",
            "-sDEVICE=jpeg",
            "-dUseCropBox",
            "-sCompression=lzw",
            "-dBATCH",
            "-o",
            output_prefix + "-%d.jpeg",
            pdf_path,
        ]
    )


async def analyze_document_async(document_analysis_client, image):
    loop = asyncio.get_event_loop()
    # Use run_in_executor to load workbook asynchronously
    # await asyncio.sleep(5)

    def wrapper():
        logger.info("*" * 10)

        rand_int = random.randint(1, 1000)

        endpoint = AZURE_DI_ENDPOINT_1
        key = AZURE_DI_KEY_1

        if rand_int % 2 == 0:
            endpoint = AZURE_DI_ENDPOINT_2
            key = AZURE_DI_KEY_2

        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )



        # Analyze the document
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=image, content_type="application/octet-stream", output_content_format=ContentFormat.MARKDOWN
        )
        
        result = poller.result()
        return result

    document = await loop.run_in_executor(None, wrapper)
    return document


async def extract_document_data(semaphore, document_analysis_client, image_path, page_num):
    async with semaphore:
        for retry_count in range(MAX_RETRY_COUNT + 1):
            try:
                # image = Image.open(image_path)
                image_data = None
                if retry_count > 0:
                    logger.info(f'\n\nTrying again, retry_count: {retry_count + 1}, Extracting text: Page {page_num}')
                else:
                    logger.info(f'Extracting text: Page {page_num}')
                with open(image_path, "rb") as image_file:
                    # image_data = f.read()
                    document = await analyze_document_async(document_analysis_client, image_file)
                return page_num, document
            except Exception as e:
                logger.info(
                    f"Exception Occurred in extracting data from {image_path}: {e}")
                logger.info(f"image {image_path} size: {Image.open(image_path).size}\n\n")

                # logger.info("\n\n\tDocument extraction interrupted, Please resolve above error.\n\n")

                if retry_count == MAX_RETRY_COUNT:
                    logger.info(f'\n\nMAX_RETRY_COUNT={MAX_RETRY_COUNT} exceeded, please process the document again.\n\n')
                    sys.exit()
                else:              
                    await asyncio.sleep(RETRY_DELAY)
                


async def extract_data_from_folder(folder_path):
    results_dict = {}
    try:
        document_analysis_client = None
        # extractor = Textractor(region_name=region_name)
    except Exception as e:
        logger.error(f"Exception while initializing OCR service: {e}")
    else:
        semaphore = asyncio.BoundedSemaphore(5)
        tasks = [
            extract_document_data(
                semaphore,
                document_analysis_client,
                os.path.join(folder_path, file_name),
                os.path.splitext(file_name)[0],
            )
            for file_name in os.listdir(folder_path)
            if file_name.endswith((".png", ".jpeg"))
        ]
        for res in asyncio.as_completed(tasks):
            page_num, document = await res
            if document:
                results_dict[page_num] = document

    return results_dict


async def process_and_extract_document(input_file_path, folder_path):
    file_name, file_extension = os.path.splitext(
        os.path.basename(input_file_path))
    output_folder_path = os.path.join(folder_path, file_name)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    images_folder = os.path.join(output_folder_path, "images")
    processed_images_folder = os.path.join(
        output_folder_path, "processed_images")
    excel_folder = os.path.join(output_folder_path, "excel")
    final_excel_folder = os.path.join(output_folder_path, "Final_Output")
    input_text_folder = os.path.join(output_folder_path, "input_text")

    for folder in [images_folder, processed_images_folder, excel_folder, final_excel_folder, input_text_folder]:
        if os.path.exists(folder):
            clear_folder(folder)
        else:
            os.makedirs(folder)

    if file_extension.lower() == '.pdf':
        pdf_to_images(input_file_path, images_folder)
    elif file_extension.lower() in (".tif", ".tiff"):
        tif_to_jpeg(input_file_path, images_folder)
    elif file_extension.lower() in (".png", ".jpeg", ".jpg"):
        convert_to_jpeg(input_file_path, images_folder)

    page_num = 1

    while True:
        image_path = os.path.join(
            images_folder, f"output_page-{page_num}.jpeg")

        if not os.path.exists(image_path):
            break

        process_image(image_path, output_folder_path)
        page_num += 1

    document_dict = await extract_data_from_folder(processed_images_folder)
    return document_dict


def sort_and_extract_page_numbers(data_dict):
    # Function to extract the page number from the key
    def page_number(key):
        return int(key.split("-")[1])

    # Sorting the dictionary by the extracted page number and creating a list of tuples (page_number, data)
    sorted_data = [
        (page_number(key), value)
        for key, value in sorted(
            data_dict.items(), key=lambda item: page_number(item[0])
        )
    ]
    return sorted_data


def get_sorted_data_with_page_numbers(pdf_filename_without_extension, document_dict):
    if not os.path.exists(f'azure_pickles/{pdf_filename_without_extension}.pickle'):
        sorted_data_with_page_numbers = sort_and_extract_page_numbers(
            document_dict)
        with open(f'azure_pickles/{pdf_filename_without_extension}.pickle', 'wb') as pickle_file:
            pickle.dump(sorted_data_with_page_numbers, pickle_file,
                        protocol=pickle.HIGHEST_PROTOCOL)

    with open(f'azure_pickles/{pdf_filename_without_extension}.pickle', 'rb') as pickle_file:
        return pickle.load(pickle_file)

