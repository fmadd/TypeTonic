import json
import unittest
from unittest.mock import patch, Mock
from app_server import app_server


class app_test(unittest.TestCase):
    @patch("http.client.HTTPConnection.request")
    @patch("http.client.HTTPConnection.getresponse")
    @patch("http.client.HTTPConnection.close")
    def test_login_1(self, mock_close, mock_getresponse, mock_request):
        test_instance = app_server()

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = "test_token".encode("utf-8")
        mock_getresponse.return_value = mock_response

        test_instance.log_in("test_login", "test_password")

        self.assertEqual(test_instance.token, "test_token")
        mock_close.assert_called_once()

    @patch("http.client.HTTPConnection.request")
    @patch("http.client.HTTPConnection.getresponse")
    @patch("http.client.HTTPConnection.close")
    def test_invalid_login_1(self, mock_close, mock_getresponse, mock_request):
        test_instance = app_server()

        mock_response = Mock()
        mock_response.status = 401
        mock_getresponse.return_value = mock_response

        with self.assertRaises(Exception) as context:
            test_instance.log_in("test_login", "test_password")

        self.assertEqual(str(context.exception), "Неверный логин или пароль")
        mock_close.assert_called_once()

    @patch("app_server.re.match")
    def test_valid_password(self, mock_match):
        test_instance = app_server()

        mock_match.return_value = True

        test_instance.valid_password("ValidPassword123")

        mock_match.assert_called_once_with(
            r"^[а-яА-Яa-zA-Z0-9]{6,}$", "ValidPassword123"
        )

    @patch("app_server.re.match")
    def test_invalid_password(self, mock_match):
        test_instance = app_server()

        mock_match.return_value = None

        self.assertEqual(test_instance.valid_password("invalid"), False)
        mock_match.assert_called_once_with(r"^[а-яА-Яa-zA-Z0-9]{6,}$", "invalid")

    @patch("http.client.HTTPConnection.request")
    @patch("http.client.HTTPConnection.close")
    def test_del_user(self, mock_close, mock_request):
        test_instance = app_server()
        test_instance.token = "test_token"

        test_instance.del_user()

        mock_request.assert_called_once_with(
            "POST", "/del_user", headers={"Authorization": "test_token"}
        )
        mock_close.assert_called_once()

    def setUp(self):
        self.app_server = app_server()
        self.app_server.token = 'token'
        self.mock_http_response = Mock()
        self.mock_http_response.read.return_value = "[{'A':4, 'E':3, 'I':7}]".encode()
        self.mock_http_connection = Mock()
        self.mock_http_connection.getresponse.return_value = self.mock_http_response

    @patch('app_server.http.client.HTTPConnection')
    @patch('app_server.get_ip')
    def test_get_user_letter(self, mock_get_ip, mock_http_connection):
        mock_get_ip.return_value = '127.0.0.1'
        mock_http_connection.return_value = self.mock_http_connection

        result = self.app_server.get_user_letter()

        self.assertIsInstance(result, str)
        self.assertIn("A", result)
        mock_http_connection.assert_called_with('127.0.0.1', 2000)
        self.mock_http_connection.request.assert_called_once_with(
            "GET", "/top_user_letter", headers={
                "Content-type": "application/json",
                "Authorization": "token"
            }
        )

        self.mock_http_connection.close.assert_called_once()



if __name__ == "__main__":
    unittest.main()
