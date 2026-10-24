# Construindo o Clima em Foco

Este roteiro acompanha a construção de uma aplicação pequena para praticar Python, Flask, formulários HTML e consumo de API. O código do projeto não contém comentários; este documento explica cada etapa.

## Estrutura

```text
ConsumirApi/
├── backend/
│   └── app.py
├── frontend/
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── estilo.css
├── docs/
│   └── passo-a-passo.md
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

O backend fica em `backend/app.py`. A página HTML e o CSS ficam em `frontend/`. O Flask conecta as duas partes: recebe os formulários, conversa com a API e envia os resultados para a página.

## Dicionário divertido do código

Os nomes do projeto estão em português para que cada parte conte o que faz. Pense no backend como uma equipe de exploradores:

| Nome no código | O que faz | Uma imagem para lembrar |
| --- | --- | --- |
| `obter_chave_de_acesso` | Lê a chave guardada no `.env`. | Pega o crachá que abre a porta da API. |
| `buscar_opcoes_de_localidade` | Procura lugares com o nome digitado. | Consulta um atlas e traz cidades parecidas. |
| `filtrar_localidades_repetidas` | Mantém apenas uma opção para cada cidade, estado e país. | Tira cópias iguais da lista de destinos. |
| `consultar_clima_por_coordenadas` | Busca o tempo de latitude e longitude escolhidas. | Chama o repórter do tempo para um ponto exato do mapa. |
| `explicar_erro_da_api` | Transforma falhas técnicas em mensagens mais claras. | Traduz o recado complicado do robô. |
| `mostrar_pagina_inicial` | Mostra a busca e as cidades encontradas. | Abre o balcão de atendimento. |
| `mostrar_clima` | Recebe a cidade escolhida e exibe o clima. | Entrega a previsão para quem escolheu o destino. |
| `gerenciar_cidades_favoritas` | Responde a pedidos GET e POST da API própria. | Cuida da pequena lista de cidades da turma. |
| `cidade_pesquisada` | Guarda o texto que a pessoa digitou. | É o destino escrito no bilhete de viagem. |
| `opcoes_de_localidade` | Guarda os lugares encontrados pela busca. | É a lista de destinos possíveis no mapa. |
| `latitude` e `longitude` | Identificam a posição de um lugar. | São o endereço GPS da cidade. |
| `dados_do_clima` | Guarda temperatura, umidade, vento e descrição. | É o boletim do tempo recém-chegado. |

Algumas palavras continuam em inglês porque são nomes oficiais do Flask, do Requests ou dos campos enviados pela OpenWeather, como `Flask`, `requests`, `name`, `country`, `lat` e `lon`. Mantê-las iguais ao material oficial facilita encontrar ajuda e ler a resposta original da API.

## 1. Preparar o ambiente

Abra o terminal na pasta do projeto e crie um ambiente virtual:

```powershell
python -m venv .venv
```

Ative-o no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale Flask, Requests e python-dotenv:

```powershell
pip install -r requirements.txt
```

Flask cria o servidor e as rotas. Requests envia chamadas HTTP. python-dotenv lê a chave guardada no arquivo `.env`.

## 2. Configurar a chave da API

Crie uma conta na OpenWeather e gere uma chave para a API. Faça uma cópia de `.env.example` com o nome `.env` e substitua o texto de exemplo:

```text
OPENWEATHER_KEY=sua_chave_real
```

O arquivo `.env` não deve ser compartilhado nem enviado ao Git. Cada aluno pode usar sua própria chave ou a turma pode executar o projeto em um ambiente preparado pelo professor.

## 3. Iniciar o servidor Flask

No terminal, execute:

```powershell
python backend/app.py
```

Abra `http://127.0.0.1:5000` no navegador. A rota `/` exibe o formulário. Quando o formulário é enviado, o navegador faz uma requisição GET com o nome da cidade e o país.

## 4. Buscar localidades correspondentes

Uma cidade pode ter o mesmo nome que outras cidades. Por isso, o backend primeiro consulta a Geocoding API da OpenWeather, em vez de pedir o clima diretamente pelo nome.

O backend envia o nome digitado, o país escolhido e o limite de resultados. A resposta é JSON. Cada correspondência pode incluir nome, país, estado, latitude e longitude. A API retorna até cinco resultados por busca.

