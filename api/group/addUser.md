## /kycface/group/addUser

Add an existing user to an existing group.

* **URL** : `/group/addUser`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- token
	
* **Request Body**

	- groupId
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
  			--url 'https://kycface.mooo.com/kycface/group/addUser' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{"groupId":"facetestaccess","userId":"+910001231314"}'
    	
    	
