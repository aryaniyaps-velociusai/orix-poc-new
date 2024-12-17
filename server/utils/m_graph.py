import base64
import logging
import os
import re
import urllib.parse

from constants import BROWSER_URL, DEBUG_FLAG, Method
from utils.helpers import api_call, get_token

# from config import DefaultConfig

METHOD = Method()
# CONFIG = DefaultConfig()
logger = logging.getLogger("orix-poc-logger")


class MGraphUtil:
    def __init__(self, link_extracted=None):
        self.onedrive_url, self.shared_type = None, None
        if link_extracted:
            self.onedrive_url, self.shared_type = self._extract_onedrive_url(
                link_extracted
            )
        self.base_url = "https://graph.microsoft.com/v1.0"

    async def get_user_detail(self, user_id):
        try:
            mail_url = f"{self.base_url}/users/{user_id}"
            access_token = get_token()
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json",
            }
            return await api_call(METHOD.GET, mail_url, headers)
        except Exception as e:
            logger.info(f"exception while fetching user's detail: {e}")
        return None, None, None

    def _extract_onedrive_url(self, text):
        # shareable url
        pattern = "https://[\w]+[\-my]*\.sharepoint\.com/:([a-z]):/[^\s]+"

        # Search for the pattern in the provided text
        match = re.search(pattern, text)
        if match:
            return match.group(0), match.group(1)

        # browser url
        pattern_2 = "https://[\w]+[\-my]*\.sharepoint\.com/personal/[^\s]+"
        match = re.search(pattern_2, text)
        if match:
            return match.group(0), BROWSER_URL

        return None, None

    def get_encoded_url(self, url):
        base_64_value = (
            base64.urlsafe_b64encode(url.encode("utf-8")).rstrip(b"=").decode("utf-8")
        )
        encoded_url = "u!" + base_64_value.replace("/", "_").replace("+", "-")
        return encoded_url

    def create_graph_api_link(self, url):
        encoded_url = self.get_encoded_url(url)
        drive_item_url = self.base_url + f"/shares/{encoded_url}/driveItem"
        graph_api_url = self.base_url + f"/shares/{encoded_url}/root/children"
        return drive_item_url, graph_api_url

    async def get_drive_path(self, shareable_url, token=None):
        drive_item_url, _ = self.create_graph_api_link(shareable_url)
        access_token = get_token()
        if token is not None:
            access_token = token
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        status_code, _, res_json = await api_call(
            METHOD.GET, drive_item_url, headers=headers
        )
        if status_code != 200:
            return None

        if res_json.get("folder"):
            return (
                self.base_url
                + f'{res_json["parentReference"]["path"]}/{res_json["name"]}'
            )
        return None

    async def list_children(self, drive_id, item_id):
        url = self.base_url + f"/drives/{drive_id}/items/{item_id}/children"
        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        status_code, reason, res_json = await api_call(METHOD.GET, url, headers=headers)
        if status_code != 200:
            logger.info(f"Error while listing children: {reason}")
            return []
        return res_json.get("value", [])

    async def delete_item(self, drive_id, item_id):
        delete_url = self.base_url + f"/drives/{drive_id}/items/{item_id}"
        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        status_code, reason, _ = await api_call(
            METHOD.DELETE, delete_url, headers=headers
        )
        if status_code != 204:
            logger.info(f"Error while deleting the item: {reason}")
            return False
        return True

    async def copy_item(
        self, from_drive_id, from_item_id, to_drive_id, to_item_id, name
    ):
        copy_url = self.base_url + f"/drives/{from_drive_id}/items/{from_item_id}/copy"
        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        req_body = {
            "parentReference": {"driveId": to_drive_id, "id": to_item_id},
            "name": name,
        }

        status_code, reason, _ = await api_call(
            METHOD.POST, copy_url, headers=headers, data=req_body
        )
        if status_code != 202:
            logger.info(f"Error while copying the items: {reason}")
            return False
        return True

    def _change_to_email(self, underscored_words):
        words = underscored_words.split("_")
        return ".".join(words[:-2]) + "@" + ".".join(words[-2:])

    def _convert_onedrive_to_graph_components(self, onedrive_url):
        # Extract username and domain from URL
        user_domain = onedrive_url.split("/personal/")[1].split("/")[0]

        email = self._change_to_email(user_domain)

        # Extract folder name from URL
        folder_names = urllib.parse.unquote(
            onedrive_url.split("id=")[1].split("&")[0]
        ).split("/")

        dir_path = ""
        start_concat = False
        for folder in folder_names:
            if folder == "Documents":
                start_concat = True
                continue
            if start_concat:
                dir_path += f"/{folder}"

        # Assemble the root URL
        root_url = f"users/{email}/drive/root:"

        dir_url_check = f"{self.base_url}/{root_url}/{dir_path}"
        dir_url = f"{self.base_url}/{root_url}/{dir_path}:/children"

        return dir_url_check, dir_url, folder_names[-1]

    async def create_shareable_link(self, base_url, item_id):
        drive_url = base_url.split("/root:")[0]
        create_link_url = f"{drive_url}/items/{item_id}/createLink"

        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        req_body = {"type": "edit", "scope": "organization"}
        status_code, reason, res_json = await api_call(
            METHOD.POST, create_link_url, headers=headers, data=req_body
        )
        if status_code in [200, 201]:
            return res_json["link"]["webUrl"]
        logger.info(
            f"Failed to create shareable link. Status code: {status_code}, Response: {reason}"
        )
        return None

    async def grant_access_to_sharing_link(self, url, emails):
        encoded_url = self.get_encoded_url(url)
        grant_url = (
            f"https://graph.microsoft.com/v1.0/shares/{encoded_url}/permission/grant"
        )

        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        recipients = []
        for email in emails:
            recipients.append({"email": email})

        req_body = {"recipients": recipients, "roles": ["write"]}

        status_code, reason, _ = await api_call(
            METHOD.POST, grant_url, headers=headers, data=req_body
        )
        if status_code == 200:
            return True
        logger.info(
            f"Failed to grant access. Status code: {status_code}, Response: {reason}"
        )
        return False

    async def create_folder_onedrive(self, base_write_url: str, directory_name: str):
        create_folder_url = f"{base_write_url}:/children"
        access_token = get_token()

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }

        folder_data = {
            "name": directory_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename",
        }

        status_code, reason, res_json = await api_call(
            METHOD.POST, create_folder_url, headers=headers, data=folder_data
        )

        # Check if the folder creation was successful
        if status_code == 201:
            logger.info(f"Folder '{directory_name}' created successfully.")
            return (
                res_json.get("name"),
                res_json.get("id"),
                res_json["parentReference"]["driveId"],
            )
        logger.info(
            f"Failed to create folder. Status code: {status_code}, Response: {reason}"
        )
        return None, None, None

    def get_name_and_content(self, file_path):
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            file_content = file.read()
        return filename, file_content

    async def check_folder_exists(self, write_url: str, folder_name: str):
        token = get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Prefer": "bypass-shared-lock",
        }
        url = f"{write_url}/{folder_name}"

        status_code, _, _ = await api_call(METHOD.GET, url, headers=headers)
        if status_code == 404:
            return False
        return True

    async def upload_to_onedrive(
        self, driver_folder_url: str, subfolder_name: str, file_path: str, token=None
    ):
        status = []

        access_token = get_token()
        if token:
            access_token = token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Prefer": "bypass-shared-lock",
        }

        filename, file_content = self.get_name_and_content(file_path)

        # filename_without_extension = ".".join(filename.split('.')[:-1])

        excel_write_url = f"{driver_folder_url}/{subfolder_name}/{filename}:/content"
        status_code, reason, res_json = await api_call(
            METHOD.PUT, excel_write_url, headers=headers, data=file_content
        )

        if status_code in [200, 201, 202, 203]:
            logger.debug(f"'{filename}' generated.")

        else:
            logger.debug(f"{DEBUG_FLAG}:'{filename}' not generated. {reason}")
            return None

        return res_json["webUrl"]
