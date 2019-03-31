## /kycface/image/verify

Verify the person in the image.

* **URL** : `/image/verify`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'formdata'
	- token
	
* **Request Body**
	- image
	- userId
	  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			“status”:“success”,
			“statusCode”:“200",
			“result”:[{
				“faceId”:“8W03lZcW4gyfVqNNtKik5rilZ78347",
				“personId”:“+918015768860",
				}
			]
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
			  --url 'https://kycface.mooo.com/kycface/image/verify' \
			  --header 'content-type: multipart/form-data \
			  --header 'token: {{token}}' \
			  --form 'userId=+910123456789' \
			  --form image0=@image_path.jpg    	
    	
