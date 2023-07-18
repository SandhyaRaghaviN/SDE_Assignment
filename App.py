#flask used for flask application, jsonify is used for JSON format responses.
from flask import Flask, jsonify

#imports the require_api_key decorator from the Auth module.
from Auth import require_api_key

#used for making HTTP requests to external APIs.
import requests

#This will handle incoming requests and direct them to the appropriate functions.
app = Flask(__name__)

#It indicates that HTTP GET requests will be handled by this route.
@app.route("/movies/<movie_name>", methods=["GET"])

#This decorator ensures that a valid API key must be provided in the request headers in order to access the function.
@require_api_key

#the 'get_movie_details' function, takes 'movie_name' as a parameter.
def get_movie_details(movie_name):
    
    #URL to fetch movie details from the OMDb API. 
    #It includes the movie name as a query parameter, API key required for authentication.
    url = f"http://www.omdbapi.com/?apikey=a2828bd2&t={movie_name}"
    
    #The response is saved in the response variable after it makes an GET request to the URL created in the previous step.
    response = requests.get(url)
    
    #This line takes the response object's JSON data and extracts it, storing it in the data variable. 
    data = response.json()
    
    #checks if the OMDb API response has the key "Response". If true, movie details were found.
    if data.get("Response") == "True":
        
        #movie details
        movie_details = {
            "title": data["Title"],
            "release_year": data["Year"],
            "plot": data["Plot"],
            "cast": data["Actors"].split(", "),
            "rating": data["imdbRating"]
        }
        
        #This line sends a JSON response with the movie_details if the movie details were found.
        return jsonify(movie_details)
    
    #This line delivers a JSON response with an error message if the movie details are not found.
    return jsonify({"error": "Movie not found"})

#This line specifies an alternative path to the endpoint /movies.
@app.route("/movies", methods=["GET"])

##This decorator ensures that a valid API key must be provided in the request headers in order to access the function.
@require_api_key

#Defines the 'get_movie_list' function, which does not take any parameters.
def get_movie_list():
    
    ##URL to fetch movie details from the OMDb API. 
    #It includes the necessary API key for authentication and specifies "movie" as the search type.
    url = f"http://www.omdbapi.com/?apikey=a2828bd2&s=popular&type=movie"
    
    #The response is saved in the response variable after it makes an GET request to the URL created in the previous step.
    response = requests.get(url)
    
    ##create a list of movie dictionaries that include details like "title" and "release_year."
    data = response.json()
    if data.get("Response") == "True":
        movie_list = []
        for movie in data["Search"]:
            movie_list.append({
                "title": movie["Title"],
                "release_year": movie["Year"]
            })
            
        #This line provides a JSON response with the movie_list if the movie list is found.
        return jsonify(movie_list)
    
    # If the movie list is not found, this line returns a JSON response with an error message.
    return jsonify({"error": "Movie list not found"})

#This line checks if the current module is the main script.
if __name__ == "__main__":
    
    #This line starts the Flask development server with debugging enabled if the current module is the main script.
    app.run(debug=True)