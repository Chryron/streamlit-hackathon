from dotenv import load_dotenv
import os
import openrouteservice

load_dotenv()
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")
coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key=OPENROUTESERVICE_API_KEY) # Specify your personal API key
routes = client.directions(coords)

def get_coords(
        location: str,
):
    """
    Get the coordinates of a location.
    """
    coords = client.pelias_search(text=location)
    return coords


# print(get_coords("Berlin"))
print(routes)