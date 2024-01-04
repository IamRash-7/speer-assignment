from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify

from src.models import Notes
from src.init import db

def get_current_user_id():
    return get_jwt_identity()

def search_note_controller():
    user_id = get_current_user_id()
    query = request.args.get('q', '')
    
    notes = Notes.query.filter(
        (Notes.title.ilike(f'%{query}%') | Notes.content.ilike(f'%{query}%')) & (Notes.user_id == user_id)
    ).all()

    return jsonify(notes=[note.serialize() for note in notes]), 200
