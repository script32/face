import requests
import os
import io
import json
import jsonify
#Libreria de face_recognition, para realizar el test
import face_recognition
import crud
import datetime
import encode_face
import recognize_faces_image
import psycopg2 as psql
import numpy as np
import traceback
from flask_jwt_extended import create_access_token

crudOperation = crud.CRUD()
faceEncode = encode_face.encod()
faceRecognizaImage = recognize_faces_image.matchFace()

class kycfaceid:

  #Funciones Group 
  def groupAddUser(groupId, userId):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupId must be a string"}
    
    try:
      dt = datetime.datetime.now();
      lastid = crudOperation.insertData("""insert into kycface."userGroup"("groupId","userId","dateCreate") values(%s,%s,%s)""",(groupId,userId,dt))
      
      retorno = None

      if(lastid<=0):
        retorno = False
      else:
        retorno = True

      data = {
        'result': retorno        
       }

    except requests.exceptions.RequestException as e:
      return e


    return data;

  def groupCreate(groupName,sizeLimit):
    if(type(groupName) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}
    if(type(sizeLimit) is not str): return {"error" : "invalid_input", "message" : "sizeLimit must be a string"}
      
    try:
      dt = datetime.datetime.now();

      lastid = crudOperation.insertData("""insert into kycface."groupTb"("groupName","sizeLimit","state","dateCreate") values(%s,%s,%s,%s)""",(groupName,sizeLimit,0,dt))
     
    except requests.exceptions.RequestException as e:
      return e
    
    return lastid;

  def groupEdit(groupId,groupName,sizeLimit):
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupId must be a string"}
    if(type(groupName) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}
    if(type(sizeLimit) is not str): return {"error" : "invalid_input", "message" : "sizeLimit must be a string"}
            
    try:
      rets=None

      rowsUpdate = crudOperation.updateData("""update kycface."groupTb" set "groupName"=%s,"sizeLimit"=%s where "groupId"=%s """,(groupName,sizeLimit,groupId))

      if(lastid<=0):
        rets = False
      else:
        rets = True

      data = {
        'result': rets        
       } 

    except requests.exceptions.RequestException as e:
      return e

    return data;

  def groupGet(groupId):
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}
      
    try:
        
        dataGroup = crudOperation.returnData("""select "groupName","sizeLimit" from kycface."groupTb" where 'groupId'=""" + groupId)

        dataUser = crudOperation.returnData("""select "userId","groupRole" from kycface."userRole" where 'groupId'=""" + groupId)
        
        data = {
          'result':{
            dataGroup,dataUser
          }
        }

    except requests.exceptions.RequestException as e:
      return e
    return data;

  def groupList():

    try:
      dataGroups = crudOperation.returnData("""select "groupId","groupName","sizeLimit" from kycface."groupTb" where "state"=0 """)
      
      data = {
        'result':{
         'groups': dataGroups
        }
      }

    except requests.exceptions.RequestException as e:
      return e
    return data;

  def groupListUser(userId):
    try:
      dataUsers = crudOperation.returnData("""select a."groupId",a."groupName",a."sizeLimit" from kycface."groupTb" as a, kycface."userGroup" as b
      where b."userId"=""" + userId + """ and a."groupId" = b."groupId" and  a."state"=0""")
      
      data = {
      'result': dataUsers
      }

    except requests.exceptions.RequestException as e:
      return e
    return data;

  def groupRemove(groupId):
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}

    try:
      rets = None
      deleteGroupUser = crudOperation.returnData("""delete from kycface."userGroup" where groupId=%s""",(groupId))
      deleteGroup = crudOperation.returnData("""delete from kycface."groupTb" where groupId=%s""",(groupId))
      
      if(deleteGroup > 0) and (deleteGroupUser >= 0):
        rets = True
      else:
        rets = False
        
      data = {
        'result': rets        
       }
    except requests.exceptions.RequestException as e:
      return e
    return data;

  
  def groupRemoveUser(groupId,userId):
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}
      
    try:
      rets = None
      deleteGroup = crudOperation.returnData("""delete from kycface."userGroup" where "userId"=%d and groupId=%s""",(userId,groupId))
      
      if(deleteGroup > 0):
        rets = True
      else:
        rets = False

      data = {
        'result': rets        
       }
    except requests.exceptions.RequestException as e:
      return e
    return data;

  def groupUserRole(groupId,userId,groupRole):
    if(type(groupId) is not str): return {"error" : "invalid_input", "message" : "groupName must be a string"}
      
    try:
      dt = datetime.datetime.now();
      lastid = crudOperation.insertData("""insert into kycface."userRole"("groupId","userId","groupRole") values(%s,%s,%s)""",(groupId,userId,groupRole))
      
      rets = None

      if(lastid<=0):
        rets = False
      else:
        rets = True

      data = {
        'result': rets        
       }
    
    except requests.exceptions.RequestException as e:
      return e
    return data;


