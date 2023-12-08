**Contexto:** Você é um cientista de dados no Santander e recebeu a tarefa de envolver seus clientes de maneira mais personalizada. Seu objetivo é usar o poder da IA Generativa para criar mensagens de marketing personalizadas que serão entregues a cada cliente.

**Condições do Problema:**

1. Você recebeu uma planilha simples, em formato CSV ('SDW2023.csv'), com uma lista de IDs de usuário do banco.
2. Seu trabalho é consumir o endpoint `GET https://sdw-2023-prd.up.railway.app/users/{id}` (API da Santander Dev Week 2023) para obter os dados de cada cliente.
3. Depois de obter os dados dos clientes, você vai usar a API do ChatGPT (OpenAI) para gerar uma mensagem de marketing personalizada para cada cliente. Essa mensagem deve enfatizar a importância dos investimentos.
4. Uma vez que a mensagem para cada cliente esteja pronta, você vai enviar essas informações de volta para a API, atualizando a lista de "news" de cada usuário usando o endpoint `PUT https://sdw-2023-prd.up.railway.app/users/{id}`.

# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

#|  ID  | Nome |  Número | Agên |L.Conta|     Cartão          |L. Cartão |
#|------|------|---------|------|-------|---------------------|----------|
#| 5963 | Luis | 13236-2 | 3010 |  800  | **** **** **** 4341 |    800   |
#| 5964 | Mary | 67472-4 | 3010 |  800  | **** **** **** 5444 |    800   |
#| 5965 | Juan | 34589-3 | 3010 |  800  | **** **** **** 4991 |    800   |
#| 5966 | Noel | 98584-5 | 3010 |  800  | **** **** **** 2315 |    800   |
#| 5967 | Sara | 74593-2 | 3010 |  800  | **** **** **** 8832 |    800   |



1. Extraia a lista de IDs de usuário a partir do arquivo CSV. Para cada ID, faça uma requisição GET para obter os dados do usuário correspondente.

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

2.

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

{
  "id": 5963,
  "name": "Luis",
  "account": {
    "id": 6313,
    "number": "13236-2",
    "agency": "3010",
    "balance": 0,
    "limit": 800
  },
  "card": {
    "id": 5796,
    "number": "**** **** **** 4341",
    "limit": 800
  },
  "features": [],
  "news": [
  ]
},
{
  "id": 5964,
  "name": "Mary",
  "account": {
    "id": 6314,
    "number": "67472-4",
    "agency": "3010",
    "balance": 0,
    "limit": 800
  },
  "card": {
    "id": 5797,
    "number": "**** **** **** 5444",
    "limit": 800
  },
  "features": [],
  "news": []
},
{
  "id": 5965,
  "name": "Juan",
  "account": {
    "id": 6315,
    "number": "34589-3",
    "agency": "3010",
    "balance": 0,
    "limit": 800
  },
  "card": {
    "id": 5798,
    "number": "**** **** **** 4991",
    "limit": 0
  },
  "features": [],
  "news": []
},
{
  "id": 5966,
  "name": "Noel",
  "account": {
    "id": 6316,
    "number": "98584-5",
    "agency": "3010",
    "balance": 0,
    "limit": 800
  },
  "card": {
    "id": 5799,
    "number": "**** **** **** 2315",
    "limit": 0
  },
  "features": [],
  "news": []
},
{
  "id": 5967,
  "name": "Sara",
  "account": {
    "id": 6317,
    "number": "74593-2",
    "agency": "3010",
    "balance": 0,
    "limit": 800
  },
  "card": {
    "id": 5800,
    "number": "**** **** **** 8832",
    "limit": 0
  },
  "features": [],
  "news": []
}

3.
Utilize a API do OpenAI GPT-4 para gerar uma mensagem de marketing personalizada para cada usuário.
!pip install openai

openai_api_key = '...'
import openai

openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

  4.
  Atualize a lista de "news" de cada usuário na API com a nova mensagem gerada.

  def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")

User Luis updated? True!
User Mary updated? True!
User Juan updated? True!
User Noel updated? True!
User Sara updated? True!

Resultado em https://sdw-2023-prd.up.railway.app/
Olá Luis, investir é essencial para aumentar sua riqueza financeira. Vamos començar?
Olá Mary, investir é crucial para crecimento financeiro pessoal e segurança a longo prazo. Vamos començar?
Juan, investir é garantir seu futuro financeiro. Comece hoje mesmo!
Noel, investir é garantir seu futuro! faça sue dinheiro trabalhar para você. #InvestirÉVencer
Sara, investir é expandir seu futuro financeiro. Não espere, comece hoje mesmo!