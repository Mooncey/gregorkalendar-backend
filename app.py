from datetime import datetime
import json
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy import event, and_
from sqlalchemy.orm import sessionmaker
from models.MemberTeamInfos import MemberTeamInfos
from models.Team import Team
from models.User import User
from models.database import db
from models.TeamUser import team_leaders, team_members
from graphs import Slot, UserAvail, match_avails_to_slots, generate_graph, mapping_to_results
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

# sample
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Adds a user to the database
    """
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
    """
    Retrieves all users in the database
    """
    result = db.session.query(User).all()
    return jsonify([user.to_dict() for user in result]), 200

@app.route('/api/user/teams', methods=['GET'])
def get_user_teams():
    """
    Retrieves all the teams a given user belongs to
    """
    user_email = request.args.get("userEmail")
    user_teams = []

    user = db.session.query(User).filter_by(email=user_email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    for t in user.leading_teams:
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

    return jsonify(teams), 200

@cross_origin()
@app.route('/api/team', methods=['GET'])
def get_team():
    """
    Retrieves team information given user email and team id
    """
    # stub_data = {
    #     "teamId": 1,
    #     "schedule": {
    #         "slotAssignments": [
    #             {
    #                 "slot": {
    #                     "name": "L2D",
    #                     "slotId": 4,
    #                     "numMembers": 3,
    #                     "startBlock": 34,
    #                     "endBlock": 40
    #                 },
    #                 "members": [
    #                     {
    #                         "name": "Matthew Kang",
    #                         "email": "matt0410@student.ubc.ca"
    #                     },
    #                     {
    #                         "name": "William Xiao",
    #                         "email": "munce@student.ubc.ca"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "slot": {
    #                     "name": "L2G",
    #                     "slotId": 7,
    #                     "numMembers": 2,
    #                     "startBlock": 20,
    #                     "endBlock": 25
    #                 },
    #                 "members": [
    #                     {
    #                         "name": "Susan Chung",
    #                         "email": "susan328@student.ubc.ca"
    #                     },
    #                     {
    #                         "name": "Kevin Zhou",
    #                         "email": "kevz21@student.ubc.ca"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "slot": {
    #                     "name": "L2H",
    #                     "slotId": 9,
    #                     "numMembers": 3,
    #                     "startBlock": 600,
    #                     "endBlock": 601
    #                 },
    #                 "members": [
    #                     {
    #                         "name": "Matthew Kang",
    #                         "email": "matt0410@student.ubc.ca"
    #                     }
    #                 ]
    #             }
    #         ]
    #     },
    #     "availability": {
    #         "userEmail": "kevz21@student.ubc.ca",
    #         "availableBlocks": [16, 17, 18, 19, 20, 21, 22, 104, 110],
    #         "preferNotBlocks": [23, 24, 25, 35, 36, 37, 600]
    #     },
    #     "slots": {
    #         "slots": [
    #             {
    #                 "name": "L2A",
    #                 "slotId": 1,
    #                 "numMembers": 2,
    #                 "startBlock": 34,
    #                 "endBlock": 40
    #             },
    #         {
    #             "name": "L2D",
    #             "slotId": 4,
    #             "numMembers": 3,
    #             "startBlock": 34,
    #             "endBlock": 40
    #         },
    #         {
    #             "name": "L2E",
    #             "slotId": 6,
    #             "numMembers": 3,
    #             "startBlock": 18,
    #             "endBlock": 24
    #         },
    #         {
    #             "name": "L2G",
    #             "slotId": 7,
    #             "numMembers": 2,
    #             "startBlock": 20,
    #             "endBlock": 25
    #         },
    #         {
    #             "name": "L2H",
    #             "slotId": 9,
    #             "numMembers": 3,
    #             "startBlock": 600,
    #             "endBlock": 601
    #         }
    #     ]
    #     },
    #     "teamInfo": {
    #         "name": "My Awesome Team",
    #         "leaders": [
    #             {
    #                 "name": "Gregor Kiczales",
    #                 "email": "gregor@cs.ubc.ca"
    #             }
    #         ],
    #         "members": [
    #             {
    #                 "name": "Susan Chung",
    #                 "email": "susan328@student.ubc.ca"
    #             },
    #             {
    #                 "name": "Matthew Kang",
    #                 "email": "matt0410@student.ubc.ca"
    #             },
    #             {
    #                 "name": "Kevin Zhou",
    #                 "email": "kevz21@student.ubc.ca"
    #             },
    #             {
    #                 "name": "William Xiao",
    #                 "email": "munce@student.ubc.ca"
    #             }
    #         ]
    #     }
    # }
    team_id = request.args.get('teamId')
    email = request.args.get('userEmail')

    team = db.session.query(Team).filter_by(id=team_id).first()
    if not team:
        return jsonify({"error": "Team not found"}), 404

    team_info = {
        "teamId": team.id,
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


    if email in [member.email for member in team.members]:
        member_info = db.session.query(MemberTeamInfos).filter(and_(MemberTeamInfos.team_id==team.id, MemberTeamInfos.user_email==email)).first()
        avail_result = {
            "userEmail": email
        }
        if member_info.available_blocks:
            avail_result["availableBlocks"] = json.loads(member_info.available_blocks)
        else:
            avail_result["availableBlocks"] = []
        if member_info.prefer_not_blocks:
            avail_result["preferNotBlocks"] = json.loads(member_info.prefer_not_blocks)
        else:
            avail_result["preferNotBlocks"] = []
        team_info["availability"] = avail_result

    if team.slots:
        team_info["slots"] = team.slots
    else:
        team_info["slots"] = None


    return jsonify(team_info)

@app.route('/api/team', methods=['POST'])
def create_single_team():
    """
    Creates a new team with a leader given a team name and user email
    """
    req = request.json
    user_email = req['userEmail']
    team_name = req['teamName']
    leader = db.session.query(User).filter_by(email=user_email).first()
    if not leader:
        return jsonify({"error": "Leader not found"}), 404
    leaders_input = [leader]
    members_input = []
    new_team = Team(name=team_name, leaders=leaders_input, members=members_input)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"teamId": new_team.id}), 200

@app.route('/api/team/leader', methods=['POST'])
def add_leader():
    """
    Adds a new leader to an existing team
    """
    error_response = {
        "error": "User with given email is already on the team"
    }

    req = request.json

    team_id = req['teamId']
    leader_email = req['leader']['email']

    user = db.session.query(User).filter_by(email=leader_email).first()

    for t in user.leading_teams:
        if t.id == team_id:
            return jsonify(error_response), 400
        
    for t in user.member_teams:
        if t.id == team_id:
            return jsonify(error_response), 400
    
    team = db.session.query(Team).filter_by(id=team_id).first()
    team.leaders.append(user)

    db.session.commit()
    return jsonify({"teamId":team_id,"leader":{"name": user.name,"email": user.email}}), 200

@app.route('/api/team/member', methods=['POST'])
def add_member():
    """
    Adds a new member to an existing team
    """
    error_response = {
        "error": "User with given email is already on the team"
    }

    req = request.json

    team_id = req['teamId']
    member = req['member']
    member_email = member['email']

    user = db.session.query(User).filter_by(email=member_email).first()

    if user.leading_teams:
        for t in user.leading_teams:
            if t.id == team_id:
                return jsonify(error_response), 400

    if user.member_teams:
        for t in user.member_teams:
            if t.id == team_id:
                return jsonify(error_response), 400
        
    db.session.add(MemberTeamInfos(team_id=team_id, user_email=member_email, max_blocks=3))

    team = db.session.query(Team).filter_by(id=team_id).first()
    team.members.append(user)

    db.session.commit()
    return jsonify({"teamId":team_id,"member":{"name": user.name,"email": user.email}}), 200


@app.route('/api/team/member/availability', methods=['POST'])
def update_availability():
    """ 
    Updates availability of a member for a team 
    """
    req = request.json

    team_id = req['teamId']
    user_email = req['userEmail']
    available_blocks = req['availableBlocks']
    prefer_not_blocks = req['preferNotBlocks']

    table_entry = db.session.query(MemberTeamInfos).filter(and_(MemberTeamInfos.team_id == team_id, MemberTeamInfos.user_email == user_email)).first()

    if not table_entry:
        return jsonify({"error": "Please double check the given team id and user email"}), 400
    else:
        table_entry.available_blocks = available_blocks
        table_entry.prefer_not_blocks = prefer_not_blocks
    
    db.session.commit()
    return req, 200
        
    


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

# @app.route('/api/teams', methods=['POST'])
# def create_team():
#     data = request.json

#     user_email = data['userEmail']
#     team_name = data['teamName']
#     leaders_input = [db.session.query(User).filter_by(email=user_email).first()]
#     members_input = []
#     # if 'leaders' in data:
#     #     leader_emails = data['leaders']
#     #     for email in leader_emails:
#     #         print(email)
#     #         leaders_input += [db.session.query(User).filter_by(email=email).first()]
#     # if 'members' in data:
#     #     members_emails = data['members']
#     #     for email in members_emails:
#     #         print(email)
#     #         members_input += [db.session.query(User).filter_by(email=email).first()]
#     new_team = Team(name=team_name, leaders=leaders_input, members=members_input)
#     print(new_team)
#     db.session.add(new_team)
#     db.session.commit()
#     return jsonify({"teamId": new_team.id}), 200

# @app.route('/api/teams', methods=['GET'])
# def get_teams():
#     result = db.session.query(Team).all()
#     return jsonify([team.to_dict() for team in result]), 200


@app.route('/api/schedule', methods=['PUT'])
def generate_schedule():
    """
    Creates the schedule for a given team
    """
    id = request.args.get("id")
    team = db.session.query(Team).filter_by(id=id).first()

    member_infos = [db.session.query(MemberTeamInfos).filter_by(team_id=id, user_email=member.email).first() for member in team.members]

    user_avails = []
    slots = []
    for mem_info in member_infos:
        avail = UserAvail(mem_info.user_email, json.loads(mem_info.available_blocks), json.loads(mem_info.prefer_not_blocks), mem_info.max_blocks)
        user_avails += [avail]

    dejsoned_slots = json.loads(team.slots)
    for slot in dejsoned_slots:
        slot_obj = Slot(slot.name, slot.slotId, slot.numMembers, slot.startBlock, slot.endBlock)
        slots += [slot_obj]

    result = match_avails_to_slots(user_avails, slots)
    # [print(f"email is {user.email} available slots are {[f"id = {s.slot_id}; pref = {s.prefer_level}" for s in user.avail_slots]}") for user in result]
    graph = generate_graph(result, slots)
    # print(graph)
    result = nx.max_flow_min_cost(graph, "source", "sink")
    final_schedule = mapping_to_results(result, user_avails)

    # TODO: transfer schedule
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
    Session = sessionmaker(bind=db.engine)
    session = Session()
    if target.leaders:
        for leader in target.leaders:
            # leader = User.query.get(leader_email)
            leader_obj = db.session.query(User).filter_by(email=leader.email).first()
            if leader_obj:
                leader_obj.leading_teams.append(target)
    if target.members:
        for member in target.members:
            # member = User.query.get(member_email)
            member_obj = db.session.query(User).filter_by(email=member.email).first()
            if member_obj:
                member_obj.member_teams.append(target)
    session.commit()

    



def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    init_db()
    if os.environ.get("IS_PRODUCTION") != 1:
        app.run(debug=True)
    