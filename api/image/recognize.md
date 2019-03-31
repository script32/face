## /kycface/image/recognize

Recognize the person in the photo if it is one of people added to the group.

* **URL** : `/image/recognize`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'formdata'
	- token
	
* **Request Body**
	- image
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			“status”:“success”,
			“statusCode”:“200",
			“result”:[{
				“personId”:“+918015768860",
				"name" : "John"
				"lastName": "Perez"
				"phone": "+45423342"
				"GroupId": "2"
				}
			]
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
			  --url 'https://kycface.mooo.com/kycface/image/recognize' \
			  --header 'content-type: multipart/form-data \
			  --header 'token: {{token}}' \
			  --form image=image in base64    	
    	
