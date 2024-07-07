# Django Rest Frame Work

***Implement a simple todo API using Django Rest Frame Work***

## How to install

```bash
pip install -r requirements.txt
```

## How to run

### First migrate your database

```bash
python manage.py migrate
```

#### Second create a super user

```bash
python manage.py createsuperuser
```

#### Then run this command

```bash
python manage.py runserver
```

*It has JWT authentication so use postman to test the api and to get token and refresh it use these urls:*

- *To get token use this url:* `http://127.0.0.1:8000/api/token/`
- *To refresh your token use this url:* `http://127.0.0.1:8000/api/token/refresh`
