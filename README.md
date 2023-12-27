# Blog API with Django Rest Framework

This project is a simple Blog API built using Django Rest Framework (DRF).

## Features

- RESTful API to create, list, update, and delete blog post.
- User Registration(sign up)
- Authentication(login)
- Comment on post.
- Following and unfollowing users.
- Listing all users 
- Viewing user profile
- Token Authentication


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Pipenv (for Python dependency management)

## Requirements

- asgiref==3.7.2
- attrs==23.1.0
- Django==5.0
- djangorestframework==3.14.0
- drf-yasg==1.21.7
- inflection==0.5.1
- jsonschema==4.20.0
- jsonschema-specifications==2023.12.1
- packaging==23.2
- pytz==2023.3.post1
- PyYAML==6.0.1
- referencing==0.32.0
- rpds-py==0.15.2
- sqlparse==0.4.4
- swagger-spec-validator==3.0.3
- typing_extensions==4.9.0
- uritemplate==4.1.1

## Setup

Navigate to the directory:

   pipenv shell

   pip install -r requirements.txt

   python manage.py makemigrations app

   python manage.py migrate

   python manage.py runserver

The API will be available at http://localhost:8000/ 

For Swagger Documentation visit http://localhost:8000/swagger/ 
For Redoc Documentation visit http://localhost:8000/redoc/ 


