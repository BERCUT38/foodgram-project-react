# praktikum_new_diplom
https://github.com/BERCUT38/foodgram-project-react/runs/6486300334?check_suite_focus=true

# api_yamdb 

 

foodgramm - это интерфейс, который позволяет публиковать рецепты, собирать рецепты других пользователей, так же формировать корзину продуктов для приготовления интересуюих рецептов. 

 

### Используемые технологии: 

 

+ Django, 

+ Django rest framework, 

+ Simple JWT, 

+ Python 

 

### Переменные окружения 

 

DB_ENGINE  

DB_NAME 

POSTGRES_USER 

POSTGRES_PASSWORD 

DB_HOST 

DB_PORT 

 

### Как запустить проект локально(ubuntu):
1 - Из папки infra/ запускаем команду:
	sudo docker-compose up -d --build

2 - выполняем команды:
	 docker-compose exec web python manage.py makemigrations
    	 docker-compose exec web python manage.py migrate
    	 # заполним базу ингредиентами
	 docker-compose exec web python manage.py add_base --path data/
 
3 - из папки infra/server/colors.txt внести тэги через админ зону

4 - Проект доступен локально по адресу:
			http://localhost/

### Запуск на сервере
из папки "infra/server/" скопировать на вирт. машину сборку docker-compose.yml, .env, default.conf

При выполнении команды "Push" проект выполняет загрузку на сервер и развертку. 

При первой разверте выполнить:
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py add_base --path data/
	docker-compose exec web python manage.py createsuperuser

 

Автор: Будник Сергей 
