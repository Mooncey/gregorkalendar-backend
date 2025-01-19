from datetime import datetime
from models.database import db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

team_leaders = db.Table('team_leaders',
                        db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
                        db.Column('user_email', db.String(120), db.ForeignKey('users.email'), primary_key=True))

team_members = db.Table('team_members',
                        db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
                        db.Column('user_email', db.String(120), db.ForeignKey('users.email'), primary_key=True))