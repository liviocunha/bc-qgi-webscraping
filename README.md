# Web scraping - Quadro Geral de Inabilitados (QGI)
Projeto tem como finalidade realizar a "raspagem" de dados do Quadro Geral de Inabilitados disponível no site do Banco Central do Brasil.
Possibilitando a realização de consultas aos nomes listados no quadro.

## Este projeto foi feito com:
* Python 3.8.0
* LXML 4.6.3
* Beautiful Soup 4.9.3
* Requests 2.25.1
* Argparse 1.4.0
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
## Executando o Script
O script é executado na linha de comando e possui dois parâmetros:
- [--nome]: argumento obrigatório onde deve-se informar o nome completo.
- [--cpf]: argumento opcional para informar o cpf da pessoa consultada.
    - *Obs.: O CPF no QGI está ofuscado, portanto é feito um match parcial: xxx000000xx*

Exemplo de consulta:      
        
      python3 scr/main.py --nome "EXEMPLO DE NOME PESQUISADO" --cpf "00000000000"

Exemplo retorno nome listado:
```
{
    "cpf_pesquisado": "00000000000",
    "data": {
        "inabilitado": {
            "cpf": "xxx000000xx",
            "cpf_corresponde": false,
            "data_publicacao": "15/06/2018",
            "intimado": "EXEMPLO DE NOME PESQUISADO",
            "mensagem": "O CPF consultado corresponde ao listado.",
            "penalidade": "INABILITAÇÃO",
            "prazo(anos)": "4",
            "prazo_final_penalidade": "15/06/2022"
        },
        "mensagem": "NOME LISTADO"
    },
    "nome_pesquisado": "EXEMPLO DE NOME PESQUISADO"
}
```
Exemplo retorno nome não listado:
```
{
    "cpf_pesquisado": "00000000000",
    "data": {
        "inabilitado": [],
        "mensagem": "NADA CONSTA"
    },
    "nome_pesquisado": "EXEMPLO DE NOME PESQUISADO"
}
```
Exemplo retorno CPF inválido:
```
{
    "inabilitado": [],
    "mensagem": "CPF INVÁLIDO"
}
```