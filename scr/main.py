import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup


def digitos_numericos(texto):
    return ''.join([posicao for posicao in texto if posicao.isdigit()])


def cpf_valido(cpf):
    if not cpf or not isinstance(cpf, str):
        return False

    cpf = digitos_numericos(cpf)

    if len(cpf) != 11:
        return False

    relacao_digito_peso = zip([int(digito) for digito in cpf[0:-2]], [peso for peso in range(10, 1, -1)])
    resto_soma = sum([digito * peso for digito, peso in relacao_digito_peso]) % 11
    digito_esperado = 11 - resto_soma if resto_soma >= 2 else 0
    if cpf[-2] != str(digito_esperado):
        return False

    relacao_digito_peso = zip([int(digito) for digito in cpf[0:-1]], [peso for peso in range(11, 1, -1)])
    resto_soma = sum([digito * peso for digito, peso in relacao_digito_peso]) % 11
    digito_esperado = 11 - resto_soma if resto_soma >= 2 else 0
    if cpf[-1] != str(digito_esperado):
        return False
    return True

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
            'mensagem': 'NADA CONSTA',
            'inabilitado': [],
        }
        
        consulta = {
            'nome_pesquisado': nome.upper(),
            'cpf_pesquisado': cpf,
            'data': data
        }
        
        if not cpf_valido(cpf):
            data['mensagem'] = 'CPF INVÁLIDO'
            return data
        else:
            qgi_data = self.get_qgi_data()
    
            for linha_quadro in qgi_data:
                if linha_quadro['intimado'] == nome.upper():
                    if linha_quadro['cpf'][3:9] == cpf[3:9]:
                        linha_quadro['cpf_corresponde'] = True
                        linha_quadro['mensagem'] = 'O CPF consultado corresponde ao listado.'
                    else:
                        linha_quadro['cpf_corresponde'] = False
                        linha_quadro['mensagem'] = 'O CPF consultado não corresponde ao listado.'
                    data['inabilitado'] = linha_quadro
                    data['mensagem'] = 'NOME LISTADO'
    
            consulta['data'] = data

        return consulta


nome = 'NOME PESQUISADO'
cpf_pesquisado = 'xxx0000000xx'

service_qgi = QuadroGeralInabilitadosService()
print(service_qgi.busca_inabilitados(nome, cpf_pesquisado))