Na página, cada resultado mostra a cidade e sua região. A pessoa escolhe a opção correta pelo estado e país. Alguns resultados podem não conter estado; nesses casos, a página avisa que a informação não foi fornecida.

## 5. Consultar o clima pela localização escolhida

Ao selecionar uma opção, o navegador envia latitude e longitude ao backend por uma requisição POST. O backend consulta o clima usando essas coordenadas e recebe outro JSON.

O projeto mostra temperatura, sensação térmica, umidade, vento e descrição do tempo. Usar coordenadas após a escolha evita que a API faça uma nova busca ambígua pelo nome da cidade.

## 6. Entender a separação entre backend e front

`backend/app.py` contém as rotas e a comunicação com a API externa. `frontend/templates/index.html` contém a estrutura da página. `frontend/static/estilo.css` controla cores, espaçamento e adaptação a telas pequenas.

O formulário funciona sem JavaScript: HTML envia os dados ao Flask, e o Flask devolve a página preenchida com resultados ou uma mensagem de erro.

## 7. Criar uma API própria como extensão

O mesmo backend disponibiliza `/api/favoritos` para praticar uma API REST simples.

- `GET /api/favoritos` retorna a lista de cidades favoritas em JSON.
- `POST /api/favoritos` recebe JSON com `cidade`, `estado` e `pais`, e adiciona a cidade à lista.

Exemplo de corpo para POST:

```json
{
  "cidade": "Campinas",
  "estado": "São Paulo",
  "pais": "Brasil"
}
```

Os dados ficam em memória e são apagados quando o servidor é reiniciado. Isso permite praticar métodos HTTP e respostas JSON sem instalar banco de dados. Persistência com SQLite pode ser um exercício posterior.

## 8. Sugestão de sequência para a aula

1. Abrir uma resposta JSON e identificar chaves e valores.
2. Explicar requisição, resposta, URL, parâmetros e método GET.
3. Enviar uma consulta para a API externa usando Requests.
4. Exibir os resultados numa página com Flask e HTML.
5. Comparar localidades com o mesmo nome e escolher uma delas.
6. Explicar POST e testar a API de favoritos enviando JSON.
7. Alterar o CSS e observar a página em tela larga e estreita.

## 9. Publicar no Render

O Render mantém a aplicação disponível na internet. Para uma aplicação Flask, ele instala as dependências e inicia o servidor de produção com Gunicorn.

### Preparar o projeto

Confirme que o projeto está no GitHub e que `requirements.txt` inclui Gunicorn. O arquivo `.gitignore` protege `.env`, então a chave pessoal não deve ser enviada ao repositório.

Quando fizer novas alterações, envie-as para a branch conectada ao Render:

```powershell
git add .
git commit -m "Descreva a alteração"
git push origin main
```

### Criar o serviço

1. Entre no painel do Render e escolha **New > Web Service**.
2. Conecte sua conta do GitHub e selecione o repositório `climaTempo`.
3. Configure os campos:

| Campo | Valor |
| --- | --- |
| Runtime | Python 3 |
| Branch | `main` |
| Root Directory | Deixe vazio |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT backend.app:aplicativo` |

4. Na seção **Environment Variables**, adicione:

| Nome | Valor |
| --- | --- |
| `OPENWEATHER_KEY` | Sua chave da OpenWeather |

5. Escolha o plano disponível para a aula e clique em **Create Web Service**.
6. Acompanhe a instalação e a inicialização na aba **Logs**. Quando o serviço estiver pronto, abra o endereço `onrender.com` exibido pelo Render.

O Render define a variável `$PORT`; o Gunicorn usa essa porta e aceita conexões externas. Cada novo `git push` para a branch conectada pode iniciar uma nova publicação automática. A configuração de `OPENWEATHER_KEY` fica salva no painel e não precisa entrar no Git.

## Referências

- [Geocoding API](https://openweathermap.org/api/geocoding-api)
- [Current Weather API](https://openweathermap.org/api/current)
- [Guia oficial do Render para Flask](https://render.com/docs/deploy-flask)
- [Variáveis de ambiente no Render](https://render.com/docs/configure-environment-variables)
