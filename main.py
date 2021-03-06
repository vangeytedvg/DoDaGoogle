import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    # The q="mimeType='application/vnd.google-apps.folder'" only retrieves folders, not files
    # in the field we map the fields we want to access afterwards in the details
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                   pageSize=100,
                                   fields="nextPageToken, files(id, name, kind, mimeType, trashed, createdTime, owners)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            # fields from the mapping above
            zen = item['owners']
            # Get specific information from the owners field (wich is a list)
            print(zen[0]['displayName'])
            print(zen[0]['kind'])
            print(
                f"{item['name']}, "
                f"{item['id']}, "
                f"{item['kind']}, "
                f"{item['mimeType']}, "
                f"{item['trashed']}, "
                f"{item['owners']}, "
                f"{item['createdTime']}")

    # This gets the files for the 'backup' directory (hence the id)
    response = service.files().list(
        q=f"parents = '1B9hpSN8OkfIJdgNTU3ApTbXyJfmZnA02'",
        spaces='drive',
        fields='nextPageToken, files(id, name, kind, mimeType, trashed, createdTime)',
        pageToken=None).execute()
    items = response.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']}, "
                  f"{item['id']}, "
                  f"{item['kind']}, "
                  f"{item['mimeType']}, "
                  f"{item['trashed']}, "
                  f"{item['createdTime']}")


if __name__ == '__main__':
    main()
