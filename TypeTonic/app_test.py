import unittest
from unittest.mock import patch, Mock
from app_server import app_server


class app_test(unittest.TestCase):

    @patch('http.client.HTTPConnection.request')
    @patch('http.client.HTTPConnection.getresponse')
    @patch('http.client.HTTPConnection.close')
    def test_login_1(self, mock_close, mock_getresponse, mock_request):
        test_instance = app_server()

        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = 'test_token'.encode('utf-8')
        mock_getresponse.return_value = mock_response


        test_instance.log_in('test_login', 'test_password')

        self.assertEqual(test_instance.token, 'test_token')
        mock_close.assert_called_once()

    @patch('http.client.HTTPConnection.request')
    @patch('http.client.HTTPConnection.getresponse')
    @patch('http.client.HTTPConnection.close')
    def test_too_many_attempts_1(self, mock_close, mock_getresponse, mock_request):
        test_instance = app_server()

        mock_response = Mock()
        mock_response.status = 402
        mock_getresponse.return_value = mock_response

        with self.assertRaises(Exception) as context:
            test_instance.log_in('test_login', 'test_password')

        self.assertEqual(str(context.exception), "Слишком много попыток ввода логина")
        mock_close.assert_called_once()

    @patch('http.client.HTTPConnection.request')
    @patch('http.client.HTTPConnection.getresponse')
    @patch('http.client.HTTPConnection.close')
    def test_invalid_login_1(self, mock_close, mock_getresponse, mock_request):
        test_instance = app_server()


        mock_response = Mock()
        mock_response.status = 401
        mock_getresponse.return_value = mock_response

        with self.assertRaises(Exception) as context:
            test_instance.log_in('test_login', 'test_password')

        self.assertEqual(str(context.exception), "Неверный логин или пароль")
        mock_close.assert_called_once()

    @patch('app_server.re.match')
    def test_valid_password(self, mock_match):

        test_instance = app_server()

        mock_match.return_value = True

        test_instance.valid_password('ValidPassword123')

        mock_match.assert_called_once_with(r'^[а-яА-Яa-zA-Z0-9]{6,}$', 'ValidPassword123')

    @patch('app_server.re.match')
    def test_invalid_password(self, mock_match):
        test_instance = app_server()

        mock_match.return_value = None

        self.assertEqual(test_instance.valid_password('invalidpassword'), False)
        mock_match.assert_called_once_with(r'^[а-яА-Яa-zA-Z0-9]{6,}$', 'invalidpassword')

    @patch('http.client.HTTPConnection.request')
    @patch('http.client.HTTPConnection.close')
    def test_del_user(self, mock_close, mock_request):
        test_instance = app_server()
        test_instance.token = 'test_token'

        test_instance.del_user()

        mock_request.assert_called_once_with(
            "POST", "/del_user", headers={'Authorization': 'test_token'}
        )
        mock_close.assert_called_once()

    '''@patch('http.client.HTTPConnection.request')
    def test_reg_user(self, mock_request):
        test_instance = app_server()

        # Создаем имитацию объекта HTTPResponse
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = 'test_token'.encode('utf-8')

        # Настроим возвращаемое значение mock_request для возврата mock_response
        mock_request.return_value = mock_response

        # Вызываем функцию
        test_instance.reg_user('test_login', 'test_password')

        # Проверяем, что HTTP-запрос был отправлен с правильными параметрами
        mock_request.assert_called_once_with(
            "POST", "/reg", '{"login": "test_login", "pass": "test_password"}',
            headers={'Content-type': 'application/json'}
        )
        print(test_instance.token)
        # Проверяем, что функция log_in была вызвана с правильными параметрами
        self.assertEqual(test_instance.token, 'test_token')'''

if __name__ == '__main__':
    unittest.main()
