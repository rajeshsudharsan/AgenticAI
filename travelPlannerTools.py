from langchain.tools import tool
from langchain_tavily import TavilySearch
from typing import List
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities import OpenWeatherMapAPIWrapper
import os
from datetime import date
from langchain_core.tools import Tool
from dotenv import load_dotenv
import requests
import json
import serpapi

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY") 
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")



@tool
def searchTouristAttraction(city:str) : 
    """
        Suggests Top attactions for the city specified in the argument

    Args:
        city (str): city
        
    Returns:
        top Attraction list in the city based on number of attractions
    """
    attraction_list =[]
    searchQuery = f'Provide top attractions nearby {city}'
    print(searchQuery)
    headers = {
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "Accept": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress"
    }
    data = {'textQuery': searchQuery}
    #responseObj = { "places": [ { "formattedAddress": "30 Rockefeller Plaza, New York, NY 10112, USA", "displayName": { "text": "Top of The Rock", "languageCode": "en" } }, { "formattedAddress": "45 Rockefeller Plaza, New York, NY 10111, USA", "displayName": { "text": "Rockefeller Center", "languageCode": "en" } }, { "formattedAddress": "45 E 42nd St, New York, NY 10017, USA", "displayName": { "text": "SUMMIT One Vanderbilt", "languageCode": "en" } }, { "formattedAddress": "30 Hudson Yards, New York, NY 10001, USA", "displayName": { "text": "Edge", "languageCode": "en" } }, { "formattedAddress": "117 West St, New York, NY 10007, USA", "displayName": { "text": "One World Observatory", "languageCode": "en" } }, { "formattedAddress": "Manhattan, NY 10036, USA", "displayName": { "text": "Times Square", "languageCode": "en" } }, { "formattedAddress": "New York, NY, USA", "displayName": { "text": "Central Park", "languageCode": "en" } }, { "formattedAddress": "New York, NY 10020, USA", "displayName": { "text": "The Channel Gardens", "languageCode": "en" } }, { "formattedAddress": "251 Spring St, New York, NY 10013, USA", "displayName": { "text": "Color Factory NYC", "languageCode": "en" } }, { "formattedAddress": "New York, NY 10011, USA", "displayName": { "text": "The High Line", "languageCode": "en" } }, { "formattedAddress": "20 W 34th St., New York, NY 10001, USA", "displayName": { "text": "Empire State Building", "languageCode": "en" } }, { "formattedAddress": "New York, NY 10004, USA", "displayName": { "text": "The Battery", "languageCode": "en" } }, { "formattedAddress": "77 8th Ave, New York, NY 10014, USA", "displayName": { "text": "Museum of Illusions", "languageCode": "en" } }, { "formattedAddress": "New York, NY 10014, USA", "displayName": { "text": "Little Island", "languageCode": "en" } }, { "formattedAddress": "75 Battery Place, New York, NY 10280, USA", "displayName": { "text": "Rockefeller Park", "languageCode": "en" } }, { "formattedAddress": "Battery Park Underpass, New York, NY 10004, USA", "displayName": { "text": "Statue of Liberty Lookout", "languageCode": "en" } }, { "formattedAddress": "234 W 42nd St, New York, NY 10036, USA", "displayName": { "text": "Madame Tussauds New York", "languageCode": "en" } }, { "formattedAddress": "20 Hudson Yards, New York, NY 10001, USA", "displayName": { "text": "Vessel", "languageCode": "en" } }, { "formattedAddress": "233 5th Ave, New York, NY 10016, USA", "displayName": { "text": "Museum of Sex", "languageCode": "en" } }, { "formattedAddress": "Ellis Island, New York, NY 10280, USA", "displayName": { "text": "Ellis Island", "languageCode": "en" } } ] }
    response = requests.post('https://places.googleapis.com/v1/places:searchText', headers=headers, json=data)
    
    responseObj = response.json()

    for place in responseObj['places']:
        attraction = place['displayName']['text']
        attraction_list.append(attraction)

    return  attraction_list

@tool
def searchHotelUsingSerp(places:str, city:str, country:str, price: int, checkInDate : str, checkoutDate : str) : 
    """
        Suggest hotels near the places mentioned within the budget for each day and provide a suggestion

    Args:
        places (str): place
        city (str): city
        price (int): price
        checkInDate (str) : checkInDate
        checkoutDate (str) : checkoutDate
    Returns:
       List of top hotel near the place in city mentioned within price
       
    """
    
    hotelList = []
    searchQuery = f'Hotels to a {places} nearby {city} for stay with address within price USD {price}'
    print(f'Tool Calling Search Hotel ==> {searchQuery}')
    client = serpapi.Client(api_key=SERP_API_KEY)
    params = {
        "engine": "google_hotels",  
        "api_key": "931b70ddb7fe1561bf504c3358328ec30db0be6bda4ddc2195955456031ba89f",
        "q": places+ "," + city,    
        "check_in_date" : checkInDate,
        "check_out_date" : checkoutDate, 
        "hl": "en",          
        "gl": country,       
        "max_price": price 
    }

    response = client.search(params)
    print(response)
    
    responseObj = response
    #print(json.dumps(responseObj, indent=4))

    for property in responseObj['properties']:
        hotel= property['name'] + " Address : " + str(property['gps_coordinates']['latitude']) + " " + str(property['gps_coordinates']['longitude']) +  " price in USD: " + str(property['total_rate']['lowest'])
        print(hotel)
        hotelList.append(hotel)
    return hotelList

