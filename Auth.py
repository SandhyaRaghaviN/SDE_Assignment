#to import we require these libraries.

# The wraps function from the functools module is imported,
# the metadata of the original function is preserved using the wraps function.
from functools import wraps

#request is used to access the data sent with the request.
from flask import request, jsonify

#imports the API_KEY variable from the Config module.
from Config import API_KEY

#This function acts as a decorator, preventing access to the wrapped function func until a valid API key is detected.
def require_api_key(func):
    
    #This decorator line uses the wraps decorator to wrap the decorated function.
    @wraps(func)
    
    #The decorated inner function is defined. This function will replace old require_api_key function.
    def decorated(*args, **kwargs):
        
        #Using the 'request.headers.get' method, this line extracts the value of the "API-Key".
        api_key = request.headers.get("API-Key")
        
        #This line determines whether the api_key variable is empty or different from the API_KEY.
        if not api_key or api_key != API_KEY:
            
            #When a requirement for an unauthorised request is satisfied, issuing a JSON response along with an error message.
            return jsonify({"error": "Unauthorized"})
        
        #This line calls the original function if the API key is valid. 
        return func(*args, **kwargs)
    
    #returned as the result of the require_api_key function.
    return decorated
