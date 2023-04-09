import json

def verifyApiRemove(chat_id):
    results = False
    with open('src/config.json', 'r') as archivos:
        file = json.load(archivos)
        for id in file:
            if id == chat_id: results = True
    return results

def registerApiRemove(chat_id, api_remove):
    with open('src/config.json', 'w') as archivos:
        data = {'X-Api-Key' : api_remove}
        archivos.seek(0)
        archivos.write(json.dumps({f'{chat_id}': data}, indent=4))
        archivos.truncate()