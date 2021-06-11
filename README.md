# usersapi

# These tutorial describe how to run application for testing purpose. Productive deployment tutorial will presented in next release.

    - Install postgres database;
    - Create database(DB_NAME);
    - Create database user(DB_USER);
    - Grant all privileges for user to the database;
    - Clone application from git to the local directory, git clone....;
    - Create python environment;
    - Create env variables in python environment; List of variables 
    (
    SEC_KEY='django-insecure-.....', 
    DB_NAME='userapi', 
    DB_USER='useruser', 
    DB_PASS='user1234', 
    DB_HOST='localhost', 
    DB_PORT=''
    )
    - Install python packages from requirements.txt file: pip install -r requirements.txt;
    - Migrate database structure to the database: python manage.py makemigrations python manage.py migrate;
    - Create superuser, for admin web: python manage.py createsuperuser;
    - Start django server in test mode python manage.py runserver
 
# REST API Description:
    Get token
    Request:
    URL: serever_hostname/api/users/get_token
    Method: POST
    Headers: 'Content-Type: application/json'
    Body:
    { 
        "username": "Kirill",
        "password": "Kirill@$%16745" 
    }
    Success Response:
    Code: HTTP 200 OK

    Create user
    Request:
    URL: serever_hostname/api/users/create_user
    Method: POST
    Headers: 'Content-Type: application/json', 'Bearer <token>'
    Body:
    {
        "username": "Batman",
        "password": "Batman@$%16745",
        "first_name": "Roman",
        "last_name": "Ivanov",
        "is_active": 1
    }
    Success Response:
    Code: HTTP 201 Created
    
    Get users
    Request:
    URL: serever_hostname/api/users/get_users
    Method: GET
    Headers: 'Content-Type: application/json', 'Bearer <token>'
    Success Response:
    Code: HTTP 200 OK
    
    Get user
    Request:
    URL: serever_hostname/api/users/get_user/<user_id>
    Method: GET
    Headers: 'Content-Type: application/json', 'Bearer <token>'
    Success Response:
    Code: HTTP 200 OK
    
    Update user
    Request:
    URL: serever_hostname/api/users/update_user/<user_id>
    Method: PATCH
    Body:
    {
        "password": "Batman@$%16745",
    }
    Headers: 'Content-Type: application/json', 'Bearer <token>'
    Success Response:
    Code: HTTP 200 OK
    
    Delete user
    Request:
    URL: serever_hostname/api/users/delete_user/<user_id>
    Method: DELETE
    Headers: 'Content-Type: application/json', 'Bearer <token>'
    Success Response:
    Code: HTTP 204 No Content