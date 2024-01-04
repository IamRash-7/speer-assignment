from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify

from src.models import Notes, User
from src.init import db

def get_current_user_id():
    return get_jwt_identity()

def share_note_controller(id):
    user_id = get_current_user_id()
    data = request.get_json()
    note = Notes.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({'message': 'Note not found'}), 404

    # Retrieve the user by username to share the note with
    username_to_share_with = data.get('username')
    user_to_share_with = User.query.filter_by(username=username_to_share_with).first()

    if not user_to_share_with:
        return jsonify({'message': 'User to share with not found'}), 404

    # Check if the note is already shared with the user
    if user_to_share_with in note.shared_with:
        return jsonify({'message': 'Note already shared with the user'}), 400

    # Share the note with the user
    note.shared_with.append(user_to_share_with)
    db.session.commit()

    return jsonify({'message': 'Note shared successfully'}), 200