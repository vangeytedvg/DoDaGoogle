import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
##SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']



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

    def get_files_in_folder(self, folder_id: str) -> list:
        """
        Get the files in the specified folder
        :param folder_id: The id of the selected folder
        :return: List with dictionary of files found in the folder
        """
        if folder_id:
            response = self.service.files().list(
                q=f"parents = '{folder_id}'",
                spaces='drive',
                fields='nextPageToken, files(id, name, kind, mimeType, trashed, createdTime, owners, parents)',
                pageToken=None).execute()
        else:
            response = self.service.files().list(
                # q=f"parents = '{folder_id}'",
                spaces='drive',
                fields='nextPageToken, files(id, name, kind, mimeType, trashed, createdTime, owners, parents)',
                pageToken=None).execute()
        # Get array of the items
        items = response.get('files', [])

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
                    'created_time': item['createdTime'],
                    'parents': item['parents']
                }
            folder_list.append(folder_details)
        return folder_list

    def upload_file(self, filename: str, path: str, folder_id: str):
        """ Load a new file or update an existing one """
        media = MediaFileUpload(f"{path}/{filename}", resumable=True)
        response = self.service.files().list(
            q=f"name='{filename}' and parents = '{folder_id}'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=None).execute()

        if len(response['files']) == 0:
            # File was not found, so create a brand new file in the google drive
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return file
        else:
            for myfile in response.get('files', []):
                # Process changed files
                update_file = self.service.files().update(
                    fileId=myfile.get('id'),
                    media_body=media, ).execute()

            return "Updated"

    def test_run(self, l: int):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=l,
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])
        if not items:
            return "No items found"
        else:
            return items
