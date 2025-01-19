from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)

# Define a simple User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


@app.route('/api/users', methods=['GET'])
def get_users():
    result = db.session.query(User).all()
    return jsonify([user.to_dict() for user in result]), 200

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

    return jsonify(stub_data)

@app.route('/api/team', methods=['POST'])
def create_team():
    # TODO
    return jsonify({
    "teamId": 110
    })

@app.route('/api/member/team', methods=['GET'])
def get_member_teams():
    # TODO
    stub_data = {
        "teams": [
            {
                "teamName": "My Awesome Team",
                "teamId": 1
            },
            {
                "teamName": "Frontend Team",
                "teamId": 2
            },
            {
                "teamName": "Backend Team",
                "teamId": 3
            },
            {
                "teamName": "CPSC 110 2024W2",
                "teamId": 4
            }
        ]
    }
    return jsonify(stub_data)


def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    app.run(debug=True)
    