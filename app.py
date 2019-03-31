from flask import Flask,redirect, url_for, request, Response,jsonify,render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import (JWTManager,create_access_token,
create_refresh_token, jwt_required, jwt_refresh_token_required,
get_jwt_identity, get_raw_jwt)
from sys import stdout
from makeup_artist import Makeup_artist
from camera import Camera
from utilss import base64_to_pil_image, pil_image_to_base64
import base64
import re
####
import os
import json
import face_recognition
import utils
import datetime
from functools import wraps

app = Flask(__name__,template_folder='template')
#api = Api(app)
socketio = SocketIO(app)
#sslify = SSLify(app)
CORS(app, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = 'kycface2019_token'

jwt = JWTManager(app)



#Identifica la carpeta donde se dejaran las fotografias que se suben
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

kycfaceid= utils.kycfaceid


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kycface/creargrupo')
def creargrupo():
    return render_template('creargrupo.html')

@app.route('/kycface/crearusuario')
def crearusuario():
    return render_template('crearusuario.html')

@app.route('/kycface/enrolarusuario')
def enrolarusuario():
    return render_template('enrolarusuario.html')

@app.route('/kycface/anadircara')
def anadircara():
    return render_template('anadircara.html')

@app.route('/kycface/detectarrostro')
def detectarrostro():
    return render_template('detectarrostro.html')

@app.route('/kycface/stream')
def stream():
    return render_template('stream.html')



@socketio.on('input image', namespace='/kycface/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)    

@socketio.on('connect', namespace='/kycface/test')
def test_connect():
    app.logger.info("client connected")

def gen():    
    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame()         
        yield (frame)


@app.route('/kycface/video_feed')
def video_feed(): 
    verifica="v0"
    try:
        verifica="v1"
        b64_bytes = base64.b64encode(gen())
        verifica="v2"
        b64_string = b64_bytes.decode()
        verifica="v3"
        verifica = kycfaceid.userFaceAuth(b64_string)
    
        return  Response(verifica)
    
    except Exception as inst:
        return Response(verifica)
    
     


@app.route('/kycfaceid/group/adduser', methods=['POST'])
@jwt_required
def groupAddUser():
    groupid = request.form['groupId']
    userid = request.form['userId']
            
    verifica = kycfaceid.groupAddUser(groupid,userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/create', methods=['POST'])
@jwt_required
def groupCreate():    
    groupname = request.form['groupName']
    access = request.form['sizeLimit']
            
    verifica = kycfaceid.groupCreate(groupname, access)
   
    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')
    
    return  resp

@app.route('/kycfaceid/group/edit', methods=['POST'])
@jwt_required
def groupEdit():
    groupid = request.form['groupId']
    groupmame = request.form['groupName']
    size = request.form['sizeLimit']
            
    verifica = kycfaceid.groupEdit(groupid, groupmame,size)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/get', methods=['POST'])
@jwt_required
def groupGet():
    groupid = request.form['groupId']
        
    verifica = kycfaceid.groupGet(groupid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/list', methods=['GET','POST'])
@jwt_required
def groupList():
        
    verifica = kycfaceid.groupList()

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/listuser', methods=['GET','POST'])
@jwt_required
def groupListUser():
    userif=None
    if request.method == 'POST':
        userid = request.form['userId']    
    else:
        userid = request.args.get('userId')

    verifica = kycfaceid.groupListUser(userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/listusers', methods=['POST'])
@jwt_required
def groupListUsers():
    groupid = request.form['groupId']
    userid = request.form['userId']
    grouprole = request.form['groupRole']
        
    verifica = kycfaceid.groupListUsers(groupid,userid,grouprole)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/remove', methods=['POST'])
@jwt_required
def groupRemove():
    groupid = request.form['groupId']  
        
    verifica = kycfaceid.groupRemove(groupid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/removeuser', methods=['POST'])
@jwt_required
def groupRemoveUser():
    groupid = request.form['groupId']  
    userid = request.form['userId']  
        
    verifica = kycfaceid.groupRemoveUser(groupid, userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/group/userrole', methods=['POST'])
@jwt_required
def groupUserRole():
    groupid = request.form['groupId']  
    userid = request.form['userId']
    grouprole = request.form['groupRole']  
        
    verifica = kycfaceid.groupUserRole(groupid, userid, grouprole)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/addface', methods=['POST'])
@jwt_required
def userAddFace():
    try:
               
        data_url = request.form['image']
        userId = request.form['userId']
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = data_url
        image_data = dataUrlPattern.match(image_data).group(2)
        image_data = image_data.encode()
        image_data = base64.b64decode(image_data)
 
        img = "/var/www/flask/face/faces/imageToSave.jpg"
        with open(img, 'wb') as f:
            f.write(image_data)
             
        verifica = kycfaceid.userAddFace(img, userId)
        
        js = json.dumps(verifica, indent=2)
        resp = Response(js, status=200, mimetype='application/json')
        
        return  resp
    except Exception as inst:
        return Response(inst.args)
    

@app.route('/kycfaceid/user/auth', methods=['POST'])
@jwt_required
def userAuth():
    userid = request.form['userId']     
    otp = request.form['otp']  
        
    verifica = kycfaceid.userAuth(userid, opt)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/create', methods=['POST'])
@jwt_required
def userCreate():
    name = request.form['name']
    lastname = request.form['lastname']              
    details = request.form['details'] 
    phone = resquest.form['phone']    

    verifica = kycfaceid.userCreate(name,lastname,details,phone)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/edit', methods=['POST'])
@jwt_required
def userEdit():
    userid = request.form['userId']      
    details = request.form['details']  

    verifica = kycfaceid.userEdit(userid, details)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/renroll', methods=['POST'])
@jwt_required
def userEnroll():
    userid = request.form['userId']      
    details = request.form['details']  
    groupid = request.form['groupId']  
    face1 = request.files['face1'] 
    face2 = request.files['face2'] 

    verifica = kycfaceid.userEnroll(userid, details, groupid, face1, face2)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/get', methods=['POST'])
@jwt_required
def userGet():
    userid = request.form['userId']         

    verifica = kycfaceid.userGet(userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/getopt', methods=['POST'])
@jwt_required
def userGetOTP():
    userid = request.form['userId']         

    verifica = kycfaceid.userGetOTP(userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/faceauth', methods=['POST'])
@jwt_required
def userFaceAuth():
    userid = request.form['userId']     
    file = request.files['image']  
    
    f = os.path.join("/root/work/face/", file.filename)
    

    file.save(f)

    verifica = kycfaceid.userFaceAuth(f, userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/remove', methods=['POST'])
@jwt_required
def userRemove():
    userid = request.form['userId']     
           
    verifica = kycfaceid.userRemove(userid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/removeface', methods=['POST'])
@jwt_required
def userRemoveFace():
    userid = request.form['userId']   
    faceid = request.form['faceId']   
           
    verifica = kycfaceid.userRemoveFace(userid,faceid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/role', methods=['POST'])
@jwt_required
def userRole():
    roles = request.form['roles']   
    userid = request.form['userId']   
           
    verifica = kycfaceid.userRole(userid,faceid)

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/user/list', methods=['POST'])
@jwt_required
def userList():

    verifica = kycfaceid.userList()

    js = json.dumps(verifica, indent=2)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp


@app.route('/kycfaceid/image/recognize', methods=['POST'])
def recognize():
    try:
        data_url = request.form['image']
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = data_url
        image_data = dataUrlPattern.match(image_data).group(2)
        image_data = image_data.encode()
        image_data = base64.b64decode(image_data)
 
        img = "/var/www/flask/face/faces/recon.jpg"
        with open(img, 'wb') as f:
            f.write(image_data)
     
        verifica = kycfaceid.recognize(img)
        

        js = json.dumps(verifica, indent=2)
        resp = Response(js, status=200, mimetype='application/json')
     
        return  resp
    except Exception as inst:
        return Response(retorna)

@app.route('/kycfaceid/image/verify', methods=['POST'])
def verify():
    file = request.files['image']
    userid = request.form['userid']

    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
    file.save(f)


    verifica = kycfaceid.verify(f, userId)

    js = json.dumps(verifica)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/login', methods=['POST','GET'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



if __name__ == "__main__":
 socketio.run(app,ssl_context='adhoc',debug=True)
 
