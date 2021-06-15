import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup


class QuadroGeralInabilitadosService:
    URL = 'https://www3.bcb.gov.br/gepad/publicobcb/qgi/relatorioInternet'

    def request_url(self, url: str = URL):
        return requests.get(url, timeout=10)

    def get_html_content(self):
        return self.request_url().text

    def get_soup_lxml(self):
        return BeautifulSoup(self.get_html_content(), 'lxml')

    def get_qgi_data(self):
        qgi_table = self.get_soup_lxml().find("table")
        qgi_table_data = qgi_table.tbody.find_all("tr")

        qgi_data = []

        for td in qgi_table_data:
            intimacao = td.get_text().split('\n\n')
            intimacao_data = {
                'cpf': intimacao[2],
                'intimado': intimacao[1],
                'penalidade': intimacao[3],
                'data_publicacao': intimacao[5],
                'prazo_final_penalidade': intimacao[6],
                'prazo(anos)': intimacao[4],
            }

            qgi_data.append(intimacao_data)
        return qgi_data

    def busca_inabilitados(self, nome: str, cpf: str):
        data = {
            'status': 'NADA CONSTA',
            'inabilitado': [],
        }

        qgi_data = self.get_qgi_data()

        for linha_quadro in qgi_data:
            if linha_quadro['intimado'] == nome.upper():
                if linha_quadro['cpf'] == cpf:
                    linha_quadro['cpf_corresponde'] = True
                    linha_quadro['mensagem'] = 'O CPF consultado corresponde ao listado.'
                else:
                    linha_quadro['cpf_corresponde'] = False
                    linha_quadro['mensagem'] = 'O CPF consultado não corresponde ao listado.'
                data['inabilitado'] = linha_quadro
                data['status'] = 'OK'

        consulta = {
            'nome_pesquisado': nome.upper(),
            'cpf_pesquisado': cpf,
            'data': data
        }

        return consulta


nome = 'NOME PESQUISADO'
cpf = 'xxx000000xx'

service_qgi = QuadroGeralInabilitadosService()
print(service_qgi.busca_inabilitados(nome, cpf))
