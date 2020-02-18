# Indroduction
the following code correspond to a small django app to handle messages 
to users and user groups (small chat), using django rest framework, jwt auth, jquery, django-channels, redis.

The idea here is use the REST-API endpoints exposed here, to handle the messages regarding the implemented front-end.



#ToDo
1. Intagrate 100% of the api endpoints in the web page hosted by the django application.
2. Implement django-channels with redis to handle real time messages.
3. improve UX/UI.

#Installation.
## Instructions for development:

#### 1. Create virtualenv:
if you do not have virtualenv installed you can check the docs 
https://virtualenvwrapper.readthedocs.io/en/latest/install.html

```
mkvirtualenv condor_chat
```

#### 2. Link project dir to postactivate:
```
setvirtualenvproject <project_dir>
```
#### 3. Clone the repository:
```
git clone https://github.com/ChronoFrank/condor_chat.git
```
#### 4. Install dependencies:
```
workon condor_chat
pip install -r requirements.txt
```
#### 5. Migrate the database (PostgreSQL):

Switch to the `postgres` user.

```
sudo su postgres
```

Create database user `<db_user>` with password `<db_password>`.

```
createuser -U postgres -s -P <db_user>
```

Create a database named `chat`.

```
createdb -U <db_user> chat
```
tpdate the DATABASES variable in condor_chat/settings.py with the recently created access
Then you can sync the database with your own user.

open a terminal and type
```
workon condor_chat
python manage.py migrate
```
#### 6. Run the server:
type in the terminal
```
python manage.py runserver
```
### 7. create superuser:
create a super user with the following command
```
python manage.py createsuperuser
```
### 8. access admin site to create more users to chat with:
* in you browser go to http://localhost:8000/admin
* go to the users model and create users to chat with

### 9. API Usage.
once the user is created, 
you will have to generate an access token so you can authenticate to the other enpoints 

```
#### request ##### 
curl -X POST \
  http://localhost:8000/api/v1/access_token/ \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{"username": "test", "password":"123456"}'
  
#### Response ####

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwidXNlcl9pZCI6MTIsImp0aSI6IjI5OGRjYTExODAxZDRkMzhiYmM0NDZiYmJkYWRlOTcwIiwiZXhwIjoxNTQ4OTcxODcyfQ.pIKY3NBsRxbk1luzyxUYucyHKKnnori0e3TI26DvZzw",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsInVzZXJfaWQiOjEyLCJqdGkiOiI5NTc5Y2NlMDVmOTI0OGI4YTIxMzZhM2Q2OGU2MTdkNSIsImV4cCI6MTU0OTA1NzY3Mn0.84HpReGRRaJYe50R-OIO-jYzHhZ2mbgKT074J1_bu-I"
}
```

The access token has a 5 minutes duration, once you no longer have access,
 you can send the following request to generate a new access token.
 
 ```
 #### Request ####
 curl -X POST \
  http://localhost:8000/api/v1/refresh_token/ \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' \
  -H 'cache-control: no-cache' \
  -d '{
	    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4MjEyMTk4OCwianRpIjoiYmEyOTljY2ZmZDJmNDczNGFiZmMxNWY4MDY0Y2Y1YzQiLCJ1c2VyX2lkIjoxfQ.z-xb3ndtN4daQSPi3LbYHIpyZAdaRzm6lHwulDK3cxg"
    }'

#### Response ####

{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDM2NDE3LCJqdGkiOiJkNDFhZmJjY2M3OTY0ZTI1YTdkZGU2YTc0MmIxOGE1YiIsInVzZXJfaWQiOjF9.q58vghhbyOmeOWgxDZqURsWsZ3qVa-avCm_bSAPyvN4"
}
 
```
Now you can use the access_token to make requests to the following endpoints.

* list available users

```
### request example ###
curl -X GET \
  http://localhost:8000/api/v1/profiles/get_available_users/ \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDM2NDE3LCJqdGkiOiJkNDFhZmJjY2M3OTY0ZTI1YTdkZGU2YTc0MmIxOGE1YiIsInVzZXJfaWQiOjF9.q58vghhbyOmeOWgxDZqURsWsZ3qVa-avCm_bSAPyvN4' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: csrftoken=J99lnrPO7QMSr32b7SQSluYXqZhayiwfvMN3eXxd7RygjrJcxqe59iSyCXojVhW6' \
  -H 'Host: localhost:8000' \

### response example ###

[
     {
        "id": 6,
        "full_name": "carlos ",
        "username": "palmibb",
        "email": "",
        "avatar_url": "http://localhost:12000/media/avatar_files/palmibb_avatar.jpg"
    },
    {
        "id": 7,
        "full_name": "andres",
        "username": "palmieri",
        "email": "",
        "avatar_url": "http://localhost:12000/media/avatar_files/saitama_YuP5tkA.jpeg"
    },
    {
        "id": 10,
        "full_name": "fabra",
        "username": "fabra",
        "email": "",
        "avatar_url": "http://localhost:12000/media/avatar_files/default_img_WgTw0Om.png"
    }
]

```

