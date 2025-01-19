#!/bin/sh

# Add a new user: John Doe
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name": "John Doe","email": "john@example.com"}' \
http://localhost:5000/api/users

# Add a new user: someone_1
curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "someone_1","email": "someone_1@example.com"}' \
http://localhost:5000/api/users

# Add a new team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamName": "CPSC 110","userEmail": "john@example.com"}' \
http://localhost:5000/api/team

# Add a new member to a team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "someone_1@example.com","name": "someone_1"}}' \
http://localhost:5000/api/team/member
