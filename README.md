#  To Run the project

#### for console Sent email just place this code in settings.py

```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
## Prerequisites

- install Docker and docker compose
- run `docker-compose up --build --remove-orphans`
- in separate terminal run `sudo docker exec -it myproject sh`
- in the docker shell run `python manage.py makemigrations`
- then ` python manage.py migrate`
- then ` python manage.py createsuperuser`

### For api Documentations

```
http://127.0.0.1:8000/swagger/
```


### Postman Test setup COde

```
const loginResponse = JSON.parse(responseBody);
pm.environment.set("ACCESS_TOKEN", loginResponse.data.access);
```