#Funciones User
  def userAddFace(faceFilePath, userId):
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    rets=None 

    try:      
      dt = datetime.datetime.now();      
      lastid = crudOperation.insertData("""insert into kycface."userFace"("userId","image","dateCreate") values(%s,%s,%s)""",(userId,'data',dt))      
      codigo = faceEncode.encoding(faceFilePath,lastid)
      
      rets ={'return': {'faceId': lastid}}

    except Exception as e:
      return retorna

    return codigo

  def userAuth(userId, otp):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    if(type(permanent) is not str): return {"error" : "entra no valida", "mensaje" : "permanent tiene que ser texto"}

    access_token=None

    try:
      
      dataUser = crudOperation.returnData("""select "userId", "token" from kycface."userTb" where "name"='""" + name + """' and token='""" + otp + """' """ )

      if (dataUser > 0 ):
        access_token = create_access_token(identity=otp)
      else:
        access_token=None


       data = {'result': {'token': access_token}}
    

    except Exception  as e:
      return str(e)

    return data

  def userCreate(name,lastname,details,phone):
    if(type(name) is not str): return {"error" : "invalid_input", "message" : "Name must be a string"}
    if(type(lastname) is not str): return {"error" : "invalid_input", "message" : "LastName must be a string"}
    if(type(details) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}
    if(type(phone) is not str): return {"error" : "invalid_input", "message" : "Phone must be a string"}

    rets=None

    try:
      dt = datetime.datetime.now();

      lastid = crudOperation.insertData("""insert into kycface."userTb"("name","lastname","details","dateCreate","state","phone") values(%s,%s,%s,%s,%s,%s)""",(name,lastname,details,dt,0,phone))
      
      if (lastid>0):
        rets=lastid
      else:
        rets=None


      data = {'result': rets}

    except Exception as e:
      return str(e)

    return data

  def userEdit(userId,name,LastName,phone,details):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(details) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}

    rets=None

    try: 
      rowsUpdate = crudOperation.updateData("""update kycface."userTb" set "name"=%s,"lastName"=%s,"phone"=%s,"details"=%s where "userId"=%s """,
      (name,lastName,phone,details,userId))

      if(rowsUpdate > 0):
        rets = True
      else:
        rets = False 

      data = {
        'result': rets        
       }

    except Exception as e:
      return str(e)

    return data

  def userEnroll(userId, details,groupId):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(details) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}

    try:
      data = {
        'faceIds': [{'label' : 'the-key-name-for-file','faceId' : 'string-max-length-40-chars'}]
        }      
       
    except Exception as e:
      return str(e)

    return response

  def userFaceAuth(faceFilePath):
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    access_token = None
    try:

      rets = faceRecognizaImage.searchMatch(image_data)      

      faceId=""
      phone=""

      if not rets:
        return {"message":"Face without Recognition"}

      for row in rets:
        faceId = row["faceId"]

      retsUser = crudOperation.returnData("""select "name","fono" from kycface."userFaceAuthVw" where "idFace"=""" + str(faceId))
      
      for row in retsUser:
        phone=fow["fono"]
      
      access_token = create_access_token(identity=phono)

      data ={'result':{'token': access_token}}

    except Exception as e:
      return retorna

    return access_token

  def userGet(userId):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}    

    try:
      retsUser = crudOperation.returnData("""select "userId","details","name","lastName","phone" from kycface."userTb" where "userId"=""" + str(userId))
      retsFaces = crudOperation.returnData("""select "faceid" from kycface."userFace" where "userId"=""" + str(userId))      
      retsGroup = crudOperation.returnData("""select a."groupId",a."groupName",a."sizeLimit" from kycface."groupTb" as a, kycface."userGroup" as b
      where b."userId"=""" + userId + """ and a."groupId" = b."groupId" and  a."state"=0""")
      
     
      data = {'result': {'userId': retsUser, 'faceId': retsFaces,
             "roles": ['user'],'groups': retsGroup
        }}      
       
    except Exception as e:
      return str(e)

    return data

  def userGetManual(name,lastname):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}    

    try:
         
      data = crudOperation.returnData("""select "userId", "name", "lastname","details","token" from kycface."userTb" where "name"='""" + name + """' and token='""" + phone + """' """ )

      return data
    
    except Exception as e:
      return str(e)


  def userGetOTP(userId):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}    

    try:
     data = {
        'result': true        
       }
    except Exception as e:
      return str(e)

    return response

  def userRemove(userId):
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}   
    
    rets=None

    try: 
      rowsUpdate = crudOperation.updateData("""update kycface."userTb" set "state"=1""",
      (userId))

      if(rowsUpdate > 0):
        rets = True
      else:
        rets = False 

      data = {
        'result': rets        
       }
    except Exception as e:
      return str(e)

    return response

  def userRemoveFace(userId, faceId):
    if(type(faceId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}

    rets = None
    try:

      lastid = crudOperation.insertData("""delete from kycface."userFace" where userId=%s and idFace=%s """,(userId,faceId))

      if (lastid>0):
        rets = True
      else:
        rets = False

      data = {'result': rets}
    
    except Exception  as e:
      return str(e)

    return data

  def userRole(roles, userId):
    if(type(roles) is not str): return {"error" : "invalid_input", "message" : "userId must be a string"}
    if(type(userId) is not str): return {"error" : "invalid_input", "message" : "details must be a string"}

    try:

      lastid = crudOperation.insertData("""insert into kycface."userRole"("userId","groupRole") values(%s,%s)""",(userId,groupRole))
      
      if (lastid>0):
        rets=lastid
      else:
        rets=None

      data = {
        'result': true        
       }
    except Exception as e:
      return str(e)

    return response

  def userList():
    retorno=dict()
    try:
      
      data = crudOperation.returnData("""select "userId", "name" || ' ' || "lastname" as nameFull,"details" from kycface."userTb" where "state"=0""")
      

    except requests.exceptions.RequestException as e:
      return e
    return data;

#Funciones image
  def recognize(image_data):   
    try:

      data = faceRecognizaImage.searchMatch(image_data)      
      faceId=""
      
      if not data:
        return {"message":"rostro sin Reconocimiento"}

      for row in data:
        faceId = row["faceId"]

      dataO = crudOperation.returnData("""select "name","fono" from kycface."userFaceAuthVw" where "idFace"=""" + str(faceId))
           
      return dataO
    
    except Exception as e:
      return e.args
   
  def verify(faceFilePath, userId):
    if((not os.path.exists(faceFilePath))): return {"error":"archivo no valido", "mensaje" : faceFilePath+" no existe"}
    if(type(userId) is not str): return {"error" : "entra no valida", "mensaje" : "userId tiene que ser texto"}
    rets = None
    dataret =""

    try:
   
      data = faceRecognizaImage.searchMatch(image_data)      
      faceId=""
      
      if not data:
        return {"message":"rostro sin Reconocimiento"}

      for row in data:
        faceId = row["faceId"]

      dataO = crudOperation.returnData("""select "name","fono" from kycface."userFaceAuthVw" where "idFace"=""" + str(faceId) + """ and "userId"=""" + userId)
      
      if(dataO > 0):
        rets = True
      else:
        rets = False

      dataret = {'result': rets}
    
      return 
    

    except Exception  as e:
      return str(e)

    return dataret

