# Web scraping - Quadro Geral de Inabilitados (QGI)
Projeto tem como finalidade realizar a "raspagem" de dados do Quadro Geral de Inabilitados disponível no site do Banco Central do Brasil.
Possibilitando a realização de consultas aos nomes listados no quadro.

## Este projeto foi feito com:

* Python 3.8.0
* LXML 4.6.3
* Beautiful Soup 4.9.3
* Requests 2.25.1

## Como executar o projeto?
* Clone este repositório.
* Prepare o ambiente:
  * Crie virtualenv com Python 3.
  * Ative o virtualenv.
  * Instale as dependências do Python.

```
git clone https://github.com/liviocunha/bc-qgi-webscraping.git
cd bc-qgi-webscraping
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
