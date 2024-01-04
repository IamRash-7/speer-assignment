from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify

from src.models import Notes
from src.init import db

def get_current_user_id():
    return get_jwt_identity()

def get_note_controller(id):
    user_id = get_current_user_id()

    # List Notes
    note = Notes.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    return jsonify(note.serialize()), 200

def update_note_controller(id):
    user_id = get_current_user_id()
    data = request.get_json()

    note = Notes.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    # Update the note with new data
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)

    db.session.commit()

    return jsonify({'message': 'Note updated successfully'}), 200


def delete_note_controller(id):
    user_id = get_current_user_id()

    note = Notes.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    # Delete the note
    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200