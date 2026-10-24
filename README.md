# Clima em Foco

Aplicação didática em Flask para consultar o clima de uma cidade usando a OpenWeather. A busca apresenta localidades com o mesmo nome para que a pessoa escolha a combinação correta de cidade, estado e país.

## Executar

1. Instale o Python.
2. Crie e ative um ambiente virtual.
3. Instale as dependências com `pip install -r requirements.txt`.
4. Copie `.env.example` para `.env` e informe sua chave em `OPENWEATHER_KEY`.
5. Inicie com `python backend/app.py` e abra `http://127.0.0.1:5000`.

O roteiro completo está em [docs/passo-a-passo.md](docs/passo-a-passo.md).

## Publicar no Render

O passo a passo de publicação está na seção **9. Publicar no Render** do roteiro. No painel do Render, configure `OPENWEATHER_KEY` como variável de ambiente. Não envie o arquivo `.env` ao GitHub.
