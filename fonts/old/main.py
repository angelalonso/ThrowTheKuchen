from game import GameLoop
import requests
import json

def start():
    newGame = GameLoop()
    newGame.run()

def test():
    api_url_base = 'http://127.0.0.1:5000/'
    api_url = '{0}info'.format(api_url_base)

    response = requests.get(api_url)
    exitcode = response.status_code
    data = json.loads(response.content.decode('utf-8'))
    print(data)

if __name__ == "__main__":
#    test()
    start()
