## /user/addFace

Register additional faces to the user to increase accuracy. Anywhere between 1-5 faces would be sufficient in most scenarios. The faceId would be provided back in the response. If the face is not detected by the system then the faceId would not be present in the response.

* **URL** : `/user/addFace`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'formdata'
	- tenantid 
	- tenantkey
	- token
	
* **Request Body**

	- userId
	- face : face image
  
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
			--header 'tenantid: {{tenantid}}' \
			--header 'tenantkey: {{tenantkey}}' \
			--header 'token: {{token}}' \
			--form 'userId=789' \
			--form image=base64Image \
    	
    	
