from unittest.mock import Mock
from app_server import app

app_instance = app()
app_mock = Mock()

app_mock = app_instance # Присваиваем mock-версию метода log_in

app_mock.log_in('Eve', '1234')
print(app_mock.log_in.calls())