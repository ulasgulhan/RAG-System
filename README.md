# RAG-System

## Overview
This project is an AI agent that answers questions asked by the user. Prepared as sample code for RAG Implementation. 2023 World Population data is available in AWS S3.


## Technologies Used

**Backend:** Django Web Framework, Django Rest Framework, LangChain, Pandas, NumPy, Cohere, Pyarrow, Renumics 

**Database:** PostgreSQL, AWS S3, Chroma


## URL's

**Register:** http://127.0.0.1:8000/auth/register/

**Login:** http://127.0.0.1:8000/auth/login/

**Logout:** http://127.0.0.1:8000/auth/logout/

**LLM Agent:** http://127.0.0.1:8000/api/llm/


## Make Migrations

```sh
    $ python manage.py makemigrations
```

```sh
    $ python manage.py migrate
```

## Start the Project

```sh
    $ python manage.py runserver
```

## Superuser Data

- Superuser Username
```sh
    admin
```
- Superuser password
```sh
    123
```

## Code Formatting
This project uses black formatter. You can use this command to format your code:
- Format all files
```sh
    $ black .
```
- Format a single file
```sh
    $ black <file_name>
```
Detailed information about black formatter: https://github.com/psf/black