@tool
def searchHotel(places:str, city:str, price: int) : 
    """
        Suggest hotels near the places mentioned within the budget for each day and provide a suggestion

    Args:
        places (str): place
        city (str): city
        price (int): price
    Returns:
       List of top hotel near the place in city mentioned within price
       
    """
    
    hotelList = []
    searchQuery = f'Hotels to a {places} nearby {city} for stay with address within price USD {price}'
    print(f'Tool Calling Search Hotel ==> {searchQuery}')
    headers = {
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "Accept": "application/json",
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress"
    }

    data = {'textQuery': searchQuery}

    #responseObj = { "places": [ { "formattedAddress": "790 7th Ave, New York, NY 10019, USA", "displayName": { "text": "The Manhattan at Times Square Hotel", "languageCode": "en" } }, { "formattedAddress": "870 7th Ave, New York, NY 10019, USA", "displayName": { "text": "Park Central Hotel New York", "languageCode": "en" } }, { "formattedAddress": "414 W 46th St, New York, NY 10036, USA", "displayName": { "text": "414 Hotel New York Times Square", "languageCode": "en" } }, { "formattedAddress": "201 W 55th St, New York, NY 10019, USA", "displayName": { "text": "WestHouse Hotel New York", "languageCode": "en" } }, { "formattedAddress": "160 W 56th St, Manhattan, NY 10019, USA", "displayName": { "text": "The Carnegie Hotel", "languageCode": "en" } }, { "formattedAddress": "15- 61 127th St 15- 63, College Point, NY 11356, USA", "displayName": { "text": "Ly New York Hotel", "languageCode": "en" } }, { "formattedAddress": "305 W 46th St, New York, NY 10036, USA", "displayName": { "text": "Hotel Riu Plaza New York Times Square", "languageCode": "en" } }, { "formattedAddress": "27 Barclay St, New York, NY 10007, USA", "displayName": { "text": "Four Seasons Hotel New York Downtown", "languageCode": "en" } }, { "formattedAddress": "270 W 43rd St, New York, NY 10036, USA", "displayName": { "text": "The Westin New York at Times Square", "languageCode": "en" } }, { "formattedAddress": "38 W 31st St #110, New York, NY 10001, USA", "displayName": { "text": "31 Street Broadway Hotel", "languageCode": "en" } }, { "formattedAddress": "414 W 46th St, New York, NY 10036, USA", "displayName": { "text": "414 Hotel NEW YORK TIMES SQUARE", "languageCode": "en" } }, { "formattedAddress": "2 6th Ave, New York, NY 10013, USA", "displayName": { "text": "The Roxy Hotel New York", "languageCode": "en" } }, { "formattedAddress": "1155 Broadway, New York, NY 10001, USA", "displayName": { "text": "Broadway Plaza Hotel", "languageCode": "en" } }, { "formattedAddress": "88 Allen St, New York, NY 10002, USA", "displayName": { "text": "The Allen Hotel", "languageCode": "en" } }, { "formattedAddress": "125 W 45th St, New York, NY 10036, USA", "displayName": { "text": "45 Times Square Hotel", "languageCode": "es" } }, { "formattedAddress": "36 Central Park S South, New York, NY 10019, USA", "displayName": { "text": "Park Lane Hotel New York", "languageCode": "en" } }, { "formattedAddress": "160 W 25th St, New York, NY 10001, USA", "displayName": { "text": "The Chelsean New York Hotel", "languageCode": "en" } }, { "formattedAddress": "16 E 30th St, New York, NY 10016, USA", "displayName": { "text": "Best Western Premier Empire State Hotel", "languageCode": "en" } }, { "formattedAddress": "1 Dutch St, New York, NY 10038, USA", "displayName": { "text": "One Dutch Hotel", "languageCode": "en" } }, { "formattedAddress": "226 W 52nd St, New York, NY 10019, USA", "displayName": { "text": "M Social Hotel New York Times Square", "languageCode": "en" } } ] }
    response = requests.post('https://places.googleapis.com/v1/places:searchText', headers=headers, json=data)

    responseObj = response.json()
    #print(json.dumps(responseObj, indent=4))

    for place in responseObj['places']:
        hotel= place['displayName']['text'] + " Address : " + place['formattedAddress'] + " price in USD: " + str(price )
        print(hotel)
        hotelList.append(hotel)
    return hotelList



@tool
def addPrice(prices: List[int]) : 
    """
        get list of prices and calulate the total price by adding each price

    Args:
        price (list[int]): price
    Returns:
        int : total price of stay for entire Travel
    """
    print(f'Tool Calling Add price Hotel {prices}')
    totalPrice = 0
    for price in prices:
        totalPrice +=price
    return totalPrice


weather = OpenWeatherMapAPIWrapper()
tools = [searchTouristAttraction,searchHotelUsingSerp,addPrice,weather.run]

#response1 = searchWeather.run({'city':'Dallas','date_of_travel':'2025-08-25'})
#print(response1)

#response2 = searchHotel.run({'places':'Willis Tower', 'city': 'Chicago', 'price' :400}) 
#print(response2)

#response3 = addPrice.run({'prices': [1,2]}) 
#print(response3)

#response4 = searchTouristAttraction.run({'city':'New York'}) 
#print(response4)

#response5 = searchHotelUsingSerp.run({'places':'RockFellar Center', 'city':'New York', 'country':'US', 'price': 300, 
#                                      'checkInDate' : '2025-06-23', 'checkoutDate' : '2025-06-24'})
#print(response5)