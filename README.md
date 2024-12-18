# online-shop

Full-featured e-commerce application built using Python Django for the backend and Bootstrap for the frontend. It offers a robust and scalable platform for managing and showcasing products with features like user authentication, product search, and tagging. The application includes dynamic functionalities such as top products with star ratings, related products, and most-viewed products powered by IP-based middleware. Users can register, log in, browse products, and view their order history seamlessly. The project is designed with separated development and production settings, modular requirements files, and an example app with a custom user model, ensuring ease of deployment and extensibility.

![Default Home View](_screenshots/product.png?raw=true "Title")

### Main features

* Separated dev and production settings

* Example app with custom user model

* Bootstrap static files included

* User registration and logging in

* Separated requirements files

* Top Products with star rating

* Related Products 

* Most viewed Products with IP Middleware

* searching on products

* product tag with taagit

* User order history 


# Getting Started
To use this template to start your own project:

clone the project

    git clone https://github.com/amirhossein-bayati/online-shop.git
    
create and start a a virtual environment

    virtualenv env --no-site-packages

    source env/bin/activate

Install the project dependencies:

    pip install -r requirements.txt

create a postgres db and add the credentials to settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_name',
            'USER': 'name',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    
then run

    python manage.py migrate

create admin account

    python manage.py createsuperuser
      
then

    python manage.py makemigrations

to makemigrations for the app

then again run

    python manage.py migrate

to start the development server

    python manage.py runserver

and open localhost:8000 on your browser to view the app.
