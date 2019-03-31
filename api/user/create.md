## /kycface/user/create

Register a new user with the tenant. This performs a subset of actions performed by /user/enroll.

* **URL** : `/user/create`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- token
	
* **Request Body**

	- userId
	- lastname
	- details
  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			"status" : "success",
			"statusCode" : "200",
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			  --url 'https://kycface.mooo.com/kycface/user/create' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{"userId":"9","details":"some string"}'
    	
    	
