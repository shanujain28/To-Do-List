# To-Do List API

#### In this post, we will build a RESTful API to handle CRUD operations on the list of To-Do tasks stored in MySQL database using FastAPI library. It uses an authentication API that grants access to the users with a valid API key.


## Features
– To-do Task Management: The system allows you to perform CRUD (Create, Read, Update and DELETE) operations on your tasks.

Authentication : This layer confirm that API only accesssible valid user.

MySQL Database Integration — Used to store the task info in a structured way

## Endpoints

GET / : Returns a welcome message for Logged in Users

- Retrieve all tasks stored in the database with a `GET /tasks`,

— `POST /tasks`: Here you can add new task to the database.

PUT /tasks/{task_id} Updates existing task into the database

• `DELETE /tasks/{task_id}`: This endpoint deletes a specific task in the database.

## Requirements

- Python: 3.6+

- FastAPI

- mysql-connector-python

- python-dotenv

- pydantic

- uvicorn

## Installation

1. Clone this down to your local machine.

2. Following, move to the project directory

3. Run the following command to install required modules:

```bash

pip install fastapi mysql-connector-python pydantic python-dotenv uvicorn

```

## Database Structure

### Tasks Table

| Column | Type | Description --

|———————- | —————————– |————————————————– |

Autocreated: task_idINTUnique indentifier for tasks

| task | VARCHAR | Description of the task

| done | BOOLEAN | Status  indicating completion

API Keys Table
| Column | Type | Description
| api_id |	INT	| Unique identifier for API keys 
| api_key|	VARCHAR	| The API key for authentication


### Use Note: Before executing the API, make sure you have a MySQL database configured and the required environment variables set up.

### In the root of your project, create a.env file with the following information:

plaintext
Copy the code.
MYSQL_USER="your_username"
"your_password" is the MySQL password.
For example, "localhost" or "127.0.0.1" MYSQL_HOST="your_host_ip" MYSQL_DB="your_database"
In the project directory, launch your command prompt or terminal.

### Use this command to launch the API:

party
Code uvicorn main:app --reload should be copied.
The URL for the API will be http://127.0.0.1:8000.

### The API documentation can be found at:

Arduino
https://127.0.0.1:8000/docs?api_key=YOUR-TOKEN is the code to copy.
Put your real API key in lieu of YOUR-TOKEN.

In conclusion
A strong basis for task management with authentication and permanent storage is offered by this To-Do List API. Adapt and expand it to meet your needs!
