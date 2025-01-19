#!/bin/sh

# Add a new user: John Doe
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name": "Emily Fuchs","email": "emilyef@ubc.ca"}' \
http://127.0.0.1:5000/api/users

# Add a new user from here...
curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Matthew Kang","email": "matthew@ubc.ca"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Susan Chung","email": "susan@ubc.ca"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Kevin Zhou","email": "kevin@ubc.ca"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Alice Johnson","email": "alice.johnson@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Bob Smith","email": "bob.smith@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Charlie Davis","email": "charlie.davis@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Diana Garcia","email": "diana.garcia@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Ethan Brown","email": "ethan.brown@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Fiona Clark","email": "fiona.clark@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "George White","email": "george.white@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Hannah Lewis","email": "hannah.lewis@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Ian Walker","email": "ian.walker@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Jasmine Hall","email": "jasmine.hall@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Kevin Zhang","email": "kevin.zhang@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Laura Martinez","email": "laura.martinez@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Michael Harris","email": "michael.harris@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Natalie Clark","email": "natalie.clark@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Oliver Wilson","email": "oliver.wilson@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Penelope Evans","email": "penelope.evans@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Quincy Foster","email": "quincy.foster@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Rachel Scott","email": "rachel.scott@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Steven Turner","email": "steven.turner@example.com"}' \
http://127.0.0.1:5000/api/users

curl -X POST  \
-H "Content-Type: application/json" \
-d '{"name": "Tina Morgan","email": "tina.morgan@example.com"}' \
http://127.0.0.1:5000/api/users



# Add a new team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamName": "CPSC 110","userEmail": "emilyef@ubc.ca"}' \
http://127.0.0.1:5000/api/team

# Add a new member to a team
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "matthew@ubc.ca","name": "Matthew Kang"}}' \
http://127.0.0.1:5000/api/team/member

curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "susan@ubc.ca","name": "Susan Chung"}}' \
http://127.0.0.1:5000/api/team/member

curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"member": {"email": "kevin@ubc.ca","name": "Kevin Zhou"}}' \
http://127.0.0.1:5000/api/team/member

# Add a new availability for someone_1
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1, "userEmail": "matthew@ubc.ca", "availableBlocks":[60,61,62,63], "preferNotBlocks": [100,101,102,103]}' \
http://127.0.0.1:5000/api/team/member/availability

curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1, "userEmail": "susan@ubc.ca", "availableBlocks":[60], "preferNotBlocks": [61, 62, 63, 100,101,102,103]}' \
http://127.0.0.1:5000/api/team/member/availability

curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1, "userEmail": "kevin@ubc.ca", "availableBlocks":[100,101,102,103], "preferNotBlocks": []}' \
http://127.0.0.1:5000/api/team/member/availability

# Add a new slot
curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"name": "L2A", "numMembers": 1, "startBlock": 60, "endBlock": 63}' \
http://127.0.0.1:5000/api/team/slot

curl -X POST \
-H "Content-Type: application/json" \
-d '{"teamId": 1,"name": "L2B", "numMembers": 2, "startBlock": 100, "endBlock": 103}' \
http://127.0.0.1:5000/api/team/slot

# Try to generate the schedule
curl -X PUT \
-H "Content-Type: application/json" \
-d '{"teamId": 1}' \
http://127.0.0.1:5000/api/schedule
