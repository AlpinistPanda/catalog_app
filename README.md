# Catalog Web Application

## About

This is an application built for a project requirement in Udacity Fullstack Nanodegree program. 
It connects to a database and retrieves a list of items within some categories (sports). It features a user login
and authentication system.
If a user logins, he can edit items and add new items.

## Files

project.py --> main file runs flask  
database_setup.py --> sets up the database  
lotsofmenus.py --> populates the database with test data  
templates --> folder that has html templates 


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

## JSON Endpoints

JSON Catalog: /catalog/JSON - This displays the entire catalog
