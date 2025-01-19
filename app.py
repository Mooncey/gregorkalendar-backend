from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from models.MemberTeamInfos import MemberTeamInfos
from models.Team import Team
from models.User import User
from models.database import db
from models.TeamUser import team_leaders, team_members
from graphs import match_avails_to_slots, generate_graph, mapping_to_results
import networkx as nx

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
# db = SQLAlchemy(app)

db.init_app(app)


@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    leading_teams_input = []
    member_teams_input = []
    if 'leading_teams' in data:
        leading_teams_input = data['leading_teams']
    if 'member_teams' in data:
        member_teams_input = data['member_teams']
    new_user = User(email=data['email'], name=data['name'], leading_teams=leading_teams_input, member_teams=member_teams_input)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


@app.route('/api/users', methods=['GET'])
def get_users():
    result = db.session.query(User).all()
    return jsonify([user.to_dict() for user in result]), 200

@app.route('/api/user/team')
def get_user_teams():
    # stub_data = {
    #     "teams": [
    #         {
    #             "teamName": "My Awesome Team",
    #             "teamId": 1
    #         },
    #         {
    #             "teamName": "Frontend Team",
    #             "teamId": 2
    #         },
    #         {
    #             "teamName": "Backend Team",
    #             "teamId": 3
    #         },
    #         {
    #             "teamName": "CPSC 110 2024W2",
    #             "teamId": 4
    #         }
    #     ]
    # }

    user_email = request['userEmail']
    user_teams = []

    user = db.session.query(User).filter_by(id=user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    for t in user.leader_teams:
        user_teams.append({
            "teamName": t.name,
            "teamId": t.id
        })

    for t in user.member_teams:
        user_teams.append({
            "teamName": t.name,
            "teamId": t.id
        })
    
    teams = {
        "teams": user_teams
    }

    return jsonify(teams), 2000

@cross_origin()
@app.route('/api/team', methods=['GET'])
def get_team():
    # TODO
    stub_data = {
        "teamId": 1,
        "schedule": {
            "slotAssignments": [
                {
                    "slot": {
                        "name": "L2D",
                        "slotId": 4,
                        "numMembers": 3,
                        "startBlock": 34,
                        "endBlock": 40
                    },
                    "members": [
                        {
                            "name": "Matthew Kang",
                            "email": "matt0410@student.ubc.ca"
                        },
                        {
                            "name": "William Xiao",
                            "email": "munce@student.ubc.ca"
                        }
                    ]
                },
                {
                    "slot": {
                        "name": "L2G",
                        "slotId": 7,
                        "numMembers": 2,
                        "startBlock": 20,
                        "endBlock": 25
                    },
                    "members": [
                        {
                            "name": "Susan Chung",
                            "email": "susan328@student.ubc.ca"
                        },
                        {
                            "name": "Kevin Zhou",
                            "email": "kevz21@student.ubc.ca"
                        }
                    ]
                },
                {
                    "slot": {
                        "name": "L2H",
                        "slotId": 9,
                        "numMembers": 3,
                        "startBlock": 600,
                        "endBlock": 601
                    },
                    "members": [
                        {
                            "name": "Matthew Kang",
                            "email": "matt0410@student.ubc.ca"
                        }
                    ]
                }
            ]
        },
        "availability": {
            "userEmail": "kevz21@student.ubc.ca",
            "availableBlocks": [16, 17, 18, 19, 20, 21, 22, 104, 110],
            "preferNotBlocks": [23, 24, 25, 35, 36, 37, 600]
        },
        "slots": {
            "slots": [
                {
                    "name": "L2A",
                    "slotId": 1,
                    "numMembers": 2,
                    "startBlock": 34,
                    "endBlock": 40
                },
            {
                "name": "L2D",
                "slotId": 4,
                "numMembers": 3,
                "startBlock": 34,
                "endBlock": 40
            },
            {
                "name": "L2E",
                "slotId": 6,
                "numMembers": 3,
                "startBlock": 18,
                "endBlock": 24
            },
            {
                "name": "L2G",
                "slotId": 7,
                "numMembers": 2,
                "startBlock": 20,
                "endBlock": 25
            },
            {
                "name": "L2H",
                "slotId": 9,
                "numMembers": 3,
                "startBlock": 600,
                "endBlock": 601
            }
        ]
        },
        "teamInfo": {
            "name": "My Awesome Team",
            "leaders": [
                {
                    "name": "Gregor Kiczales",
                    "email": "gregor@cs.ubc.ca"
                }
            ],
            "members": [
                {
                    "name": "Susan Chung",
                    "email": "susan328@student.ubc.ca"
                },
                {
                    "name": "Matthew Kang",
                    "email": "matt0410@student.ubc.ca"
                },
                {
                    "name": "Kevin Zhou",
                    "email": "kevz21@student.ubc.ca"
                },
                {
                    "name": "William Xiao",
                    "email": "munce@student.ubc.ca"
                }
            ]
        }
    }
    team_id = request['teamId']
    user_email = request['userEmail']

    team = db.session.query(Team).filter_by(id=team_id).first()
    if not team:
        return jsonify({"error": "Team not found"}), 404

    team_info = {
        "teamId": team.id,
        # "teamName": team.name,
        # "leaders": [leader.to_dict() for leader in team.leaders],
        # "members": [member.to_dict() for member in team.members],
        "teamInfo": {
            "name": team.name,
            "leaders": [{"name": leader.name, "email": leader.email} for leader in team.leaders],
            "members": [{"name": member.name, "email": member.email} for member in team.members]
        }
    }
    if team.schedule:
        team_info["schedule"] = team.schedule
    else:
        team_info["schedule"] = None

    if team.availability:
        team_info["availability"] = team.availability
    else:
        team_info["availability"] = None

    if team.slots:
        team_info["slots"] = team.slots
    else:
        team_info["slots"] = None


    return jsonify(team_info)

@app.route('/api/team', methods=['POST'])
def create_single_team():
    # TODO
    user_email = request['userEmail']
    team_name = request['teamName']
    leaders_input = [db.session.query(User).filter_by(email=user_email).first()]
    members_input = []
    new_team = Team(name=team_name, leaders=leaders_input, members=members_input)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"teamId": new_team.id}), 200

    # return jsonify({
    # "teamId": 110
    # })

