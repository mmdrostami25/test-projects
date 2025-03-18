import requests
import json
import os

def get_instagram_photos(user_id, access_token):
    # Define the endpoint URL
    url = f'https://graph.instagram.com/{user_id}/media?access_token={access_token}'

    # Make a request to the Instagram API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print(f'Error fetching data: {response.status_code}')
        return []

def download_photos(photos):
    if not os.path.exists('instagram_photos'):
        os.makedirs('instagram_photos')

    for photo in photos:
        image_url = photo.get('media_url')
        if image_url:
            photo_id = photo.get('id')
            img_data = requests.get(image_url).content
            with open(f'instagram_photos/{photo_id}.jpg', 'wb') as img_file:
                img_file.write(img_data)
            print(f'Downloaded {photo_id}.jpg')

if __name__ == '__main__':
    user_id = input('Enter Instagram User ID: ')  # Input for user ID
    access_token = 'https://www.instagram.com/'  # Replace with your access token

    photos = get_instagram_photos(user_id, access_token)
    download_photos(photos)
