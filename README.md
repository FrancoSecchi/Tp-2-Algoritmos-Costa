# CRUX

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


## Requirements

It is recommended to use a virtual environment (Eg: **_virtualenv_** python module)

Crux requires these versions: 
- **Python3.7**
- Facebook api
    - **Python-facebook-api==0.4.2**
- ChatBot
    - ... 

## Create virtual environment
Install virtualenv from python

`pip install virtualenv`

Then, place yourself in the project folder, run the following command

`virtualenv venv --python=python3.7`


What this command does is create a folder called venv which will contain the installed python modules.
And the '**_--python=python3.7_**' configures the version of python that the virtual environment will use.
(configures the version of python that the virtual environment will use **_ChatBot_**)

Having already installed the virtual environment, to work within the virtual environment, run the following command

`. venv/bin/activate` o `source venv/bin/activate`

And once inside it, proceed to install the corresponding modules.
To be able to exit the virtual environment, run the following command

`deactivate`

## Facebook-api installation  
To install **python-facebook-api**, copy and run the following code in your terminal

`pip install python-facebook-api==0.4.2`