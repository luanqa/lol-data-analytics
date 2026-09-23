from datetime import datetime, timezone, timedelta
import os
import requests
import json
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("RIOT_API_KEY")

def buscar_dados():
    url = "http://httpbin.org/get"
    params = {"nome": "Carlos", "idade": 32}
    response = requests.get(url, params=params)

    #print(response.status_code)
    #print(response.json())
    
    if(response.status_code == 200):
        dados = response.json()
        return(dados)

    
def buscar_dadosRiot(gameName, tagLine):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{quote(gameName)}/{quote(tagLine)}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    print(response.text)

def buscar_partidas(nick, tag):
    dados = buscar_dadosRiot(nick, tag)
    params = {"count": 10}
    if dados:
        print("Jogador Encontrado")
        print("PUUID: ", dados["puuid"])
        puuid = dados["puuid"]
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{quote(puuid)}/ids"
        response = requests.get(url, params=params, headers={"X-Riot-Token": API_KEY})
        dados = response.json()
        if(dados):
            return dados
def salvar_dados():
    dados = buscar_partidas("THE TARV", "YONCE")
    with open("data/raw/match_ids.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def ler_dados():
    with open("data/raw/match_ids.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

def partida():
    dados = ler_dados()
    #for i in dados:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{quote(dados[0])}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})
    dados_partida = response.json()
    print (dados_partida["metadata"]["matchId"])
    data = dados_partida["info"]["gameStartTimestamp"]
    fuso_br = timezone(timedelta(hours=-3))
    data = datetime.fromtimestamp(data / 1000, tz=fuso_br)
    print(data.strftime("%d/%m/%Y %H:%M:%S"))
    print (dados_partida["info"]["gameDuration"])
    print(dados_partida["info"]["gameMode"])
partida()