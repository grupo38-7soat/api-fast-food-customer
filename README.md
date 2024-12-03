# API Fast Food Customer

Este é um projeto de aplicação desenvolvido em Python 3.12. Ele utiliza a biblioteca `loguru` para logging e inclui testes unitários com `pytest` e `pytest-cov`.

## Objetivo

Esta aplicação tem como objetivo cadastrar os usuários da aplicação dentro de um DynamoDB da AWS, realizando operações de CRUD (Create, Read, Update, Delete).

## Requisitos

- Python 3.12
- pip

## Instalação

Para instalar as dependências necessárias, execute o seguinte comando apontando para o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
````    

##  Executando a Aplicação
Para executar a aplicação, utilize o comando:
```bash
python src/app.py
````    

A aplicação possui um Swagger disponível na porta 3000. Para acessar, basta rodar o código e acessar http://localhost:3000/swagger/.


##  Testes Unitários
Para rodar os testes unitarios é preciso ter o pytest e pytest-cov instalados, caso não tenha, pode instalar com o comando abaixo
````    
pip install pytest
pip install pytest-cov
````

Para Analisar o codigo local e verificar a porcentagem de cobertura em cada arquivo, pode rodar o comando abaixo
````
coverage3 run -m pytest -v --cov=. 
````

Comando para rodar o covarage, geracao do arquivo covarerage.xml e o sonar-scanner
````
coverage3 run -m pytest -v --cov=. --cov-report xml:coverage.xml
sonar-scanner
````

##  Integração e Deploy
Esta aplicação conta com a integração do GitHub Actions, permitindo fazer o deploy da aplicação diretamente na AWS, utilizando os arquivos Kubernetes presentes na pasta eks. Para subir a imagem, estamos utilizando o AWS ECR.


Caso alguma alteração no projeto seja feita, é de estrema importancia atualizar as dependencias do projeto, e para isso pode usar o seguinte comando
````
pip freeze > requirements.txt
````


