## /kycface/user/removeFace

Remove a face from the user by providing the faceId.


* **URL** : `/user/removeFace`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	
	- token
	
* **Request Body**

	- userId
	- faceId
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			"status" : "success",
			"statusCode" : "200"
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			  --url 'https://kycface.mooo.com/kycface/user/removeFace' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{"userId":"+910123456789", "faceId" : "testId"}'
    	
    	
