[![CircleCI](https://circleci.com/gh/sam-karis/sendIt-API.svg?style=svg)](https://circleci.com/gh/sam-karis/sendIt-API)
[![Coverage Status](https://coveralls.io/repos/github/sam-karis/sendIt-API/badge.svg?branch=master)](https://coveralls.io/github/sam-karis/sendIt-API?branch=master)

# SendiT-API
SendIt-API is a courier service that helps users deliver parcels to different destinations.  
The API functionality and the respective endpoints include the following:  
 

|Endpoints and methods                           | Functionality                        |Authorized
|------------------------------------------------|---------------------------------------|---------------------
|/api/v1/auth/signup(POST)                       |Register a user                        | Everybody
|/api/v1/auth/login(POST)                        |Login a user                           | Registered user
|/api/v1/auth/reset-password(POST)               |Reset a user Password                  | Registered user
|/api/v1/parcels (POST)                          |Make a new order                       | Logged in user       
|/api/v1/parcels(GET)                            |Get all orders                         | Admin only     
|/api/v1/parcels/*parcel_id* (GET)               |Get one order by id                    | Admin only 
|/api/v1/users/*user_id*/parcels(GET)            |Get all orders for a user              | Owner of the order
|/api/v1/users/*user_id*/parcels/*parcel_id*(GET)|Get one order by id                    | Owner of the order
|/api/v1/parcels/*parcel_id*/cancel(PUT)         |Cancel an placed order                 | Owner of the order
|/api/v1/parcels/*parcel_id*/destination(PUT)    |Edit deliverly destination of an order | Owner of the order
|/api/v1/parcels/*parcel_id*/status(PUT)         |update order status                    | Admin only 
|/api/v1/parcels/*parcel_id*/presentLocation(PUT)|update parcel current location         | Admin only 

#### Running and Testing of the API

**Prequisites**
```
Python - version 3.7.2
Postgress database
postman - To run various endponts
```
**Installing**   

Perform the following simple steps:   
- Open git and navigate to directory yo which to run the app from.
- Git clone the this repository using either.
  - Using SSH:
    
    ``git@github.com:sam-karis/sendIt-API.git``
  
  - Using HTTP:
    
    ``https://github.com/sam-karis/sendIt-API.git``

- Set up a virtual eniviroment for reference click [here](https://pipenv.readthedocs.io/en/latest/).

- Install the apps dependencies by running `pipenv install`
- Activate the virtualenv on your terminal ``pipenv shell``

- Create database and set all global variables defined in the ``env.sample.sh``  

To create database tables run  
    `flask migrate`  

To drop database tables run  
    `flask drop`  

To run the app to launch the localhost.  
    ``flask run``

**Tests**   
SendIt-API has automated test(unittest) to check if it the endpoints work as expected.  
To run the tests activate the virtual environment and then set ``FLASK_ENV`` to ``testing``  
To run the test use ``pytests`` or ``tox``

**To contribute to this work**

Fork the repository from links shared above and make a pull request.