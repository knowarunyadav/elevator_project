[[_TOC_]]

# General Instructions
- Default Drop Floor : Ground Floor
- For Eg: if a request comes from any floor, it's drop floor will always be ground.
- After Picking all requests, elevator will always move to Ground Floor.
- All Elevators can have any number of requests, there's no max capacity.

# Models Used
- Elevator model contains all the details regarding elevator
- 2nd model holds the elevator requests

# API

1) request Elevator : Will assign the elevator that takes least time to reach ground floor
2) Move Elevator : Will move each elevator one floor up or down based on the request. Will also open and close gates as per required and makes elevator stop and start

3) Elevators : To create elevators and get details of elevators
4) Elevator : To get detail of a particular elevator
5) Not working : Sets an elevator as non functional.

# Serializers

- have created manual serializers, it gives more control over them , you can design them as required.

# Testing 

1) All Api(s) can be tested using POSTMAN or any other tool or normal browser since no POST requests are made , it's a simple project.

# Deployment

- Can be deployed like any other simple django project.