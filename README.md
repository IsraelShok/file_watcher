File Watcher
This is a file watcher application that monitors a specified directory for changes, and logs them to a database and a log file.

# Getting Started
To get started with this application, follow the instructions below.

# Prerequisites
To run this application, you will need to have Docker installed on your machine. You can download Docker from the official website here.

# Installing
Clone this repository to your local machine.
Navigate to the project directory in your terminal.
Create a .env file in the project root directory, and set the following environment variables:
```
DB_USERNAME='files_user'
DB_PASSWORD='files_pass'
DB_HOST='postgres'
DB_DATABASE='files_db'
DB_PORT = '5432'

RABBITMQ_QUEUE='file_changes'
RABBITMQ_USER='rabbit_user'
RABBITMQ_PASSWORD='rabbit_pass'
RABBITMQ_HOST='rabbitmq'

PATH_TO_WATCH = '<path to directory to monitor>'

FILES_FOLDER = '/files_folder'
```

Run `docker-compose up --build` to start the application.

# Running the Tests
To run the tests for this application, navigate to the project directory in your terminal and run the following command:
`python -m unittest`


# Built With
Python
Watchdog
Docker
PostgreSQL

# Acknowledgments
This application was built using the Watchdog library.
This project was completed as part of an assignment for a software engineering course.
