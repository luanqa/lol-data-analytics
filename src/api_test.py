import requests
import json

def buscar_dados():
    url = "http://httpbin.org/get"
    params = {"nome": "Carlos", "idade": 32}
    response = requests.get(url, params=params)

    #print(response.status_code)
    #print(response.json())
    dados = response.json()
    print(type(response.status_code))
    return(dados)

buscar_dados()