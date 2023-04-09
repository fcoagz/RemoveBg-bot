import requests

class ApiRemoveBg:
    def __init__(self, api_remove_bg) -> None:
        self.api_remove = api_remove_bg

    def publish(self, image_url, size='auto'):
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data= {
            'image_url' : image_url,
            'size' : size
            },
            headers={
            'X-Api-Key' : self.api_remove
            }
        )

        if response.status_code == 200:
            with open('src/photo/remove-bg.png', 'wb') as new_file:
                new_file.write(response.content)
                print('La solicitud a la API de Remove.bg funcionó correctamente')
        else:
            print(response.json()['errors'][0]['title'])