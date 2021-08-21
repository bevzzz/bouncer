# imports for authentication
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleDriveStorage:

    _SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    def __init__(self):
        self._service = self.authorize()

    def authorize(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('/resources/config/token.json'):
            creds = Credentials.from_authorized_user_file('/resources/config/token.json', self._SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'resources/config/credentials.json', self._SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('resources/config/token.json', 'w') as token:
                token.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)

    def upload_pdf(self):
        pass

    def upload_img(self):
        pass

    def list_directories(self):
        request = self._service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=None
        )
        return request.execute()


drive = GoogleDriveStorage()
print(drive.list_directories())