# API для каталога художественных произведений

## **Описание:**

Проект **api_yamdb** создан в учебных целях и демонстрирует
возможности создания программного интерфейса **API** с использованием
одного из актуальных и востребованных подходов — это архитектура *REST*
или *REpresentational State Transfer*.
Разработанный **API-интерфейс** позволяет наладить взаимодействие со
сторонними приложениями и/или устройствами, подддерживающим передачу данных
в формате *json*.

По содержанию **api_yamdb** - это каталог произведений с возможностью для
пользователей создавать свои обзоры с оценкой отдельных произведений, а так
же комментарии к обзорам.  
Так же в проекте реализована система по управлению учетными записями пользователей.

Для этого в проекте созданы следующие логически (и программно) связанные блоки:

1. *Title* - описание произведения, в т.ч.:
    * *Genre* - жанр произведения
    * *Category* - категория произведения
2. *Review* - обзоры с оценкой от зарегистрированных пользователей
3. *Comment* - комментарии зарегистрированных пользователей к обзорам
2. *User* - пользователи
3. *Auth* - регистрация и аутентификация пользователей

### **Установка:**

1. Клонировать репозиторий и перейти в него в командной строке.

2. Cоздать и активировать виртуальное окружение:

```
python -m venv env

source env/bin/activate
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Выполнить миграции:

```
python manage.py migrate
```

5. Запустить проект:

```
python manage.py runserver
```

### **Синтаксис API-запросов:**

Проект **api_yamdb** поддерживает следующие запросы:

**1. *Auth (регистрация, выдача токена)***

 Тип запроса                     | End-point            | Параметры запроса             | Код ответа    |
---------------------------------|----------------------|-------------------------------|---------------|
 POST (регистрация пользователя) | /api/v1/auth/signup/ | *email, username*             | 200, 400      |
 POST (получение токена)         | /api/v1/auth/token/  | *username, confirmation_code* | 200, 400, 404 |

**2. *Category (категории произведений)***

 Тип запроса                     | End-point                  | Авторизация | Параметры запроса | Код ответа         |
---------------------------------|----------------------------|-------------|-------------------|--------------------|
 GET (список всех категорий)     | /api/v1/categories/        | ---         | ---               | 200                |
 POST (создание новой категории) | /api/v1/categories/        | JWT-токен   | *name, slug*      | 201, 400, 401, 403 |
 DELETE (удаление категории)     | /api/v1/categories/{slug}/ | JWT-токен   | ---               | 204, 401, 403, 404 |

**3. *Genre (жанры произведений)***

 Тип запроса                  | End-point              | Авторизация | Параметры запроса | Код ответа         |
------------------------------|------------------------|-------------|-------------------|--------------------|
 GET (список всех жанров)     | /api/v1/genres/        | ---         | ---               | 200                |
 POST (создание нового жанра) | /api/v1/genres/        | JWT-токен   | *name, slug*      | 201, 400, 401, 403 |
 DELETE (удаление жанра)      | /api/v1/genres/{slug}/ | JWT-токен   | ---               | 204, 401, 403, 404 |

**4. *Title (произведения)***

 Тип запроса                         | End-point                   | Авторизация | Параметры запроса                          | Код ответа         |
-------------------------------------|-----------------------------|-------------|--------------------------------------------|--------------------|
 GET (список всех произведений)      | /api/v1/titles/             | ---         | ---                                        | 200                |
 POST (создание нового произведения) | /api/v1/titles/             | JWT-токен   | *name, year, discription, genre, category* | 201, 400, 401, 403 |
 GET (произведение)                  | /api/v1/titles/{titles_id}/ | ---         | ---                                        | 200, 404           |
 PATCH (обновление произведения)     | /api/v1/titles/{titles_id}/ | JWT-токен   | *name, year, discription, genre, category* | 201, 400, 401, 403 |
 DELETE (удаление произведения)      | /api/v1/titles/{titles_id}/ | JWT-токен   | ---                                        | 204, 401, 403, 404 |

**5. *Review (отзывы)***

 Тип запроса                   | End-point                                       | Авторизация | Параметры запроса | Код ответа              |
-------------------------------|-------------------------------------------------|-------------|-------------------|-------------------------|
 GET (список всех отзывов)     | /api/v1/titles/{title_id}/reviews/              | ---         | ---               | 200                     |
 POST (создание нового отзыва) | /api/v1/titles/{title_id}/ reviews/             | JWT-токен   | *text, score*     | 201, 400, 401, 404      |
 GET (отзыв)                   | /api/v1/titles/{title_id}/ reviews/{review_id}/ | ---         | ---               | 200, 404                |
 PATCH (обновление отзыва)     | /api/v1/titles/{title_id}/ reviews/{review_id}/ | JWT-токен   | *text, score*     | 200, 400, 401, 403, 404 |
 DELETE (удаление отзыва)      | /api/v1/titles/{title_id}/ reviews/{review_id}/ | JWT-токен   | ---               | 204, 401, 403, 404      |

**6. *Comment (комментарии к отзывам)***

 Тип запроса                        | End-point                                                             | Авторизация | Параметры запроса | Код ответа              |
------------------------------------|-----------------------------------------------------------------------|-------------|-------------------|-------------------------|
 GET (список всех комментариев)     | /api/v1/titles/{title_id}/ reviews/{review_id}/comments/              | ---         | ---               | 200                     |
 POST (создание нового комментария) | /api/v1/titles/{title_id}/ reviews/{review_id}/comments/              | JWT-токен   | *text*            | 201, 400, 401, 404      |
 GET (комментарий)                  | /api/v1/titles/{title_id}/reviews/ {review_id}/comments/{comment_id}/ | ---         | ---               | 200, 404                |
 PATCH (обновление комментария)     | /api/v1/titles/{title_id}/reviews/ {review_id}/comments/{comment_id}/ | JWT-токен   | *text*            | 200, 400, 401, 403, 404 |
 DELETE (удаление комментария)      | /api/v1/titles/{title_id}/reviews/ {review_id}/comments/{comment_id}/ | JWT-токен   | ---               | 204, 401, 403, 404      |

**7. *User (пользователи)***

 Тип запроса                             | End-point                 | Авторизация | Параметры запроса                                    | Код ответа              |
-----------------------------------------|---------------------------|-------------|------------------------------------------------------|-------------------------|
 GET (список всех пользователей)         | /api/v1/users/            | JWT-токен   | ---                                                  | 200, 401                |
 POST (создание нового пользователя)     | /api/v1/users/            | JWT-токен   | *username, email (first_name, last_name, bio, role)* | 201, 400, 401, 403      |
 GET (пользователь)                      | /api/v1/users/{username}/ | JWT-токен   | ---                                                  | 200, 404                |
 PATCH (обновление пользователя)         | /api/v1/users/{username}/ | JWT-токен   | *username, email (first_name, last_name, bio, role)* | 200, 400, 401, 403, 404 |
 DELETE (удаление пользователя)          | /api/v1/users/{username}/ | JWT-токен   | ---                                                  | 204, 401, 403, 404      |
 GET (своя учетная запись)               | /api/v1/users/me/         | JWT-токен   | ---                                                  | 200                     |
 PATCH (обновление своей учетной записи) | /api/v1/users/me/         | JWT-токен   | *username, email (first_name, last_name, bio)*       | 200, 400                |

### Авторы
Максим и команда Практикума
