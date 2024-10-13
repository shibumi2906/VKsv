import unittest
from unittest.mock import patch, MagicMock
import os
from loguru import logger
from config import access_token, group_id, video_folder, description  # Импорт конфиденциальной информации

# Импортируем функции, которые будем тестировать
from main_script import post_video, upload_videos_from_folder

class TestVkVideoUpload(unittest.TestCase):

    @patch('time.sleep', return_value=None)
    @patch('main_script.post_video')
    @patch('os.listdir')
    def test_upload_videos_from_folder(self, mock_listdir, mock_post_video, mock_sleep):
        # Мокаем список файлов
        mock_listdir.return_value = ['video1.mp4', 'video2.avi']

        # Вызываем тестируемую функцию
        upload_videos_from_folder('fake_folder', '123', 'Test description')

        # Отладочный вывод вызовов post_video
        logger.info(mock_post_video.call_args_list)

        # Проверяем вызовы с использованием os.path.join для корректного пути
        mock_post_video.assert_any_call(os.path.join('fake_folder', 'video1.mp4'), '123', 'Test description')
        mock_post_video.assert_any_call(os.path.join('fake_folder', 'video2.avi'), '123', 'Test description')
        self.assertEqual(mock_post_video.call_count, 2)  # Проверка на два вызова

if __name__ == '__main__':
    unittest.main()


