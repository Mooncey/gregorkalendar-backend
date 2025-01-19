#!/bin/sh

# Add a new user: John Doe
curl -X POST http://localhost:5000/api/users \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "email": "john@example.com"
}'

# Add a new user: someone_1
curl -X POST http://localhost:5000/api/users \
-H "Content-Type: application/json" \
-d '{"name": "someone_1","email": "someone_1@example.com"}'

# Add a new team
curl -X POST http://localhost:5000/api/team \
-H "Content-Type: application/json" \
-d '{"teamName": "CPSC 110","userEmail": "john@example.com"}'

# Add a new member to a team
curl -X POST http://localhost:5000/api/team/member \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "someone_1@example.com","name": "someone_1"}}'
