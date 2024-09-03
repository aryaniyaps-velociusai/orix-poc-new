import os
import uuid
import boto3
import aioboto3
from botocore.exceptions import ClientError
import asyncio
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('AWS_S3_BUCKET')


async def upload_to_s3_generate_presigned_download_url(file_path):
    id = str(uuid.uuid4())

    s3_key = f"clearstreet-advisors/due-dilligence/output/{id}"
    await upload_file_to_s3(file_path, BUCKET_NAME, s3_key)

    # s3_client.upload_file(file_path, BUCKET_NAME, s3_key)


    file_name = os.path.basename(file_path)

    presign_url = await generate_presigned_url(BUCKET_NAME, s3_key, file_name)

    # presign_url = s3_client.generate_presigned_url(
    #     ClientMethod='get_object',
    #     Params={
    #         'Bucket': BUCKET_NAME,
    #         'Key': s3_key,
    #         'ResponseContentDisposition': f"attachment; filename = {urllib.parse.quote(file_name)}"
    #     },
    #     ExpiresIn=3600)
    # print(presign_url)

    return presign_url


# test_file = "Title Data Sample.xlsx"
#
# upload_to_s3_generate_presigned_download_url(test_file)

async def upload_file_to_s3(file_path, bucket_name, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_path

    # Create an S3 client
    async with aioboto3.Session().client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    ) as s3_client:
        try:
            await s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False
    return True

async def generate_presigned_url(bucket_name, object_name, file_name = None, expiration=3600):
    async with aioboto3.Session().client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    ) as s3_client:
        try:
            params={'Bucket': bucket_name, 'Key': object_name}
            if file_name:
                params['ResponseContentDisposition'] = f"attachment; filename = {urllib.parse.quote(file_name)}"

            response = await s3_client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expiration
            )
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
    return response

async def main():
    file_path = 'Title Reports/541-956999_Title Report.pdf'
    object_name = 'your-object-name-in-s3.txt'
    id = str(uuid.uuid4())
    s3_key = f"clearstreet-advisors/due-dilligence/output/{id}"

    # Upload the file
    upload_success = await upload_file_to_s3(file_path, BUCKET_NAME, s3_key)
    if upload_success:
        # Generate presigned URL
        presigned_url = await generate_presigned_url(BUCKET_NAME, s3_key)
        if presigned_url:
            print(f"Presigned URL: {presigned_url}")

if __name__ == '__main__':
    asyncio.run(upload_to_s3_generate_presigned_download_url('Title Reports/541-956999_Title Report.pdf'))