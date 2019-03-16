import requests
import os
import json
#Libreria de face_recognition, para realizar el test
import face_recognition

class kycfaceid:

  def userFaceAuth(faceFilePath, userId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}

    try:
      #Reconocimiento por medio de la libreria face_recognition
      image_entry = face_recognition.load_image_file(faceFilePath)
      entry_encoding = face_recognition.face_encodings(image_entry)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)
      #--------------------------------------------------------

      #Construccion del arreglo para respuesta
      data = {
        'validate': str(response[0]),
        'faceid' : 3,
        'personId': 0,
        'label': str(faceFilePath)
       }
       #-------------------------------------

    except Exception as e:
      return str(e)

    return data


  def userCreate(userId, details):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(details) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}

    try:
     response = 'none'
    except Exception as e:
      return str(e)

    return response


  def userAddFace(faceFilePath, userId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}

    try:
     response = 'none'
    except Exception  as e:
      return str(e)

    return response

  def recognize(faceFilePath, groupId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(groupId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}

    try:
      #Reconocimiento por medio de la libreria face_recognition
      image_entry = face_recognition.load_image_file(faceFilePath)
      entry_encoding = face_recognition.face_encodings(image_entry)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)
      #--------------------------------------------------------
      
      #Construccion del arreglo para respuesta          
      data = {
        'validate': str(response[0]),
        'faceid' : 3,
        'personId': 0,
        'label': str(faceFilePath)
       }
      #--------------------------------------

    except Exception as e:
      return str(e)

    return data

  def verify(faceFilePath, userId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    
    try:
      #Reconocimiento por medio de la libreria face_recognition
      image_entry = face_recognition.load_image_file(faceFilePath)
      entry_encoding = face_recognition.face_encodings(image_entry)[0]

      unknown_picture = face_recognition.load_image_file("foto.jpg")
      unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

      response = face_recognition.compare_faces([entry_encoding], unknown_face_encoding)
      #---------------------------------------------------------------------------

      #Construccion del arreglo para respuesta
      data = {
        'validate': str(response[0]),
        'faceid' : userId,
        'personId': 0,
        'label': str(faceFilePath)
       }
       #-------------------------------------

    except Exception  as e:
      return str(e)

    return data
