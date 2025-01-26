# Projeto Bank API

Este projeto é uma API para gerenciamento de usuários e transações bancárias.

## Tecnologias
![Python Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Postgres Badge](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Docker Badge](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Instalação

Para instalar o projeto, siga os passos abaixo:

1. Clone o repositório:
    ```sh
    git clone https://github.com/melgacoc/python_bank
    ```

2. Suba os containers Docker:
    ```sh
    docker-compose up --build
    ```

## Rodando os Testes

Para rodar os testes, execute o seguinte comando dentro do console do container:

```sh
python manage.py test bank.tests.controllers
```

# Documentação da API de Usuários

## Considerações

- As rotas de registro e login retornam um token que precisa ser passado nas demais requisições no headers.
- As rotas de deposito, transferência, deposito e consulta de histórico recuperam o usuário pelo token.

## Endpoints

### 1. Registro de Usuário

- **URL:** `/api/register/`
- **Método:** `POST`
- **Descrição:** Registra um novo usuário.
- **Parâmetros de Entrada:**
  - `username` (string): "claudio" - Sem espaços ou caracteres especiais
  - `password` (string): "12345678" - Minimo de 8 caracteres
  - `email` (string): "claudio@email.com" - Validação de email
  - `cpf` (string): "90887605001" - O CPF precisa ser válido
- **Respostas:**
  - `200 OK`: Usuário registrado com sucesso.
  - `400 Bad Request`: Dados inválidos ou usuário já existe.

### 2. Login de Usuário

- **URL:** `/api/login/`
- **Método:** `POST`
- **Descrição:** Realiza o login de um usuário.
- **Parâmetros de Entrada:**
  - `username` (string): "admin"
  - `password` (string): "admin"
- **Respostas:**
  - `200 OK`: Login bem-sucedido.
  - `401 Unauthorized`: Credenciais incorretas.

### 3. Consulta de Usuário

- **URL:** `/api/users/`
- **Método:** `GET`
- **Descrição:** Consulta os detalhes de um usuário específico.
- **Respostas:**
  - `200 OK`: Retorna os detalhes do usuário.

### 4. Consulta de Saldo

- **URL:** `/api/balance/`
- **Método:** `GET`
- **Descrição:** Consulta o saldo do usuário autenticado.
- **Respostas:**
  - `200 OK`: Retorna o saldo do usuário.

### 5. Listagem de Transações

- **URL:** `/api/transactions/`
- **Método:** `GET`
- **Descrição:** Lista as transações do usuário autenticado.
- **Parâmetros de Entrada Opcionais:**
  - `start_date` (string): Data de início no formato `YYYY-MM-DD`.
  - `end_date` (string): Data de término no formato `YYYY-MM-DD`.
- **Respostas:**
  - `200 OK`: Retorna a lista de transações do usuário.

### 6. Transferência de Fundos

- **URL:** `/api/transfer/`
- **Método:** `POST`
- **Descrição:** Transfere fundos para outro usuário.
- **Parâmetros de Entrada:**
  - `receiver` (string): "claudio".
  - `amount` (float): 100.10
- **Respostas:**
  - `200 OK`: Transferência bem-sucedida.
  - `400 Bad Request`: Saldo insuficiente ou dados inválidos.
  - `404 Not Found`: Receptor não encontrado.

### 7. Adição de Fundos

- **URL:** `/api/add-funds/`
- **Método:** `POST`
- **Descrição:** Adiciona fundos à conta do usuário autenticado.
- **Parâmetros de Entrada:**
  - `amount` (float): 1000
- **Respostas:**
  - `200 OK`: Fundos adicionados com sucesso.
