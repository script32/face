import os
import json
import face_recognition
from flask import Flask,redirect, url_for, request, Response
from flask_restful import Api, Resource, reqparse
import utils
#Python para implementar microservicios

app = Flask(__name__)
api = Api(app)

#Identifica la carpeta donde se dejaran las fotografias que se suben
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

kycfaceid= utils.kycfaceid

@app.route('/kycfaceid/recognize', methods=['POST'])
def recognize():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
    file.save(f)

    verifica = kycfaceid.recognize(f, "groupId")

    js = json.dumps(verifica)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp

@app.route('/kycfaceid/verify', methods=['POST'])
def verify():
    file = request.files['image']
    userid = request.form['userid']

    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
    file.save(f)

    verifica = kycfaceid.verify(f, userId)

    js = json.dumps(verifica)
    resp = Response(js, status=200, mimetype='application/json')

    return  resp


        
if __name__ == "__main__":
 app.run(host='0.0.0.0')
