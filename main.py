import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# declaring variables
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
IMAGES_DIR = "./images/"
PRES_ID = input('Введите ID презентации: ')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

slides_service = build('slides', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# get slides size
presentation = slides_service.presentations().get(
    presentationId=PRES_ID).execute()

slide_size = presentation['pageSize']


# function to create slide
def create_slide(pres_id):
    slides_service = build('slides', 'v1', credentials=credentials)

    body = {
        'requests': [{
            'createSlide': {
                'slideLayoutReference': {
                    'predefinedLayout': 'BLANK'
                }
            }
        }]
    }
    response = slides_service.presentations().batchUpdate(
        presentationId=pres_id,
        body=body
    ).execute()

    return response['replies'][0]['createSlide']['objectId']


# function to add image to new slide
def add_image_to_slide(pres_id, slide_size, photo_id):

    slide_id = create_slide(pres_id)

    image_url = 'https://drive.google.com/uc?id='+photo_id
    print(image_url)
    body = {
        'requests': [{
            'createImage': {
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': slide_id,
                    'size': {
                        'height': {
                            'magnitude': slide_size['height']['magnitude'],
                            'unit': 'EMU'
                        },
                        'width': {
                            'magnitude': slide_size['width']['magnitude'],
                            'unit': 'EMU'
                        }
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 0,
                        'translateY': 0,
                        'unit': 'PT'
                    }
                }
            }
        }]
    }

    slides_service.presentations().batchUpdate(
        presentationId=pres_id,
        body=body
    ).execute()


# function to upload photo to google drive
def upload_photo(image_path):
    file_metadata = {
        'name': 'slide.png',
        'mimeType': 'image/png'
    }

    media = MediaFileUpload(image_path, mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    drive_service.permissions().create(
        fileId=file.get('id'),
        body={'role': 'writer', 'type': 'anyone'}
    ).execute()

    return file.get('id')


# function to delete photo from google drive
def delete_photo(photo_id):
    drive_service.files().delete(fileId=photo_id).execute()


# get photos from images folder and upload to google slides
photos = os.listdir(IMAGES_DIR)
for photo in photos:
    photo_id = upload_photo(IMAGES_DIR+str(photo))
    add_image_to_slide(PRES_ID, slide_size, photo_id)
    delete_photo(photo_id)
