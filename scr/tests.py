import bs4
import unittest
from unittest.mock import patch
from scr.main import requests, QuadroGeralInabilitadosService


class TestScrapping(unittest.TestCase):
    def setUp(self):
        self.nome = 'NOME PESQUISADO'
        self.cpf = 'xxx000000xx'
        self.service_qgi = QuadroGeralInabilitadosService()
        self.URL_not_found = 'https://www.google.com/gepad/publicobcb/qgi/relatorioInternet'

    def test_request_url_success(self):
        response_url = self.service_qgi.request_url()
        self.assertEqual(response_url.status_code, 200)

    def test_request_url_not_found(self):
        response_url = self.service_qgi.request_url(self.URL_not_found)
        self.assertEqual(response_url.status_code, 404)

    @patch.object(requests, 'get', side_effect=requests.exceptions.Timeout)
    def test_mock_request_url_timeout(self, mock_request):
        with self.assertRaises(requests.exceptions.Timeout):
            self.service_qgi.request_url()

    def test_get_string_html_content(self):
        result = self.service_qgi.get_html_content()
        self.assertIs(type(result), str)

    def test_qgi_table_and_quantity(self):
        qgi_table = self.service_qgi.get_soup_lxml().find("table")
        qgi_table_data = qgi_table.tbody.find_all("tr")
        self.assertIsInstance(qgi_table, bs4.element.Tag)
        self.assertEqual(qgi_table_data.__len__(), 810)




