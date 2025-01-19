from datetime import datetime
from models.database import db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Define User Table
class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    leading_teams = db.relationship('Team', secondary='team_leaders', backref='team_leader_relation')
    member_teams = db.relationship('Team', secondary='team_members', backref='team_member_relation')

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'leading_teams': [user.to_dict() for user in self.leading_teams],
            'member_teams': [user.to_dict() for user in self.member_teams]
        }
