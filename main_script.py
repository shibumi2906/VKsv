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
