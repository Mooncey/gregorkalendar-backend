#!/bin/sh

# Add a new user: John Doe
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name": "John Doe","email": "john@example.com"}' \
http://127.0.0.1:5000/api/users

# Add a new user: someone_1
curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "someone_1","email": "someone_1@example.com"}' \
http://127.0.0.1:5000/api/users

# Add a new team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamName": "CPSC 110","userEmail": "john@example.com"}' \
http://127.0.0.1:5000/api/team

# Add a new member to a team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "someone_1@example.com","name": "someone_1"}}' \
http://127.0.0.1:5000/api/team/member

# Add a new availability for someone_1
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1, "userEmail": "someone_1@example.com", "availableBlocks":[60,61,62,63], "preferNotBlocks": [100,101,102,103]}' \
http://127.0.0.1:5000/api/team/member/availability

# Add a new slot
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"name": "L2A", "numMembers": 2, "startBlock": 60, "endBlock": 63}' \
http://127.0.0.1:5000/api/team/slot

# Try to generate the schedule
# curl -X PUT \
# -H "Content-Type: application/json" \
# -d '{"teamId": 1}' \
# http://127.0.0.1:5000/api/schedule
