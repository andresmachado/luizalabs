# luizalabs

## How to run the project
You can run the project on UNIX systems with (Virtualenv recommended)
> make build

## How to make requests
You need to pass your requests through a x-www-form-urlencoded form or JSON object

### To list users:
> GET http://localhost:8000/person/[limit, ]

### To get info about a specific user
> GET http://localhost:8000/person/:facebook_id

### To delete a specific user
> DELETE http://localhost:8000/person/:facebook_id

### OBS:
I can't get username from Facebook, since they deprecated this field on its API versions greater than v2.0
