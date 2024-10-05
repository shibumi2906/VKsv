import vk_api
import os
import time

# Параметры
access_token = "ВАШ_ТОКЕН"  # Токен доступа
group_id = "ID_ГРУППЫ"  # ID вашей группы (без минуса)
video_folder = "путь_до_папки_с_видео"  # Путь до папки с видеофайлами
description = "Описание для видео"  # Описание для видео

# Авторизация в VK через API
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()


# Функция для загрузки и постинга видео
def post_video(file_path, group_id, description):
    # Получаем данные для загрузки
    upload_url = vk.video.save(name=os.path.basename(file_path), description=description, group_id=group_id)[
        'upload_url']

    # Загружаем видео
    with open(file_path, 'rb') as video_file:
        response = vk_api.upload.VkUpload(vk_session).http.post(upload_url, files={'video_file': video_file})

    # Видео успешно загружено, создаем пост
    vk.wall.post(owner_id=-int(group_id), from_group=1, message=description,
                 attachments=f"video{response['owner_id']}_{response['video_id']}")


# Основной цикл для загрузки всех видео из папки
def upload_videos_from_folder(video_folder, group_id, description):
    # Перебираем файлы в папке
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"Загружаем видео: {video_file}")
        try:
            post_video(video_path, group_id, description)
            print(f"Видео {video_file} успешно загружено.")
        except Exception as e:
            print(f"Ошибка при загрузке видео {video_file}: {e}")

        # Ждем некоторое время, чтобы избежать блокировок
        time.sleep(5)


# Запуск загрузки только при непосредственном запуске скрипта
if __name__ == "__main__":
    upload_videos_from_folder(video_folder, group_id, description)
