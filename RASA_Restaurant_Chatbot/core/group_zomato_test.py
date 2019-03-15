import json
import requests
import os
import numpy as np

os.chdir("C:\\Users\\anugraha.sinha\\OneDrive\\Documents\\Post Graduate ML & AI IIIT-Bangalore Upgrad\\Main Program\\3_NLP\\3_5_ChatBot_Rasa_Stack\\case_study_rest_chatbot\\core")
from zomatopy import initialize_app

class ZomatoInfo:
    def __init__(self):
        zomatoConfig = {"user_key" : "6ce88a5ec1419e335afa1c7f92f4b739" }
        self.zomato = initialize_app(zomatoConfig)
        # With ref from : https://en.wikipedia.org/wiki/Classification_of_Indian_cities #
        self.selectedCityList = ['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Delhi NCR', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune', 
                                         'Agra', 'Ajmer', 'Aligarh', 'Allahabad', 'Amravati', 'Amritsar', 'Asansol', 'Aurangabad', 
                                         'Bareilly', 'Belgaum', 'Bhavnagar', 'Bhiwandi', 'Bhopal', 'Bhubaneswar', 'Bikaner', 
                                         'Bokaro Steel City', 'Chandigarh', 'Coimbatore', 'Cuttack', 'Dehradun', 'Dhanbad', 
                                         'Durg-Bhilai Nagar', 'Durgapur', 'Erode', 'Faridabad', 'Firozabad', 'Ghaziabad', 
                                         'Gorakhpur', 'Gulbarga', 'Guntur', 'Gurgaon', 'Guwahati','Gwalior', 'Hubli-Dharwad', 
                                         'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 'Jammu', 'Jamnagar', 'Jamshedpur', 'Jhansi', 
                                         'Jodhpur', 'Kannur', 'Kanpur', 'Kakinada', 'Kochi', 'Kottayam', 'Kolhapur', 'Kollam', 'Kota', 
                                         'Kozhikode', 'Kurnool', 'Lucknow', 'Ludhiana', 'Madurai', 'Malappuram', 'Mathura', 'Goa', 'Mangalore', 
                                         'Meerut', 'Moradabad', 'Mysore', 'Nagpur', 'Nanded', 'Nashik', 'Nellore', 'Noida', 'Palakkad', 'Patna', 
                                         'Pondicherry', 'Raipur', 'Rajkot', 'Rajahmundry', 'Ranchi', 'Rourkela', 'Salem', 'Sangli', 'Siliguri', 'Solapur', 
                                         'Srinagar', 'Sultanpur', 'Surat', 'Thiruvananthapuram', 'Thrissur', 'Tiruchirappalli', 'Tirunelveli', 'Tiruppur', 
                                         'Ujjain', 'Vijayapura', 'Vadodara', 'Varanasi', 'Vasai-Virar City', 'Vijayawada', 'Visakhapatnam', 'Warangal']

    def getDetails(self,location,cuisine,lowerRateLimit=0,upperRateLimit=300,debugMode=False):

        try:
            # get the location details -> latitude and longitude #
            loc = json.loads(self.zomato.get_location(location,limit=1))
            city_lat = loc["location_suggestions"][0]["latitude"]
            city_long = loc["location_suggestions"][0]["longitude"]
            city_id = loc["location_suggestions"][0]["city_id"]
            city_name = loc["location_suggestions"][0]["title"]
            if debugMode:
                print("city_name = %s, city_lat = %s, city_long = %s, city_id = %s" %(str(city_name),str(city_lat),str(city_long),str(city_id)))
            if city_name not in self.selectedCityList:
                print("City : %s not in area where Foodie operates" %(city_name))
                return {"results_found" : [] }
            # get cuisine #
            selected_cuisine_info = dict()
            available_cuisines = self.zomato.get_cuisines(city_id)
            if cuisine not in available_cuisines.values():
                print("In City : %s, selected cuisine : %s not available" %(city_name,cuisine))
                return {"results_found" : [] }
            else:
                for key,value in available_cuisines.items():
                    if value == cuisine:
                        selected_cuisine_info[value] = key
            # Get restaurant details #
            zomato_result = json.loads(self.zomato.restaurant_search("", city_lat, city_long, str(selected_cuisine_info.get(cuisine)), limit=20))
            result_list = list()
            user_rating_list = list()
            for rest in zomato_result["restaurants"]:
                rest_data = rest["restaurant"]
                if rest_data["average_cost_for_two"] > lowerRateLimit and rest_data["average_cost_for_two"] <= upperRateLimit:
                    result_data = { "name" : rest_data["name"],
                                                        "location" : rest_data["location"]["address"],
                                                        "user_rating" : rest_data["user_rating"]["aggregate_rating"]
                                                        }
                    user_rating_list.append(rest_data["user_rating"]["aggregate_rating"])
                    result_list.append(result_data)
            if debugMode:
                print("Unsorted result list:\n%s" %(str(result_list)))
            if len(result_list) > 0:
                # Sort by user_rating
                result_list = list(np.array(result_list)[np.argsort(np.array(user_rating_list))])
                # Since above was ascending order, lets 
                result_list.reverse()
                result_list = result_list[0:5]

            if debugMode:
                print("Final result list:\n%s" %(str(result_list)))
            return {"results_found" : result_list}

        except Exception as e:
            print("Exception is searching through zomato, exception : %s" %(str(e)))
            #raise(e)
            # May be we should not raise an exception here #
            return {"results_found" : [] }