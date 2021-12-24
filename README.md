# Local Library - A Library Management System

This web application creates an online catalog for a small local library, where users can browse available books and manage their accounts.

## Features

The main features that have currently been implemented are:

- There are models for books, book copies, genre, language and authors.
- Users can view list and detail information for books and authors.
- Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).
- Librarians can renew reserved books
  
## Technology Stack

**Frontend:** HTML, CSS(+ Bootstrap 4)  
**Backend:** Python/Django  
**Database:** SQLite3  

And additional requirements are in [**requirements.txt**](https://github.com/jkrlr/locallibrary/blob/master/requirements.txt)

## Getting Started

### Setting-up the project

- Download and install Python 3.8
- Download and install Git.
- Fork the Repository.
- Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/locallibrary.git`
- Change directory to locallibrary `$ cd locallibrary`
- Install virtualenv `$ pip3 install virtualenv`
- Create a virtual environment `$ virtualenv env -p python3.8`  
- Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
- Install the requirements: `$ pip install -r requirements.txt`
- Make migrations `$ python manage.py makemigrations`
- Migrate the changes to the database `$ python manage.py migrate`
- Create admin `$ python manage.py createsuperuser`
- Run the server `$ python manage.py runserver`
