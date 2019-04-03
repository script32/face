## /user/edit

Edit the user details with this API call.

* **URL** : `/user/edit`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- tenantid 
	- tenantkey
	- token
	
* **Request Body**

	- userId
  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
		  "status": "success",
		  "statusCode": "200"
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			--url 'https://kycface.mooo.com/kycface/user/edit' \
            --header 'content-type: application/json' \
            --header 'tenantid: {{tenantid}}' \
            --header 'tenantkey: {{tenantkey}}' \
            --data '{"userId":"+910123456789","details":"some string that you want to store"}'


    	
    	
