# File Watcher
This is a file watcher application that monitors a specified directory for changes, and logs them to a database and a log file.

If there are 2 identical files (same content), the handler will change the latest file to <original_file_name>_DUP_#.

For example:

<img width="759" alt="image" src="https://user-images.githubusercontent.com/18027980/222963889-ad49a598-8ac7-4f4e-8de8-df1cb696a996.png">

# Getting Started
To get started with this application, follow the instructions below.

# Prerequisites
To run this application, you will need to have Docker installed on your machine. You can download Docker from the official website.

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

# Logs
To see the logs, in the same watch dir, will be created a "logs" folder that contains "log.txt" and "db_status.csv" (Current status of the DB).

Also, there are print logs in each container.

For example:

<img width="745" alt="image" src="https://user-images.githubusercontent.com/18027980/222963480-ca29ef23-b699-4f0e-b925-5d4509fb1f49.png">

<img width="1100" alt="image" src="https://user-images.githubusercontent.com/18027980/222963493-63ddeb66-10bd-4b0a-885a-a56edd980bd0.png">

<img width="807" alt="image" src="https://user-images.githubusercontent.com/18027980/222963543-e7e1f99a-d8e4-4acd-a912-34bb57363467.png">


# Built With
Python

Watchdog

Docker

PostgreSQL

RabbitMQ
