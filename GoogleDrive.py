import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


class GoogleDrive:

    def __init__(self):
        """
        Ctor
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('drive', 'v3', credentials=self.creds)

    def get_drive_folders(self, pagesize: int) -> list:
        # The q="mimeType='application/vnd.google-apps.folder'" only retrieves folders, not files
        # in the field we map the fields we want to access afterwards in the details
        results = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            pageSize=pagesize,
                                            fields="nextPageToken, files(id, name, kind, mimeType, trashed, createdTime, owners)").execute()
        items = results.get('files', [])
        folder_list = []
        if not items:
            return None
        else:
            folder_list = []
            for item in items:
                zen = item['owners']
                folder_details = {
                    'owner_name': zen[0]['displayName'],
                    'owner_kind': zen[0]['kind'],
                    'fileid': item['id'],
                    'filename': item['name'],
                    'file_kind': item['kind'],
                    'mime_type': item['mimeType'],
                    'trashed': item['trashed'],
                    'created_time': item['createdTime']
                }
                folder_list.append(folder_details)
        return folder_list

    def get_files_in_folder(self, folder_id: str) -> list:
        # This gets the files for the 'backup' directory (hence the id)
        # '1B9hpSN8OkfIJdgNTU3ApTbXyJfmZnA02'
        response = self.service.files().list(
            q=f"parents = '{folder_id}'",
            spaces='drive',
            fields='nextPageToken, files(id, name, kind, mimeType, trashed, createdTime, owners)',
            pageToken=None).execute()
        items = response.get('files', [])

        folder_list = []
        if not items:
            return None
        else:
            folder_list = []
            for item in items:
                zen = item['owners']
                folder_details = {
                    'owner_name': zen[0]['displayName'],
                    'owner_kind': zen[0]['kind'],
                    'fileid': item['id'],
                    'filename': item['name'],
                    'file_kind': item['kind'],
                    'mime_type': item['mimeType'],
                    'trashed': item['trashed'],
                    'created_time': item['createdTime']
                }
                folder_list.append(folder_details)
        return folder_list
