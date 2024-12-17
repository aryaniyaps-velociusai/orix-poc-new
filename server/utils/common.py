import json
import logging
import os
from datetime import datetime

logger = logging.getLogger("orix-poc-logger")


def is_mm_dd_yyyy(date_str):
    try:
        date_object = datetime.strptime(date_str, "%m/%d/%Y")
        return datetime.strftime(date_object, "%m/%d/%Y") == date_str
    except ValueError:
        return False


def get_filename_without_extension(file_path):
    # Get the base name from the file path
    base_name = os.path.basename(file_path)
    # Split the base name into filename and extension, and get just the filename
    filename_without_extension = os.path.splitext(base_name)[0]
    return filename_without_extension


def create_subfolders(file_path):
    # Get the directory path from the file path
    directory = os.path.dirname(file_path)

    # Check if the directory exists
    if not os.path.exists(directory):
        # If it does not exist, create the directory and all intermediate directories
        os.makedirs(directory)
        logger.info(f"Created directories for path: {directory}")
    else:
        logger.info(f"Directories already exist for path: {directory}")
