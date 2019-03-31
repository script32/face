## /kycface/user/addFace

Register additional faces to the user to increase accuracy. Anywhere between 1-5 faces would be sufficient in most scenarios. the faceId would be provided back in the response. If the face is not detected by the system then the faceId would not be present in the response.

* **URL** : `/user/addFace`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'formdata'
	- token
	
* **Request Body**

	- userId
	- image : image in base64
  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			"status" : "success",
			"statusCode" : "200",
			"result" : {
				"faceId": "string-with-max-chars-40"
			}
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
			--url 'https://kycface.mooo.com/kycface/user/addFace' \
			--header 'content-type: multipart/form-data' \
			--header 'token: {{token}}' \
			--form 'userId=+910123456789' \
			--form image=@image_path.jpg \
    	
    	
