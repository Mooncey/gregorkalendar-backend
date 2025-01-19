from datetime import datetime
from models.database import db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Team table
class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    # leaders = db.relationship('User', secondary='team_leaders', backref='users.leading_teams')
    # members = db.relationship('User', secondary='team_members', backref='users.member_teams')
    leaders = db.relationship('User', secondary='team_leaders', backref=db.backref('team_leader_relation', lazy='dynamic'))
    members = db.relationship('User', secondary='team_members', backref=db.backref('team_member_relation', lazy='dynamic'))
    schedule = db.Column(db.JSON, nullable=True)
    slots = db.Column(db.JSON, nullable=False)
    
    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'leaders': [{"name": leader.name, "email": leader.email} for leader in self.leaders],
            'members': [{"name": member.name, "email": member.email} for member in self.members]
        }
        if self.schedule:
            result['schedule'] = self.schedule
        if self.slots:
            result['slots'] = self.slots

        return result
