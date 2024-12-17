from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    Request,
    BackgroundTasks,
    status,
)
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from uuid import uuid4
from process_pdf_document import process_pdf_document
from utils.s3_upload import upload_to_s3_generate_presigned_download_url
from utils.json_to_xlsx import document_json_to_xlsx
from utils.cosmos_db_op import create_record, get_item_by_id, update_item
import time

app = FastAPI(title="Orix Operating Statement POC API", version="0.1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_file(file: UploadFile):
    try:

        if not os.path.exists("files"):
            os.makedirs("files")
        file_path = os.path.join("files", file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        return file_path
    except Exception as e:
        print("Exception occured while saving file locally", e)


@app.get("/")
async def root_path():
    print("here starts")
    # start = time.time()
    # time.sleep(5)
    # await asyncio.sleep(5)
    return HTMLResponse(
        content='<section><h1>This is root path!</h1><a href="/docs">Go to API docs</a></section>'
    )


@app.post("/api/get-excel-from-document-json")
async def get_excel_from_document_json(request_body: Request):
    try:
        document_json = await request_body.json()
        file_name = document_json["file_name"]
        timestamp = int(time.time())
        excel_output_path = document_json_to_xlsx(
            document_json, "./excel_output_template.xlsx", file_name, timestamp
        )
        excel_output_s3_presigned_url = None

        if os.path.exists(excel_output_path):
            excel_output_s3_presigned_url = (
                await upload_to_s3_generate_presigned_download_url(excel_output_path)
            )

        data = {
            "message": "Excel file generated Successfully!",
            "excel_output_url": excel_output_s3_presigned_url,
        }
        return JSONResponse(content=data, status_code=201)
    except Exception as e:
        return JSONResponse(
            content={
                "message": "An error occurred while processing the json to excel.",
                "error": str(e),
            },
            status_code=500,
        )


@app.post("/api/extract-pdf")
async def process_pdf_task(file: UploadFile, background_tasks: BackgroundTasks):
    task_id = str(uuid4())
    pdf_file_path = save_file(file)

    task = {
        "id": task_id,
        "file_name": file.filename,
        "status": "in progress",
        "progress": [
            {"progress_index": 1, "progress_message": "1. File Upload in Progress"}
        ],
        "result": None,
    }
    await create_record(task)
    print("*" * 20, "1. File Upload in Progress")

    task_item = await get_item_by_id(task_id)

    background_tasks.add_task(extract_pdf, pdf_file_path, task_item)

    return JSONResponse(content={"id": task_id}, status_code=status.HTTP_202_ACCEPTED)


async def extract_pdf(pdf_file_path: UploadFile, task: dict):
    try:
        task_id = task["id"]
        # pdf_file_path = save_file(file)

        input_pdf_s3_presigned_url = None
        # if os.path.exists(pdf_file_path):
        #     input_pdf_s3_presigned_url = await upload_to_s3_generate_presigned_download_url(pdf_file_path)

        task["status"] = "in progress"
        task["progress"].append(
            {"progress_index": 2, "progress_message": "1. File Upload Completed"}
        )

        task["progress"].append(
            {"progress_index": 3, "progress_message": "2. Document OCR in progress"}
        )

        await update_item(task)
        print("*" * 20, "1. File Upload Completed")
        print("*" * 20, "2. Document OCR in progress")

        output, final_json_response = await process_pdf_document(pdf_file_path, task)
        excel_output_s3_presigned_url = None

        if os.path.exists(output):
            excel_output_s3_presigned_url = (
                await upload_to_s3_generate_presigned_download_url(output)
            )

        data = {
            "message": "File uploaded and processed successfully!",
            "file_path": pdf_file_path,
            "excel_output_url": excel_output_s3_presigned_url,
            "pdf_url": input_pdf_s3_presigned_url,
            "json_response": final_json_response,
        }
        task["status"] = "completed"
        task["result"] = data
        task["progress"].append(
            {"progress_index": 8, "progress_message": "4. Excel Output Generated"}
        )

        await update_item(task)
        print("*" * 20, "4. Excel Output Generated")

    #     return JSONResponse(content=data)
    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)

        await update_item(task)
        print(
            f"Error occured while processing the document. method: {extract_pdf.__name__} ",
            e,
        )
    #     return JSONResponse(content={"message": "An error occurred while processing the document.", "error": str(e)}, status_code=500)


@app.get("/api/status/{task_id}")
async def get_process_pdf_task_status(task_id: str):
    try:
        task = await get_item_by_id(task_id)
        return JSONResponse(task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while fetching document extraction status",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
