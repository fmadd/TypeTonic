import unittest
from unittest.mock import Mock, MagicMock, patch
from main import PersonalCabinet, LoginPanel, TrainingModePanel, TrainingPanel
import tkinter as tk


class TestPersonalCabinet(unittest.TestCase):
    def setUp(self):
        self.app_mock = Mock()
        self.app_mock.account = {"nickname": "testuser"}

        self.app_mock.root = Mock(spec=tk.Tk)

        self.app_mock.root.withdraw = Mock()

        self.personal_cabinet = PersonalCabinet(self.app_mock)

    def test_init(self):
        self.assertEqual(self.personal_cabinet.nickname, "testuser")

        self.app_mock.root.title.assert_called_with("TypeTonic")

    def test_clear(self):
        child_mocks = [Mock(spec=tk.Widget) for _ in range(3)]
        self.app_mock.root.winfo_children.return_value = child_mocks

        self.personal_cabinet.clear()

        for child in child_mocks:
            child.destroy.assert_called_once()
class TestTrainingModePanel(unittest.TestCase):
    def setUp(self):
        patcher = patch("tkinter.Tk")
        self.MockTk = patcher.start()
        self.addCleanup(patcher.stop)

        self.app = Mock()
        self.app.root = self.MockTk()

        self.training_mode_panel = TrainingModePanel(self.app)

    def test_on_language_selected(self):
        test_language = "Английский"
        self.training_mode_panel.on_language_selected(test_language)
        self.app.set_lang.assert_called_once_with(test_language)

    def test_start_training(self):
        self.training_mode_panel.start_training()
        self.app.start_training.assert_called_once()

    def test_show_cabinet_panel(self):
        self.training_mode_panel.show_cabinet_panel()
        self.app.show_cabinet_panel.assert_called_once()

    def test_on_level_selected(self):
        self.training_mode_panel.diff_to_int = Mock(return_value=3)

        test_difficulty = "Сложный"
        self.training_mode_panel.on_level_selected(test_difficulty)

        self.training_mode_panel.diff_to_int.assert_called_once_with(test_difficulty)

        self.app.set_diff.assert_called_once_with(3)


class TestTrainingPanel(unittest.TestCase):
    def setUp(self):
        self.root = Mock()

        self.mock_db_service = Mock()
        self.mock_db_service.send_attempt = Mock()

        self.app = Mock()
        self.app.db_service = self.mock_db_service
        self.app.account = {"nickname": "test_user"}

        self.panel = TrainingPanel(self.app)

        self.panel.sample_label = Mock()
        self.panel.input_entry = Mock()
        self.panel.speed_label = Mock()

        self.panel.sample_label.cget = Mock(return_value="test text")
        self.panel.input_entry.get = Mock(return_value="")

        patch("threading.Thread", new=Mock()).start()
        patch("time.sleep", new=Mock()).start()

    def tearDown(self):
        self.root.destroy()

    def test_clear_stat(self):
        self.panel.clear_stat()
        self.assertEqual(self.panel.warr, 0)
        self.assertEqual(self.panel.mistakes, {})
        self.assertFalse(self.panel.running)
        self.assertEqual(self.panel.counter, 0)

    def test_start_non_running(self):
        start_event_mock = Mock()
        start_event_mock.keycode = 65
        with patch("threading.Thread") as mock_thread:
            self.panel.start(start_event_mock)
            mock_thread.assert_called_once()
            self.assertTrue(self.panel.running)

    @patch("main.threading.Thread")
    def test_start_running(self, mock_thread):
        self.panel.running = True
        start_event_mock = Mock()
        start_event_mock.keycode = 65
        self.panel.input_entry.get.return_value = "test te"
        self.panel.start(start_event_mock)
        self.assertEqual(self.panel.warr, 0)
        mock_thread.assert_not_called()


if __name__ == "__main__":
    unittest.main()