* Search User by name or email

```
### request example ###
curl -X GET \
  'http://localhost:8000/api/v1/profiles/get_available_users/?full_name=car' \
  -H 'Accept: */*' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDM3MzI3LCJqdGkiOiI3NDAxYTAyZWNlZjE0ODI4OTc0YTE3NTU3YTMwNzk5NyIsInVzZXJfaWQiOjF9.nKHJ-N6_vIDhtAIgXmAClDQCtrOK5mGo4znkycsq1MI' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' 

### response example ###

[
    {
        "id": 6,
        "full_name": "carlos palmiBB",
        "username": "palmibb",
        "email": "",
        "avatar_url": "http://localhost:12000/media/avatar_files/palmibb_avatar.jpg"
    }
]

```

* Send message to user

```
### request example ###
curl -X POST \
  http://localhost:8000/api/v1/send_message_to_user/ \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDM3OTc3LCJqdGkiOiJkYWY2MWI1YzgwM2Q0ODg5YjY5YTgxYjNjN2Y3NmU4NSIsInVzZXJfaWQiOjF9.hkUetTL44o7ilO4Pxlmo3kIZtiQwIE-TnNJZlnPkJHw' \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -d '{
        "message": "this is a test message",
        "user_id": 7
      }'

### response example ###

{
    "title": "fcarreno - palmieri",
    "timestamp": "2020-02-17T22:11:43.568051-05:00",
    "messages": [
        {
            "sender": 1,
            "timestamp": "2020-02-17T22:11:43.563446-05:00",
            "content": "mensaje de prueba para"
        },
        {
            "sender": 1,
            "timestamp": "2020-02-18T09:49:53.942125-05:00",
            "content": "this is a test message"
        }
    ]
}

```

* create a room or group to chat

```
### request example ###
curl -X POST \
  http://localhost:8000/api/v1/rooms/ \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDQwNjYwLCJqdGkiOiI0YzU1YzRiMzI2ODE0YTkxYjVhZDFlOTk4NTlmODMwNCIsInVzZXJfaWQiOjF9.4RJ8tr9OghI_iSWb_vG4XKijNmt4PbknPEnGgo9RQeo' \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' \
  -d '{
    "title": "new test room chat",
    "participants": [3, 5 , 7, 1]
}'

### response example ###
{
    "id": 12,
    "title": "new test room chat",
    "timestamp": "2020-02-18T10:36:34.738532-05:00",
    "messages": []
}

```

* send message to group

```
### request example ###
curl -X POST \
  http://localhost:8000/api/v1/send_message_to_room/ \
  -H 'Accept: */*' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDQyMDk0LCJqdGkiOiIyNGNjYmEwZDU3ZGE0MzM3YjVkZDkyYzQ0YWIwYjQxNSIsInVzZXJfaWQiOjF9.Dp4teza8peKVAhx7IQHOPLUeT6EVrtz3n-NZOFRN1LM' \
  -H 'Content-Type: application/json' \
  -H 'Host: localhost:8000' \
  -d '{
	"message": "new message for new room",
	"group_id": 12
	
}'

### response ###
{
    "id": 12,
    "title": "new test room chat",
    "timestamp": "2020-02-18T10:36:34.738532-05:00",
    "messages": [
        {
            "sender": 1,
            "timestamp": "2020-02-18T11:01:59.668609-05:00",
            "content": "new message for new room"
        }
    ]
}
```


* change profile picture
You must provide a the user id to update, and unless you are superuser you cant change a profile picture
for another user.
```
### request example
curl -X PUT \
  http://localhost:8000/api/v1/profiles/10/pic/ \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyMDQyODI1LCJqdGkiOiI5ZjFlNDFlNDhkNDM0OGJlYmZhMDcwNzc0MzBhZmVhNiIsInVzZXJfaWQiOjF9.sUqS1yJ20B6MIyAKe7mIbQTVFetgFv0M6ves_8u0mX8' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 10939' \
  -H 'Content-Type: multipart/form-data; boundary=--------------------------028661432418725680236886' \
  -H 'Host: localhost:8000' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F avatar=@/home/fcarreno/Pictures/saitama.jpeg

### response ###
# success response
{
    "avatar": "/media/avatar_files/saitama_8t0t4CZ.jpeg"
}

# failed response
{
    "error": "invalid user to update"
}

```

you also can chet the front-end accessing the  url http://localhost:8000

Happy coding :)
