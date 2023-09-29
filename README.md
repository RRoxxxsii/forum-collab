<h1>В данный момент проект находится в разработке</h1>
<hr>
<h2>Запуск проекта:</h2>
<ul>


1 `git clone`


2 создать файл web.env в директории backend

3 вставить в него переменные для тестовой БД:


+ `DJANGO_SETTINGS_MODULE=core.settings` 
+ `POSTGRES_HOST=db`
+ `POSTGRES_PORT=5432`
+ `POSTGRES_USER=cycle_user`
+ `POSTGRES_PASSWORD=pro191Ji321`
+ `POSTGRES_DB=cycle_db`
    

4 `docker compose up --build`

</ul>
<hr>

**Запуск тестов для бекенда:**

Из директории backend ввести команду:

<span>`python manage.py test`</span>

**Или:**

<span>`./manage.py test`</span>
<hr>

<h3>Вы также можете заполнить тестовую БД данными загрузив фикстуры с помощью команды:</h3>
<span>`./manage.py loaddata ./fixture.json`</span>
<hr>
<h3>Если есть необходимость создать дополнительные тестовые данные, вы можете ввести команду:</h3>

<span>`./manage.py createdata`</span>
<hr>
<h3><a href="https://github.com/RRoxxxsii/forum-collab/blob/backend-main/backend/admin_info.txt">Реквизиты для доступа к админ-панели с тестовыми данными по ссылке</a></h3>
<hr>
<h3>Документация API доступна по адресу:</h3>

`localhost:8000/swagger`