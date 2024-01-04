from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify

from src.models import Notes, User
from src.init import db

def get_current_user_id():
    return get_jwt_identity()

def list_notes_controller():
    user_id = get_current_user_id()

    # List owned notes
    owned_notes = Notes.query.filter_by(user_id=user_id).all()

    # List shared notes
    user = User.query.get(user_id)
    shared_notes = user.shared_notes

    all_notes = owned_notes + shared_notes
    return jsonify(notes=[note.serialize() for note in all_notes]), 200

def create_notes_controller():
    user_id = get_current_user_id()
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    # Create a new note
    new_note = Notes(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully', 'note_id': new_note.id}), 201