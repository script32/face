## /kycface/group/remove

Delete the group. But retain the users in the tenant.

* **URL** : `/group/remove`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- token
	
* **Request Body**

	- groupId
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
		  "status": "success",
		  "statusCode": "200"
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			  --url 'https://kycface.mooo.com/kycface/group/remove' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{"groupId":"facetestaccess"}'
    	
    	
