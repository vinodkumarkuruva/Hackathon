import os
from flask import request, jsonify
from .models import User,Hackathon
from Hack import db,app
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

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
        login_user(user)
        return jsonify({"message":"login successfully completed"}),200
    return jsonify({"alert":"email or password is incorrect"}),400

@app.route('/update' , methods=['POST'])
@login_required
def update():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_user.check_password(current_password):
        return jsonify({"error": "Incorrect current password"}), 401
    password_hash = generate_password_hash(new_password)
    current_user.password_hash = password_hash
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

@app.route('/logout',methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    else:
        return jsonify({"error": "Already logged out"}), 400

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
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    
@app.route('/hackathon/create', methods=['POST'])
def create_hackathon():
    data = request.form
    start_datetime = datetime.utcnow()
    end_datetime = start_datetime + timedelta(days=7)
    hackathon = Hackathon.query.filter_by(title=data['title']).first()
    if hackathon:
        return jsonify({'alert':'Title already there please choose different title'}),400
    file = request.files.get('image')
    a = upload_image(file)
    b = upload_image(file)
    hackathon = Hackathon(
        title=data['title'],
        description=data['description'],
        background_image=a,
        Hackathon_image =b,
        start_datetime = start_datetime,
        end_datetime=end_datetime,
        reward_prize=data['reward_prize'],
        creator_id=current_user.id)
    db.session.add(hackathon)
    db.session.commit()

    return jsonify({'message': 'Hackathon created successfully'}), 201

@app.route('/delete_hack' , methods=['DELETE'])
def delete_hack():
    data = request.json
    title = data['title']
    Hack1 = Hackathon.query.filter_by(title=title).first()

    if not Hack1:
        return jsonify({"error": "Hackathon not found"}), 404
    if Hack1:
        if current_user.id == Hack1.creator_id:
            db.session.delete(Hack1)
            db.session.commit()
            return jsonify({"msg":" deleted Hackathon "}),200
        else:
            return jsonify({"msg":" Your are not allowed to delete.You are not the owner to delete !"}),400
    return jsonify({"alert":"Invalid Title !"}),400

@app.route('/hackathon_all' , methods=['GET'])
def hackathon_all():
    hackathonss = Hackathon.query.all()
    users = [{
        "Title":h1.title,
        "Start_date":h1.start_datetime,
        "End_date":h1.end_datetime,
        "Reward_prize":h1.reward_prize,
        "image":h1.Hackathon_image,
        "owner":h1.creator.username}
    for h1 in hackathonss]
    return jsonify({'Hackathons': users}), 200

@app.route('/hackathon_by_username/<string:username>' , methods=['GET'])
def hackathon_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [{
        "Title":h1.title,
        "Start_date":h1.start_datetime,
        "End_date":h1.end_datetime,
        "Reward_prize":h1.reward_prize,
        "image":h1.Hackathon_image}
    for h1 in user.hackathons]
    return jsonify({'Hackathons': users}), 200


########## REGISTER ##############

