## /kycface/user/auth

If the tenant uses phone numbers as userId, then this API call can be used to obtain the user token. This has to be called after the /user/getOTP api call.

* **URL** : `/user/auth`
  
* **Method:** `POST`

* **Header**
	
	- content-type : 'application/json'
	
* **Request Body**

	- userId
	- otp 
  
* **Success Response:**

  * **Code:** 200 <br />
  * Schema : 
		
			
		{
			"status" : "success",
			"statusCode" : "200",
			"result" : {
				"token": "*************************************"
			}
		}
		
	

* **Sample Call:**

   	
    	curl --request POST \
  			--url 'https://kycface.mooo.com/kycface/user/auth' \
            --header 'content-type: application/json' \
            --data '{"userId":"+910123456789","otp":"1234"}'
    	
    	
