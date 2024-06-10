# Social Networking API

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/35951631-0bd98368-2682-4c97-acb9-654a4c3c8744?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D35951631-0bd98368-2682-4c97-acb9-654a4c3c8744%26entityType%3Dcollection%26workspaceId%3Dd7b2eef9-d25e-4b39-9c34-a5bd4f9e8efe)

This project is a social networking API built using Django Rest Framework (DRF). It provides functionalities for user registration, login, friend request management, and user search.

## Features

- User Registration and Login
- Search users by email or name
- Send, accept, and reject friend requests
- List friends and pending friend requests

## Installation (For Docker Users)

### Prerequisites
- Python 3.8+

### Step 1: Clone the Repository
```bash
git clone https://github.com/paras-gill/Social-Networking-API.git
cd social_networking_api
```

### Step 2: Create and configure .env file
Create a .env file in the root directory. Add the following variables to the .env file:
```
POSTGRES_DB=networking
POSTGRES_USER=dev101
POSTGRES_PASSWORD=hello!world
```

### Step 3: Build and run the containers
```bash
docker-compose up -d --build
```

### Step 4: Migrate Database
To migrate the new PostgreSQL database running in Docker execute the following command:
```bash
docker-compose exec web python manage.py migrate
```

### Step 5: Create superuser 
Create a superuser to access the Django admin:
```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts to set up the superuser account.

### Step 5: Access the API
Now you can access the application at `https://127.0.0.1:8080`

Use `Run in Postman` button at the top of this Readme file to test APIs using Postman collection.

### Step 6: Close Container
When you're done, close down your Docker container:
```bash
docker-compose down
```


## Installation (For Non-Docker Users)

Follow these steps to set up the project locally:

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/paras-gill/Social-Networking-API.git
cd social_networking_api
```

### Step 2: Setup a Virtual Environment
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Create and configure .env file
Create a .env file in the root directory. Add the following variables to the .env file:
```bash
POSTGRES_DB=networking
POSTGRES_USER=dev101
POSTGRES_PASSWORD=hello!world
```

### Step 5: Configure the Database
Ensure that PostgreSQL is installed on your system. For Linux users, use the following commands:
```bash
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install libpq-dev python3-dev
```

Install psycopg2, a PostgreSQL adapter for Django, using the following command:
```bash
pip install psycopg2
```

Start PostgreSQL server:
```bash
sudo service postgresql start
```

By default, PostgreSQL is configured to use the postgres user. Switch to this user:
```bash
sudo -i -u postgres
```
Access the PostgreSQL Shell:
```bash
psql
```

Create a database named `networking` which this application is configured to use:
```bash
CREATE DATABASE networking;
CREATE USER dev101 WITH PASSWORD 'hello!world';
GRANT ALL PRIVILEGES ON DATABASE networking TO dev101;
```


### Step 6: Apply Migrations
Apply the database migrations to create the necessary tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create a Superuser 
Create a superuser to access the Django admin:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up the superuser account.

### Step 8: Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

### Step 9: Access the API
The API will be available at http://127.0.0.1:8000.

Use `Run in Postman` button at the top of this Readme file to test APIs using Postman collection.


## Endpoints

- `POST /register/`: Register a new user
- `POST /login/`: Log in a user
- `GET /users/search/`: Search users by email or name (requires authentication)
- `POST /friend-request/send/<receiver_id>/`: Send a friend request (requires authentication)
- `GET /friend-requests/pending/`: List pending friend requests (requires authentication)
- `PATCH /friend-request/respond/<request_id>/<action>/`: Respond to a friend request (requires authentication)
- `GET /friends/`: List friends (requires authentication)

## Authentication Scheme

The API uses JWT for authentication. Include the token in the Authorization header of requests that require authentication:

```bash
Authorization: Bearer <your_token>
```

## Throttling

To prevent abuse, the API has rate limiting enabled for sending friend requests. Users can send up to 3 friend requests per minute.

## Testing API

You can use followong three methods to test your API

#### 1. [Postman app](https://www.postman.com/downloads/)
   
#### 2.  Browser

#### 3.  cURL command
 For example: Command to register user:
 ```bash
curl -X POST \
  http://127.0.0.1:8000/api/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "john.doe@example.com",
    "name": "John Doe",
    "password": "hello!world"
}'
 ```
Command to login user:

```bash
curl -X POST \
  http://127.0.0.1:8000/api/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "john.doe@example.com",
    "password": "hello!world"
}'
```
It will return an access token. Use it to access all api end points requiring authentication. For example, command to search all users containing "am" in their name:
```bash
curl -X GET \
  http://127.0.0.1:8000/api/users/search/?query=am \
  -H 'Authorization: Bearer your_access_token_here'
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.


## Contact

For any inquiries or support, please contact [paras_gill@outlook.com](mailto:paras_gill@outlook.com).
