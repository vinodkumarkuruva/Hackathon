from flask import request, jsonify
from .models import User,Hackathon
from Hack import db,app
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash


######### USERS #######
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data['username'] or not data['email'] or not data['password']:
        return jsonify({'message': 'Missing fields'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"error": " Email already registered! Please use different Email !" }), 400
    user = User(username=data['username'], email=data['email'],
                password_hash=generate_password_hash(data['password']),
                is_authorized = True )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login' , methods=['POST'])
def login():
    data = request.json
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(data['password']):
        return jsonify({"message":"login successfully completed"}),200
    return jsonify({"alert":"email or password is incorrect"}),400

@app.route('/signup_users' , methods=['GET'])
def all_users():
    userss = User.query.all()
    users = [{
        "email":user.email,
        "username":user.username,
        "authorized":user.is_authorized}
    for user in userss]
    return jsonify({'signup_users': users}), 200

@app.route('/delete' , methods=['DELETE'])
def delete():
    data = request.json
    email = data['email']
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
 
    if user and user.check_password(data['password']):
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg":"deleted account"}),200
    return jsonify({"alert":"Invalid email or password ! "}),400
    

#############Hackathons###########

@app.route('/hackathons/create', methods=['POST'])
@jwt_required()
def create_hackathon():

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user.is_authorized:
        return jsonify({'message': 'Unauthorized user'}), 403

    data = request.get_json()
    start_datetime = datetime.utcnow()
    end_datetime = start_datetime + timedelta(days=7)

    hackathon = Hackathon.query.filter_by(title=data['title']).first()

    if hackathon:
        return jsonify({'alert':'Title already there please choose different title'}),400
    
    type = data["type_of_submission"]
    if type not in ('link','image','file'):
        return jsonify({'alert':'Please check the type of file'})
    
    hackathon = Hackathon(
        title=data['title'],
        description=data['description'],
        background_image=data['background_image'],
        hackathon_image=data['hackathon_image'],
        type_of_submission=data['type_of_submission'],
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        reward_prize=data['reward_prize'],
        creator_id=current_user_id
    )
    
    db.session.add(hackathon)
    db.session.commit()

    return jsonify({'message': 'Hackathon created successfully'}), 201
