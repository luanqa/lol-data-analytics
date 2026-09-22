import requests
import json

def buscar_dados():
    url = "http://httpbin.org/get"
    params = {"nome": "Carlos", "idade": 32}
    response = requests.get(url, params=params)

    #print(response.status_code)
    #print(response.json())
    
    if(response.status_code == 200):
        dados = response.json()
        return(dados)

