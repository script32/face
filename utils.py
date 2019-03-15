import requests
import os
import json
import face_recognition


class kycfaceid:

  def userFaceAuth(userId, faceFilePath):
    if((not os.path.exists(faceFilePath))): return {"error":"invalid_input", "message" : faceFilePath+" does not exist"}
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    
    try:
      
      image_entry = face_recognition.load_image_file(files=dict(image=open(faceFilePath)))
      entry_encoding = face_recognition.face_encodings(image_cristian)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
      
      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)

    except requests.exceptions.RequestException as e:
      print e

    return json.loads(response.text)

  
  def userCreate(userId, details):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(details) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}
    
    try:
     #response = requests.post(self.url+"user/create", json=payload, headers=headers)
    except requests.exceptions.RequestException as e:
      print (e)

    return json.loads(response.text);


  def userAddFace(userId, faceFilePath):
    if((not os.path.exists(faceFilePath))): return {"error":"invalid_input", "message" : faceFilePath+" does not exist"}
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    
    try:
      #response = requests.post(self.url+"user/addFace", files=dict(image=open(faceFilePath)), data=dict(userId=userId), headers=headers);
    except requests.exceptions.RequestException as e:
      print e

    return json.loads(response.text)


  def recognize(faceFilePath, groupId):
    if((not os.path.exists(faceFilePath))): return {"error":"invalid_input", "message" : faceFilePath+" does not exist"}
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupId must be a string"}
    
    try:

      image_entry = face_recognition.load_image_file(files=dict(image=open(faceFilePath)))
      entry_encoding = face_recognition.face_encodings(image_cristian)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
      
      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)

    except requests.exceptions.RequestException as e:
      print (e)

    return json.loads(response.text)


  def verify(faceFilePath, userId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
   

    try:

      image_entry = face_recognition.load_image_file(files=dict(image=open(faceFilePath)))
      entry_encoding = face_recognition.face_encodings(image_cristian)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
      
      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)

   
    except requests.exceptions.RequestException as e:
      print (e)

    return json.loads(response.text)


