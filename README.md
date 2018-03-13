# Catalog Web Application

## Introduction

This is an application built for a project requirement in Udacity Fullstack Nanodegree program. 
It connects to a database and retrieves a list of items within some categories (sports). It features a user login
and authentication system.
If a user logins, he can edit or delete existing items (only if he created it) and add new items.

## Changes after first review ver. 2

- removed facebook login as it needs a valid privacy agreement and i dont have that
- removed the feature of adding, removing, 

## Files

project.py --> main file runs flask  
database_setup.py --> sets up the database  
some_items.py --> populates the database with test data  
templates --> folder that has html templates 

## Instructions

    Install Vagrant & VirtualBox
    Clone the Udacity Vagrantfile
    Go to Vagrant directory and either clone this repo or download and place zip here
    Launch the Vagrant VM (vagrant up)
    Log into Vagrant VM (vagrant ssh)
    Navigate to the directory
    The app imports requests which is not on this vm. Run sudo pip install requests
    Setup application database python database_setup.py
    Insert fake data python some_items.py (Optional)
    Run application using python project.py
    Access the application locally using http://localhost:5000

## JSON Endpoints

JSON Catalog: /catalog/JSON - This displays the entire catalog
