from src.init import app

from flask_jwt_extended import jwt_required
from flask import request

from src.apis.authentication import login_controller, signup_controller
from src.apis.all_notes import list_notes_controller, create_notes_controller
from src.apis.each_note import get_note_controller, update_note_controller, delete_note_controller
from src.apis.search_notes import search_note_controller
from src.apis.share_notes import share_note_controller

@app.route('/') 
def base_welcome(): 
    return 'Welcome'

@app.route('/api/auth/signup', methods = ['POST']) 
def post_signup_api(): 
    return signup_controller()

@app.route('/api/auth/login', methods = ['POST']) 
def post_login_api(): 
    return login_controller()

@app.route('/api/notes', methods = ['POST', 'GET']) 
@jwt_required()
def all_notes_api():
    if request.method == "GET":
        return list_notes_controller()
    elif request.method == "POST":
        return create_notes_controller()
    
@app.route('/api/notes/<id>', methods = ['GET', 'PUT', 'DELETE']) 
@jwt_required()
def each_note_api(id):
    if request.method == "GET":
        return get_note_controller(id)
    if request.method == "PUT":
        return update_note_controller(id)
    if request.method == "DELETE":
        return delete_note_controller(id)
    
@app.route('/api/search', methods=['GET'])
@jwt_required()
def search_notes():
    return search_note_controller()

@app.route('/api/notes/<id>/share', methods = ['POST']) 
@jwt_required()
def share_note_api(id):
    return share_note_controller(id)