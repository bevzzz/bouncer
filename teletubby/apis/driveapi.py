import os
import io
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleDrive:
    """
    This class is responsible for establishing connection (authorizing)
    with Google Drive API and manipulating files (i.e. uploading,
    downloading DriveObjects, moving them between folder, deleting them etc.)
    """

    api_version = 'v3'
    GOOGLE_MIME = {
        'folder': 'application/vnd.google-apps.folder'
    }

    def __init__(self, scope, token_path, credentials_path):
        self.scope = scope
        self.credentials = self.authorize(credentials_path, token_path)
        self.service = self.build_service()

    @classmethod
    def from_config_file(cls, config):
        google_drive = cls(
            scope=config['scope'],
            token_path=config['filepath']['token'],
            credentials_path=config['filepath']['credentials']
        )
        return google_drive

    def authorize(self, credentials_path, token_path):
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        else:
            creds = None

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.scope)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def build_service(self):
        return build('drive', self.api_version, credentials=self.credentials)

    def download_file(self, drive_id):
        req = self.service.files().get_media(fileId=drive_id)
        container = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=container, request=req)

        done = None
        while not done:
            status, done = downloader.next_chunk()
        container.seek(0)
        return container

    def upload_file(self, file, folder_id):
        media_body = file.get_upload_media()
        file = self.service.files().create(
            body=self.build_metadata(file, folder_id),
            media_body=media_body,
            fields='id'
        ).execute()
        return file['id']

    @staticmethod
    def build_metadata(file, folder_id):
        metadata = {
            'name': file.name,
            'parents': [folder_id]
        }
        return metadata

    def get_folder_id_by_name(self, name):
        if self._exists_folder(name):
            folder_id = self._get_folder_by_name(name)['id']
        else:
            folder = self._create_folder(name)
            folder_id = folder['id']
        return folder_id

    def _get_folder_by_name(self, name):
        all_folders = self._get_all_folders()
        return [f for f in all_folders if f.get('name', '') == name][0]

    def _exists_folder(self, name):
        all_folders = self._get_all_folders()
        try:
            result = any(f.get('name') == name for f in all_folders)
        except IndexError:
            result = False
        return result

    def _get_all_folders(self):
        query = "mimeType='{}'".format(self.GOOGLE_MIME['folder'])
        response = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        return response['files']

    def _create_folder(self, name):
        metadata = {
            'name': name,
            'mimeType': self.GOOGLE_MIME['folder']
        }

        folder = self.service.files().create(
            body=metadata,
            fields='id'
        ).execute()

        return folder
