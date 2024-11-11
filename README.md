## Добро пожаловать в систему обучения!

### В проекте описаны модели:
    Course - Уроки с полями: (Название, описание, изображение, владелец, цена)
    Lesson - Курсы с полями: (Название, описание, изображение, ссылка на видео, курс, владелец, цена)
    Users - Пользователи с полями: (Email, имя, фамилия, телефон, город, аватар)
    Payment - Оплата с полями: (Пользователь, дата, курс, урок, сумма, тип оплаты, сессия, ссылка на оплату)
    Subscription - Подписка на курс: (Пользователь, курс)

###  Необходима настройка:
     1) env.example переименовать в .env
     2) Внести необходимые в нём изменения.
________________________

### Запуск через Docker-compose:
    1) Установить docker следуя инструкции на сайте для своей ОС: https://www.docker.com/
    2) Запустить команду: "docker-compose up -d --build"
    3) Создадутся 5 объединённых контейнеров необходимых для работы приложения. 
    4) Сервер доступен по адресу: http://0.0.0.0:8000/
    
________________________

### Для работы возможно создать:
    1) Суперпользователя: "python manage.py csu" 
        Логин: admin@pow.ru
        Пароль: 12345
________________________
    2) Объекты моделей: "python manage.py fill"