# TODO: Delete later
# @app.route('/api/member/team', methods=['GET'])
# def get_member_teams():
#     # TODO
#     stub_data = {
#         "teams": [
#             {
#                 "teamName": "My Awesome Team",
#                 "teamId": 1
#             },
#             {
#                 "teamName": "Frontend Team",
#                 "teamId": 2
#             },
#             {
#                 "teamName": "Backend Team",
#                 "teamId": 3
#             },
#             {
#                 "teamName": "CPSC 110 2024W2",
#                 "teamId": 4
#             }
#         ]
#     }

#     user_email = request['userEmail']
#     user_teams = []

#     user = db.session.query(User).filter_by(id=user_email).first()

#     if not user:
#         return jsonify({"error": "User not found"}), 404
    
#     for t in user.member_teams:
#         user_teams.append({
#             "teamName": t.name,
#             "teamId": t.id
#         })
    
#     teams = {
#         "teams": user_teams
#     }

#     return jsonify(teams)

@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.json

    user_email = data['userEmail']
    team_name = data['teamName']
    leaders_input = [db.session.query(User).filter_by(email=user_email).first()]
    members_input = []
    # if 'leaders' in data:
    #     leader_emails = data['leaders']
    #     for email in leader_emails:
    #         print(email)
    #         leaders_input += [db.session.query(User).filter_by(email=email).first()]
    # if 'members' in data:
    #     members_emails = data['members']
    #     for email in members_emails:
    #         print(email)
    #         members_input += [db.session.query(User).filter_by(email=email).first()]
    new_team = Team(name=team_name, leaders=leaders_input, members=members_input)
    print(new_team)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"teamId": new_team.id}), 200

@app.route('/api/teams', methods=['GET'])
def get_teams():
    result = db.session.query(Team).all()
    return jsonify([team.to_dict() for team in result]), 200


# Graph algorithm endpoints
@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    id = request.args.get("id")
    team = db.session.query(Team).filter_by(id=id).first()
    if not team:
        return jsonify({"error": "Team not found"}), 404

    if not team.schedule:
        return jsonify({"error": "Schedule doesn't exist yet"}), 400

    user_avails = []
    slots = []
    result = match_avails_to_slots(user_avails, slots)
    [print(f"email is {user.email} available slots are {[f"id = {s.slot_id}; pref = {s.prefer_level}" for s in user.avail_slots]}") for user in result]
    graph = generate_graph(result, slots)
    # print(graph)
    result = nx.max_flow_min_cost(graph, "source", "sink")
    final_schedule = mapping_to_results(result, user_avails)
    return jsonify(final_schedule), 200


@event.listens_for(User, 'after_insert')
def update_team_after_insert_user(mapper, connection, target):
    if target.leading_teams:
        for team_id in target.leading_teams:
            team = Team.query.get(team_id)
            if team:
                team.leaders.append(target)
        db.session.commit()
    if target.member_teams:
        for team_id in target.member_teams:
            team = Team.query.get(team_id)
            if team:
                team.members.append(target)
        db.session.commit()

@event.listens_for(Team, 'after_insert')
def update_user_after_insert_team(mapper, connection, target):
    if target.leaders:
        for leader_email in target.leaders:
            # leader = User.query.get(leader_email)
            leader = db.session.query(User).filter_by(email=leader_email).first()
            if leader:
                leader.leading_teams.append(target)
        db.session.commit()
    if target.members:
        for member_email in target.members:
            # member = User.query.get(member_email)
            member = db.session.query(User).filter_by(email=member_email).first()
            if member:
                member.member_teams.append(target)
        db.session.commit()

    



def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    app.run(debug=True)
    