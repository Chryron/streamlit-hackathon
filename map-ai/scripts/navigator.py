from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, ChatMessage
from langchain.tools import format_tool_to_openai_function, StructuredTool
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

import requests
from route import Route

from dotenv import load_dotenv
import os
import json

import openrouteservice
from openrouteservice import convert

load_dotenv()
OPENROUTESERVICE_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")
# Specify your personal API key
client = openrouteservice.Client(key=OPENROUTESERVICE_API_KEY)


def get_route(
        start_coords: tuple,
        end_coords: tuple,
):
    """
    Get the route between two points as a GeoJSON.
    Params are tuples of (longitude, latitude).
    """
    coords = (start_coords, end_coords)
    routes = client.directions(coords)

    # decode_polyline needs the geometry only
    # geometry = routes[0]['geometry']

    # decoded = convert.decode_polyline(geometry)

    return routes


def get_coords(
        location: str,
):
    """
    Get the coordinates of a location.
    """
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={location}&limit=1&format=jsonv2")
    geolocation = response.json()[0]
    coords = (geolocation["lon"], geolocation["lat"])
    return coords


systemmessagecontent = """You are an AI chatbot with access to a route planning API.
"""


class Navigator:
    # weather_tool = StructuredTool.from_function(get_current_weather)
    route_tool = StructuredTool.from_function(get_route)
    coords_tool = StructuredTool.from_function(get_coords)
    tools = [route_tool, coords_tool]
    functions = [format_tool_to_openai_function(tool) for tool in tools]
    chat = ChatOpenAI(model="gpt-3.5-turbo")

    def process_query(self, user_query: str) -> Route:
        result = None
        messages = [
            SystemMessage(content=systemmessagecontent),
            HumanMessage(content=user_query)
        ]
        AI_message = self.chat.predict_messages(
            messages, functions=self.functions)
        messages += [AI_message]

        while AI_message.additional_kwargs.get("function_call") is not None:
            function_call = AI_message.additional_kwargs["function_call"]
            # execute function call
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            try:
                f = globals()[function_name]
                result = f(**function_args)
            except Exception as e:
                result = str(e)

            messages.append(ChatMessage(
                role="function",
                additional_kwargs={'name': function_name},
                content=json.dumps(result),))
            AI_message = self.chat.predict_messages(
                messages, functions=self.functions)
            messages += [AI_message]
        return Route(result, AI_message.content)
