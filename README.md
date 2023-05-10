# Django_rest_framework-test

This repository contains a Django project that uses Django REST Framework and Docker to build a REST API.


To start the Django development server execute the command:
> docker-compose up -d --build

Base URL: http://localhost:8000/. Available endpoints:
- GET /chargepoint: List of chargers
- GET /chargepoint/<id> Charger details for the specified ID
- POST /chargepoint: Create a new charger
- PUT /chargepoint/<id> Modify the charger for the specified ID
- DELETE /chargepoint/<id> Delete the charger for the specified ID
