<h1>В данный момент проект находится в разработке</h1>
<hr>
<h2>Запуск проекта:</h2>
<ul>
    <ol>`git clone`</ol>
    <ol>создать файл web.env в директории `/backend`</ol>
    <ol>вставить в него переменные для тестовой БД:
        <ul>
            <li>`DJANGO_SETTINGS_MODULE=core.settings`</li>
            <li>`POSTGRES_HOST=db`</li>
            <li>`POSTGRES_PORT=5432`</li>
            <li>`POSTGRES_USER=cycle_user`</li>
            <li>`POSTGRES_PASSWORD=pro191Ji321`</li>
            <li>`POSTGRES_DB=cycle_db`</li>
        </ul>
    </ol>
    <ol>`docker compose up --build`</ol>
</ul>
<hr>
<h2>Запуск тестов для бекенда:</h2>
<h4>Из директории backend ввести команду:</h4>
<span>`python manage.py test`</span>
<h4>Или:</h4>
<span>`./manage.py test`</span>
<hr>

<h3>Вы также можете заполнить тестовую БД данными загрузив фикстуры с помощью команды:</h3>
<span>`./manage.py loaddata ./fixture.json`</span>
<hr>


