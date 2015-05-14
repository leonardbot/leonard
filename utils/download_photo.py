import requests
import os

try:
    # Try to create file directory
    os.mkdir('files')
except FileExistsError:
    # If it already created - pass
    pass


def download_photo(photo_url):
    # Get name of file
    file_name = photo_url.split('/')[-1]
    response = requests.get(photo_url)
    if response.status_code == 200:
        file = open("files/" + file_name, 'wb')
        file.write(response.content)
        file.close()
        return "files/" + file_name
    else:
        return ''
