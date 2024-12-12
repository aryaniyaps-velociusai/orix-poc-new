import glob
import json
import logging
import sys
import os
from dotenv import load_dotenv
import fitz

from services.azure_ocr import get_text_from_pdf_with_doc_intelligence
from services.response_formatter import format_os_response
from utils.calculate_totals import calculate_totals
from utils.common import get_filename_without_extension, create_subfolders
from utils.prompt import get_balance_sheet_user_prompt, get_income_statement_user_prompt
from utils.cosmos_db_op import update_item
from utils.decorators import log_execution_time, log_execution_time_async
from utils.helpers import clear_folder
from utils.json_to_xlsx import json_to_xlsx
from services.extractor import process_and_extract_document, get_sorted_data_with_page_numbers
from services.openai_request import extract_data_azure_openai
import time
from utils.calculate_confidence_score_and_coordinates_list import update_confidence_score_with_coordinates
from logging import Logger
from utils.logger_util import setup_logger
from utils.m_graph import MGraphUtil
from services.financial_prompt_updater import get_financial_items



load_dotenv()

SHAREPOINT_LOGS_FOLDER_PATH = os.getenv('SHAREPOINT_LOGS_FOLDER_PATH')



@log_execution_time_async
async def process_pdf_document(pdf_path, task):
    # datefmt = '%Y-%m-%d %H:%M:%S'
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - line: %(lineno)d -\n %(message)s', datefmt=datefmt)
    logger = logging.getLogger('orix-poc-logger')
    task_id = task["id"]
    log_path = ''
    logger = None
    pdf_filename_without_extension = get_filename_without_extension(pdf_path)
    excel_output_path = ''
    timestamp = int(time.time())
    ocr_response_text_path = f'textract_response_output/layout_text_response_{pdf_filename_without_extension}.txt'
    json_response_path = f"json_response_folder/json_response_{pdf_filename_without_extension}_{timestamp}.json"
    formatted_json_response_path = f"formatted_json_response_folder/formatted_json_response_{pdf_filename_without_extension}_{timestamp}.json"
    openai_json_response_path = f"openai_json_response_folder/openai_json_response_{pdf_filename_without_extension}_{timestamp}.json"
    azure_ocr_json_response_path = f"azure_ocr_json_response_folder/azure_ocr_json_response_{pdf_filename_without_extension}_{timestamp}.json"
    create_subfolders(json_response_path)
    create_subfolders(formatted_json_response_path)
    create_subfolders(openai_json_response_path)
    create_subfolders(ocr_response_text_path)
    create_subfolders(azure_ocr_json_response_path)


    try:

        log_path = f'logs/{pdf_filename_without_extension}/log-{timestamp}-{pdf_filename_without_extension}.log'
        
        logger:Logger = setup_logger(log_path)

        logger.info(f'Filename: {pdf_filename_without_extension}')

        logger.info('2. OCR Started ####')
        # output_folder_path = "./output_images_folder"

        # document_dict = None

        # pickle_file_path = f'azure_pickles/{pdf_filename_without_extension}.pickle'

        # create_subfolders(pickle_file_path)


        # if not os.path.exists(output_folder_path):
        #     os.makedirs(output_folder_path)

        # if not os.path.exists(pickle_file_path):
        #     document_dict = await process_and_extract_document(input_file_path=pdf_path, folder_path=output_folder_path)
        # else:
        #     logger.debug(f'Extracted Textract Document already exists for file: {pdf_filename_without_extension} ')

        # clear_folder(output_folder_path)

        # sorted_data_with_page_numbers = get_sorted_data_with_page_numbers(
        #     pdf_filename_without_extension=pdf_filename_without_extension, document_dict=document_dict)

        # PAGE_SEPARATOR = "\n\n"
        # extracted_text = ""

        # # <!-- PdfDocumentPageNumber 7 -->
        # for page_no, document in sorted_data_with_page_numbers:
        #         extracted_text += PAGE_SEPARATOR
        #         extracted_text += f"<!-- PdfDocumentPageNumber {page_no} -->"
        #         extracted_text += PAGE_SEPARATOR
        #         extracted_text += document.content
        #         extracted_text += "\n"
        #     # logger.info(extracted_text)
        # # print(extracted_text)
        # with open(f"textract_response_output/layout_text_response_{pdf_filename_without_extension}.md", "w", encoding="utf-8") as file:
        #     file.write(extracted_text)

        # azure_ocr_json_response = {"azure_ocr_pages_response": {}}
        # for page_num, document in sorted_data_with_page_numbers:
        #     azure_ocr_json_response['azure_ocr_pages_response'][str(page_num)] = document.as_dict()

        # create_subfolders(azure_ocr_json_response_path)
        # with open(azure_ocr_json_response_path, "w") as file:
        #     file.write(json.dumps(azure_ocr_json_response, indent=2))



        logger.info('2. OCR Completed')
        task["progress"].append(
            {
                "progress_index": 4,
                "progress_message": "2. Document OCR Completed"
            }
        )
        task["progress"].append(
            {
                "progress_index": 5,
                "progress_message": "3. Document Extraction in Progress"
            }
        )

        await update_item(task)

        print("*"*20, "2. Document OCR Completed")
        print("*"*20, "3. Document Extraction in Progress")

        extracted_text, azure_ocr_json_response = get_text_from_pdf_with_doc_intelligence(pdf_path)
        

        


        json_response = {}

                # fetch from DBsamp
        # fetch bs_key
        #     -> updated_prompt
        #     -> user_feedback_bs
        # fetch is_key
        #     -> updated_prompt

        financial_items = await get_financial_items()
        updated_income_statement_prompt = financial_items["updated_income_statement_prompt"]
        income_statement_user_feedback = {} if financial_items["income_statement_user_feedback"] is None else financial_items["income_statement_user_feedback"]
        updated_balance_sheet_prompt = financial_items["updated_balance_sheet_prompt"]
        balance_sheet_user_feedback = {} if financial_items["balance_sheet_user_feedback"] is None else financial_items["balance_sheet_user_feedback"]

        # get balance sheet
        balance_sheet_user_prompt = get_balance_sheet_user_prompt(updated_balance_sheet_prompt)
        balance_sheet_openai_response, _ = await extract_data_azure_openai(balance_sheet_user_prompt,extracted_text,balance_sheet_user_feedback)

        balance_sheet_json_response = json.loads(balance_sheet_openai_response)

        json_response["is_balance_sheet_present"] = balance_sheet_json_response["is_balance_sheet_present"]
        json_response["balance_sheet"] = balance_sheet_json_response["balance_sheet"]
        
        logger.info("Balance Sheet Extracted.")
        logger.info(json.dumps(balance_sheet_json_response, indent=2))


        # get income statement
        income_statement_user_prompt = get_income_statement_user_prompt(updated_income_statement_prompt)
        income_statement_openai_response, _ = await extract_data_azure_openai(income_statement_user_prompt,extracted_text,income_statement_user_feedback)

        income_statement_json_response = json.loads(income_statement_openai_response)

        json_response["is_income_statement_present"] = income_statement_json_response["is_income_statement_present"]
        json_response["income_statement"] = income_statement_json_response["income_statement"]

        logger.info("\n\n***********************\n\n***********************\n\n")
        logger.info("Income Statement Extracted.")
        logger.info(json.dumps(income_statement_json_response, indent=2))

        # 

        with open(openai_json_response_path, "w") as file:
            file.write(json.dumps(json_response, indent=2))


        formatted_json_response = format_os_response(json_response, balance_sheet_user_feedback, income_statement_user_feedback)

        with open(formatted_json_response_path, "w") as file:
            file.write(json.dumps(formatted_json_response, indent=2))
        
        
        # formatted_json_response = None
        # with open('formatted_json_response_folder/formatted_json_response_107311---DPO---Operating-Statements---9-30-2023---THE-TERRACE-OF-HAMMOND-PHASE-I_1725860900.json', "r") as file:
        #     formatted_json_response = json.load(file)

        final_json_response = calculate_totals(formatted_json_response)
        final_json_response = update_confidence_score_with_coordinates(final_json_response, azure_ocr_json_response)
        with open(json_response_path, "w") as file:
            file.write(json.dumps(final_json_response, indent=2))

        excel_output_path = json_to_xlsx(final_json_response, 'excel_output_template.xlsx', pdf_filename_without_extension, timestamp)

        
        task["progress"].append(
            {
                "progress_index": 6,
                "progress_message": "3. Document Extraction Completed"
            }
        )
        task["progress"].append(
            {
                "progress_index": 7,
                "progress_message": "4. Generating Excel Output"
            }
        )

        await update_item(task)

        print("*"*20, "3. Document Extraction Completed")

        # primary_mortgages_with_confidence = update_confidence_score_with_coordinates(primary_mortgages, azure_ocr_json_response)
        # assignments_with_confidence = update_confidence_score_with_coordinates(assignments, azure_ocr_json_response)
        # re_recorded_mortgages_with_confidence = update_confidence_score_with_coordinates(re_recorded_mortgages, azure_ocr_json_response)

        # output_json = {}

        # output_json['primary_mortgages'] = primary_mortgages_with_confidence
        # output_json['re_recorded_mortgages'] = re_recorded_mortgages_with_confidence
        # output_json['assignments'] = assignments_with_confidence
        
        # output_json_folder_path = f"output_json_folder/output_json_{pdf_filename_without_extension}_{timestamp}.json"
        # create_subfolders(output_json_folder_path)
        # with open(output_json_folder_path, "w") as file:
        #     file.write(json.dumps(output_json, indent=2)) 

        return excel_output_path, final_json_response
    except Exception as e:
        print("**********"*50)
        print("An error occured!", e)
        # print(e.with_traceback())
        print("**********"*50)
        task["status"] = "failed"
        task["error"] = str(e)

        await update_item(task)
        
        if logger:
            logger.debug(e)
        print(e)
        raise
        return '', [], [], [], {}
    finally:

        try:

            access_token = os.getenv('GRAPH_API_ACCESS_TOKEN')
            folder_path_list = []
            # try:
            mgu = MGraphUtil(SHAREPOINT_LOGS_FOLDER_PATH)
            onedrive_folder_graph_url = await mgu.get_drive_path(mgu.onedrive_url, token=access_token)

            if onedrive_folder_graph_url and os.path.exists(log_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, log_path, token=access_token)
                folder_path_list.append(os.path.dirname(log_path))
            
            if onedrive_folder_graph_url and os.path.exists(excel_output_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, excel_output_path, token=access_token)
                folder_path_list.append(os.path.dirname(excel_output_path))
            
            if onedrive_folder_graph_url and os.path.exists(ocr_response_text_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, ocr_response_text_path, token=access_token)
                folder_path_list.append(os.path.dirname(ocr_response_text_path))
            
            if onedrive_folder_graph_url and os.path.exists(azure_ocr_json_response_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, azure_ocr_json_response_path, token=access_token)
                folder_path_list.append(os.path.dirname(azure_ocr_json_response_path))
            
            if onedrive_folder_graph_url and os.path.exists(json_response_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, json_response_path, token=access_token)
                folder_path_list.append(os.path.dirname(json_response_path))

            if onedrive_folder_graph_url and os.path.exists(formatted_json_response_path):
                await mgu.upload_to_onedrive(onedrive_folder_graph_url, pdf_filename_without_extension, formatted_json_response_path, token=access_token)
                folder_path_list.append(os.path.dirname(formatted_json_response_path))
        except Exception as e:
            print("**************"*10)
            print("Error occured while pushing files to sharepoint")
            print("**************"*10)
        

        # finally:
        #     if not access_token:
        #         for folder_path in folder_path_list:
        #             clear_folder(folder_path=folder_path)
        #             print(f'Cleared folder: {folder_path}')
        

# if __name__ == '__main__':
#
#     cli_args = sys.argv
#
#     if len(cli_args) < 2:
#         print('insufficient arguments, Please provide document name to process')
#         sys.exit(1)
#
#     pdf_path = sys.argv[1]
#     temp_pdf_file_path = './source_docs/132-261475 - 728 E ILLINOIS AVE, CARTERVILLE, IL 62918.pdf'
#
#     if not os.path.exists(pdf_path):
#         print("Error: File does not exist.")
#         sys.exit(1)
#
#     asyncio.run(process_pdf_document(pdf_path))

# python app.py <file_name>
