import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DA_INTERFACE = PASTA_PROJETO / "frontend"
load_dotenv(PASTA_PROJETO / ".env")

aplicativo = Flask(
    __name__,
    template_folder=PASTA_DA_INTERFACE / "templates",
    static_folder=PASTA_DA_INTERFACE / "static",
    static_url_path="/static",
)

URL_BUSCA_LOCALIDADES = "https://api.openweathermap.org/geo/1.0/direct"
URL_CLIMA_ATUAL = "https://api.openweathermap.org/data/2.5/weather"
PAISES_DISPONIVEIS = {
    "ALL": "Qualquer país",
    "BR": "Brasil",
    "US": "Estados Unidos",
    "PT": "Portugal",
    "AR": "Argentina",
    "CL": "Chile",
}
CIDADES_FAVORITAS = []


def obter_chave_de_acesso():
    chave_de_acesso = os.getenv("OPENWEATHER_KEY")
    if not chave_de_acesso or chave_de_acesso == "sua_chave_aqui":
        raise ValueError("Configure sua chave da OpenWeather no arquivo .env.")
    return chave_de_acesso


def buscar_opcoes_de_localidade(nome_da_cidade, codigo_do_pais):
    nome_para_busca = nome_da_cidade if codigo_do_pais == "ALL" else f"{nome_da_cidade},{codigo_do_pais}"
    resposta_da_api = requests.get(
        URL_BUSCA_LOCALIDADES,
        params={"q": nome_para_busca, "limit": 5, "appid": obter_chave_de_acesso()},
        timeout=10,
    )
    resposta_da_api.raise_for_status()
    localidades_recebidas = resposta_da_api.json()
    return filtrar_localidades_repetidas(localidades_recebidas)


def filtrar_localidades_repetidas(localidades_recebidas):
    localidades_sem_repeticao = []
    identificadores_encontrados = set()

    for localidade in localidades_recebidas:
        identificador = (
            str(localidade.get("name") or "").strip().casefold(),
            str(localidade.get("state") or "").strip().casefold(),
            str(localidade.get("country") or "").strip().upper(),
        )
        if identificador not in identificadores_encontrados:
            identificadores_encontrados.add(identificador)
            localidades_sem_repeticao.append(localidade)

    return localidades_sem_repeticao


def consultar_clima_por_coordenadas(latitude, longitude):
    resposta_da_api = requests.get(
        URL_CLIMA_ATUAL,
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": obter_chave_de_acesso(),
            "units": "metric",
            "lang": "pt_br",
        },
        timeout=10,
    )
    resposta_da_api.raise_for_status()
    dados_recebidos = resposta_da_api.json()
    return {
        "cidade": dados_recebidos.get("name", "Localidade"),
        "pais": dados_recebidos.get("sys", {}).get("country", ""),
        "temperatura": round(dados_recebidos["main"]["temp"]),
        "sensacao": round(dados_recebidos["main"]["feels_like"]),
        "umidade": dados_recebidos["main"]["humidity"],
        "descricao": dados_recebidos["weather"][0]["description"].capitalize(),
        "vento": dados_recebidos.get("wind", {}).get("speed", 0),
    }


def explicar_erro_da_api(erro_recebido):
    if isinstance(erro_recebido, requests.HTTPError) and erro_recebido.response is not None:
        if erro_recebido.response.status_code == 401:
            return "A chave da OpenWeather não foi aceita. Confira o arquivo .env."
    if isinstance(erro_recebido, requests.RequestException):
        return "Não foi possível acessar a API. Confira sua conexão e tente novamente."
    return str(erro_recebido)


@aplicativo.get("/")
def mostrar_pagina_inicial():
    nome_da_cidade = request.args.get("cidade", "").strip()
    codigo_do_pais = request.args.get("pais", "BR")
    opcoes_de_localidade = []
    mensagem_de_erro = None

    if codigo_do_pais not in PAISES_DISPONIVEIS:
        codigo_do_pais = "BR"

    if nome_da_cidade:
        try:
            opcoes_de_localidade = buscar_opcoes_de_localidade(nome_da_cidade, codigo_do_pais)
            if not opcoes_de_localidade:
                mensagem_de_erro = "Nenhuma localidade encontrada. Confira o nome e tente novamente."
        except (requests.RequestException, ValueError) as erro_recebido:
            mensagem_de_erro = explicar_erro_da_api(erro_recebido)

    return render_template(
        "index.html",
        cidade_pesquisada=nome_da_cidade,
        pais_escolhido=codigo_do_pais,
        lista_de_paises=PAISES_DISPONIVEIS,
        opcoes_de_localidade=opcoes_de_localidade,
        dados_do_clima=None,
        mensagem_de_erro=mensagem_de_erro,
    )


@aplicativo.post("/clima")
def mostrar_clima():
    try:
        latitude = float(request.form.get("latitude", ""))
        longitude = float(request.form.get("longitude", ""))
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError("Selecione uma localidade válida.")
        dados_do_clima = consultar_clima_por_coordenadas(latitude, longitude)
        mensagem_de_erro = None
    except (ValueError, KeyError, IndexError, requests.RequestException) as erro_recebido:
        dados_do_clima = None
        mensagem_de_erro = explicar_erro_da_api(erro_recebido)

    return render_template(
        "index.html",
        cidade_pesquisada="",
        pais_escolhido="BR",
        lista_de_paises=PAISES_DISPONIVEIS,
        opcoes_de_localidade=[],
        dados_do_clima=dados_do_clima,
        mensagem_de_erro=mensagem_de_erro,
    )


@aplicativo.route("/api/favoritos", methods=["GET", "POST"])
def gerenciar_cidades_favoritas():
    if request.method == "GET":
        return jsonify(favoritos=CIDADES_FAVORITAS)

    dados_recebidos = request.get_json(silent=True) or {}
    nome_da_cidade = str(dados_recebidos.get("cidade", "")).strip()
    if not nome_da_cidade:
        return jsonify(erro="Informe o nome da cidade."), 400

    cidade_favorita = {
        "cidade": nome_da_cidade,
        "estado": str(dados_recebidos.get("estado", "")).strip(),
        "pais": str(dados_recebidos.get("pais", "")).strip(),
    }
    if cidade_favorita not in CIDADES_FAVORITAS:
        CIDADES_FAVORITAS.append(cidade_favorita)
    return jsonify(favorito=cidade_favorita), 201


if __name__ == "__main__":
    aplicativo.run(debug=True)
