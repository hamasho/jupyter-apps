import os
import gmaps
import googlemaps


API_KEY = os.environ['GCP_API_KEY']
gmaps.configure(api_key=API_KEY)
CLIENT = googlemaps.Client(key=API_KEY)

DEBUG = False
