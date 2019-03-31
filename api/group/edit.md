## /kycface/group/edit

Edit Name and Size Limit.

* **URL** : `/group/edit`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- token
	
* **Request Body**

	- groupId
	- groupName
	- sizeLimit 	
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
					
		{
		  "status": "success",
		  "statusCode": "200"
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			--url 'https://kycface.mooo.com/kycface/group/edit' \
            --header 'content-type: application/json' \
            --header 'token: {{token}}' \
            --data '{
					"groupId":"facetestaccess1500894070054914",
					"groupName":"PV96YXVwRB",
			    	"sizeLimit":631				
				}'
    	
    	
