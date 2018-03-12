# Catalog Web Application

## About

This is an application built for a project requirement in Udacity Fullstack Nanodegree program. 
It provides a list of items within a variety of categories as well as provide a user registration 
and authentication system.
Registered users will have the ability to post, edit and delete their own items.



This project has one main Python module project.py which runs the Flask application. 
A SQL database is created using the database_setup.py module and you can choose to populate the database with test data using
databasesetup.py. The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the 
application. CSS is stored in the static folder.

## Instructions

    Install Vagrant & VirtualBox
    Clone the Udacity Vagrantfile
    Go to Vagrant directory and either clone this repo or download and place zip here
    Launch the Vagrant VM (vagrant up)
    Log into Vagrant VM (vagrant ssh)
    Navigate to cd/vagrant/catalog/Catalog
    The app imports requests which is not on this vm. Run sudo pip install requests
    Setup application database python database_setup.py
    Insert fake data python lotsofmenus.py (Optional)
    Run application using python project.py
    Access the application locally using http://localhost:5000

JSON Endpoints

JSON Catalog: /catalog/JSON - This displays the entire catalog
