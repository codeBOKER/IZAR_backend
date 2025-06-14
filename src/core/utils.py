import requests
from django.conf import settings

def upload_image_to_imgur(image_file):
    """Uploads an image file to Imgur and returns the image URL."""

    headers = {'Authorization': f'Client-ID {settings.IMGUR_CLIENT_ID}'}
    files = {'image': image_file.read()}
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)
    if response.status_code == 200:
        return response.json()['data']['link']
    raise Exception('Imgur upload failed: ' + response.text)
