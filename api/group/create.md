## /kycface/group/create

Create a group with a name and a limit The response would include the group ID, which will be the unique identifier of the group for future references.

* **URL** : `/group/create`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- token
	
* **Request Body**

	- groupName
	- sizeLimit
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
		  "status": "success",
		  "statusCode": "200",
		  "result": {
		    "groupId": "weryui4589fgh"
		  }
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  		    --url 'https://kycface.mooo.com/kycface/group/create' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{"groupName":"facetestaccess","sizeLimit":100}'
    	
    	
