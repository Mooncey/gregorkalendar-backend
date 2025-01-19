from datetime import datetime
from models.database import db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

class MemberTeamInfos(db.Model):
    __tablename__ = 'member_team_infos'
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)
    user_email = db.Column(db.String(120), db.ForeignKey('users.email'), primary_key=True)
    availbility = db.Column(db.JSON, nullable=False)
    max_blocks = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'team_id': self.team_id,
            'user_email': self.user_email,
            'availbility': self.availbility,
            'max_blocks': self.max_blocks
        }