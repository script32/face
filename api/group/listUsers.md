## /group/listUsers

Lists users in a group

* **URL** : `/group/listUsers`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	- tenantid 
	- tenantkey
	- token
	
* **Request Body**
	- groupId	
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
		  "status": "success",
		  "statusCode": "200",
		  "result" : {
		  	"users" : [{
				"userId" : "string",
				"details" : "string",
				"roles" : ["user/admin"],
				"groups" : [{
					"groupId" : "string",
					"role" : "user/groupAdmin"
				}],
				"faces" : ["string"]
			}]
		  }
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			  --url 'https://kycface.mooo.com/kycface/group/listUsers' \
            --header 'content-type: application/json' \
            --header 'tenantid: {{tenantid}}' \
            --header 'tenantkey: {{tenantkey}}' \
            --header 'token: {{token}}' \
            --data '{"groupId":"0CwUv4L","userId":"+910123456789","groupRole":"user"}'
    	
    	
