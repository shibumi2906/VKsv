import vk_api
import os
import time
from loguru import logger
from config import access_token, group_id, video_folder, description  # Импорт конфиденциальной информации

# Настройка логирования
logger.add("main_script.log", rotation="1 MB")

# Авторизация в VK через API
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()


# Функция для загрузки и постинга видео как клипа
def post_video(file_path, group_id, description):
    try:
        # Получаем данные для загрузки, устанавливаем is_clips=True
        logger.info(f"Получаем URL для загрузки видео: {file_path}")
        response_save = vk.video.save(
            name=os.path.basename(file_path),
            description=description,
            group_id=group_id,
            is_clips=True  # Загрузка как клип
        )
        upload_url = response_save['upload_url']
        logger.info(f"Параметры загрузки: {response_save}")

        # Загружаем видео
        logger.info(f"Загружаем видео: {file_path}")
        with open(file_path, 'rb') as video_file:
            response = vk_api.upload.VkUpload(vk_session).http.post(upload_url, files={'video_file': video_file})

        logger.info(f"Ответ от VK после загрузки: {response}")

        # Видео успешно загружено, создаем пост
        logger.info(f"Создаем пост для видео: {file_path}")
        vk.wall.post(owner_id=-int(group_id), from_group=1, message=description,
                     attachments=f"video{response['owner_id']}_{response['video_id']}")
        logger.info(f"Видео {file_path} успешно загружено и опубликовано как клип.")

    except Exception as e:
        logger.error(f"Ошибка при загрузке видео {file_path}: {e}")


# Основной цикл для загрузки всех видео из папки
def upload_videos_from_folder(video_folder, group_id, description):
    # Перебираем файлы в папке
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        logger.info(f"Начинаем загрузку видео: {video_file}")
        try:
            post_video(video_path, group_id, description)
            logger.info(f"Видео {video_file} успешно загружено.")
        except Exception as e:
            logger.error(f"Ошибка при загрузке видео {video_file}: {e}")

        # Ждем некоторое время, чтобы избежать блокировок
        time.sleep(5)


# Запуск загрузки только при непосредственном запуске скрипта
if __name__ == "__main__":
    logger.info("Запуск скрипта для загрузки видео из папки")
    upload_videos_from_folder(video_folder, group_id, description)
