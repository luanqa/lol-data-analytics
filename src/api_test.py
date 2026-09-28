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
    if response.status_code == 200:
        return response.json()

def buscar_partidas(nick, tag):
    dados = buscar_dadosRiot(nick, tag)
    params = {"count": 10}
    if dados:
        puuid = dados["puuid"]
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{quote(puuid)}/ids"
        response = requests.get(url, params=params, headers={"X-Riot-Token": API_KEY})
        partidas = response.json()
        if(partidas):
            return partidas,dados
        
def salvar_dados():
    dados = buscar_partidas("THE TARV", "YONCE")
    dados_jogador = []
    for i in dados[1]:
       dados_jogador.append(dados[1][i])
    with open("data/raw/match_ids.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados[0], arquivo, indent=4, ensure_ascii=False)
    with open("data/raw/jogador.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_jogador, arquivo, indent=4, ensure_ascii=False)

def ler_dados_partida():
    with open("data/raw/match_ids.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

def ler_dados_jogador():
    with open("data/raw/jogador.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

salvar_dados()

def partida():
    dados = ler_dados_partida()
    dados_jogador = ler_dados_jogador()


    #for i in dados:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{quote(dados[0])}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})
    dados_partida = response.json()
    #print (dados_partida["metadata"]["matchId"])
    data = dados_partida["info"]["gameStartTimestamp"]
    fuso_br = timezone(timedelta(hours=-3))
    data = datetime.fromtimestamp(data / 1000, tz=fuso_br)
    #print(data.strftime("%d/%m/%Y %H:%M:%S"))
    #print (dados_partida["info"]["gameDuration"])
    #print(dados_partida["info"]["gameMode"])


    #jogador
    puuid         = dados_jogador[0]
    nome_jogador  = dados_jogador[1]
    tag_jogador   = dados_jogador[2]

    match_id      = dados_partida["metadata"]["matchId"]
    data_partida  = datetime.fromtimestamp(dados_partida["info"]["gameStartTimestamp"] / 1000, tz=fuso_br)
    duracao       = dados_partida["info"]["gameDuration"]
    kill = 0
    death = 0
    assists = 0
    cs = 0
    ouro = 0
    vitoria = False
    #champ
    for participante in dados_partida["info"]["participants"]:
        if(participante["riotIdGameName"] == nome_jogador):
            champ         = participante["championName"]
            kill          = participante["kills"]
            death         = participante["deaths"]
            assists       = participante["assists"]
            cs            = (participante["totalMinionsKilled"]) + (participante["neutralMinionsKilled"])
            ouro          = participante["goldEarned"]
            vitoria       = participante["win"]    

    chaves_jogador           = ['puuid', 'nome', 'tag'] #jogador
    valores_jogador          = [puuid, nome_jogador, tag_jogador]
    dicionario_jogador       = dict(zip(chaves_jogador, valores_jogador))
    
    chaves_partida           = ['match_id','data_partida', 'duracao', 'modo', 'path'] #partida
    valores_partida          = [match_id, data_partida, duracao]
    dicionario_partida       = dict(zip(chaves_partida, valores_partida))

    #'jogador_id', 'partida_id', 'campeao_id'
    chaves_participante      = ['kills', 'deaths', 'assists', 'cs', 'ouro', 'vitoria'] #participante
    valores_participante     = [kill, death, assists, cs, ouro, vitoria]
    dicionario_participante  = dict(zip(chaves_participante, valores_participante))

    return(dicionario_jogador, dicionario_partida, dicionario_participante, champ)

partida()