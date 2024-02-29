import unittest
from unittest.mock import patch
from io import StringIO
from final_GUI import WebsiteStatus
import requests

class TestWebsiteStatus(unittest.TestCase):
    def setUp(self):
        self.url = "http://example.com"
        self.website_status = WebsiteStatus(self.url)

    @patch('requests.get')
    def test_get_website_status_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200

        result = self.website_status.get_website_status()

        self.assertEqual(result, 200)

    @patch('requests.get', side_effect=requests.RequestException('Mocked error'))
    def test_get_website_status_exception(self, mock_get):
        result = self.website_status.get_website_status()

        self.assertIsNone(result)

    @patch('requests.head')
    def test_get_http_status_success(self, mock_head):
        mock_response = mock_head.return_value
        mock_response.status_code = 302

        result = self.website_status.get_http_status()

        self.assertEqual(result, 302)

    @patch('requests.head', side_effect=requests.RequestException('Mocked error'))
    def test_get_http_status_exception(self, mock_head):
        result = self.website_status.get_http_status()

        self.assertIsNone(result)

    @patch('requests.head')
    def test_get_last_modification_date_success(self, mock_head):
        mock_response = mock_head.return_value
        mock_response.headers = {'last-modified': 'Thu, 01 Jan 1970 00:00:00 GMT'}

        result = self.website_status.get_last_modification_date()

        self.assertEqual(result, 'Thu, 01 Jan 1970 00:00:00 GMT')

    @patch('requests.head', side_effect=requests.RequestException('Mocked error'))
    def test_get_last_modification_date_exception(self, mock_head):
        result = self.website_status.get_last_modification_date()

        self.assertIsNone(result)

    @patch('requests.head')
    @patch('ssl.create_default_context')
    @patch('socket.create_connection')
    def test_get_ssl_certificate_info_success(self, mock_create_connection, mock_context, mock_head):
        mock_response = mock_head.return_value
        mock_response.headers = {}

        mock_socket = mock_create_connection.return_value.__enter__.return_value
        mock_ssl_socket = mock_context.return_value.wrap_socket.return_value
        mock_ssl_socket.getpeercert.return_value = {'subject': ((('commonName', 'example.com'),),)}

        result = self.website_status.get_ssl_certificate_info()

        self.assertIsNotNone(result)

    @patch('requests.get')
    def test_get_all_links_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.content = '<a href="http://example.com/page1">Page 1</a>'

        result = self.website_status.get_all_links()

        self.assertEqual(result, ['http://example.com/page1'])

if __name__ == '__main__':
    unittest.main()
