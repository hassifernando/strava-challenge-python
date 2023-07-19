# Strava Challenge Python

  Este projeto é um conjunto de testes automatizados para a integração com a API do Strava, uma plataforma de atividades físicas. Ele realiza testes em diversos endpoints da API     para garantir o correto funcionamento e integração com o sistema.
  
  Os testes abrangem funcionalidades como autenticação, recuperação de informações do perfil do atleta, criação de atividades e outras operações relacionadas.
  
  O objetivo deste projeto é aplicar e aprimorar o conhecimento em Python, além de utilizar os recursos avançados do Pytest para testar de forma abrangente os diversos endpoints     da API.

## Funcionalidades
- Autenticação e autorização do usuário
- Recuperação de informações do perfil do atleta
- Criação e gerenciamento de atividades
- Testes de segurança e confidencialidade
- Verificação da estrutura e formatos de resposta da API
  
## Requisitos

- Python: 3.11.4
- pipenv: version 2023.7.11

## Instalação

Clone este repositório em sua máquina local:

```shell
git clone https://github.com/hassifernando/strava-challenge-python.git
```

Acesse o diretório do projeto:
```
cd strava-challenge-python
```
Instale as dependências necessárias:
```
pipenv install
```

## Executando os Testes

Para executar os testes automatizados, siga os passos abaixo:

1. Acesse o diretório do projeto:
```
cd strava-challenge-python
```

2.Execute o seguinte comando para rodar todos os testes:
```
pytest
```
3.Caso prefira executar algum teste específico:
```
 pytest -k test_create_activity tests/test_activities.py
```

