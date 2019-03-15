from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from flask import Response

import json
import requests
import os
import numpy as np
import logging
import ast
import traceback

import smtplib
from .zomatopy import Zomato

from lib import ChatBotConfigParser
from lib import ChatBotLogging

logger = logging.getLogger("ChatBotBase.coreActions")

class ZomatoInfo:
	def __init__(self):
		self.config = ChatBotConfigParser().parser
		
		zomatoConfig = {"user_key" : self.config.get('Zomato','user_key') }
		self.zomato = Zomato(zomatoConfig)
		# With ref from : https://en.wikipedia.org/wiki/Classification_of_Indian_cities #
		self.selectedCityList = ['Ahmedabad', 'Bangalore', 'Bengaluru', 'Chennai', 'Delhi','Delhi NCR','Hyderabad', 'Kolkata', 'Mumbai', 'Pune', 
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
	def isLocationAvailable(self,location,debugMode=False):
		try:
			loc=json.loads(self.zomato.get_location(location,limit=1))
			if len(loc['location_suggestions'])==0:
				logger.debug("city_name = %s, Not found" %(str(location)))
				return {"location_found":'notfound'}

			city_name=loc["location_suggestions"][0]["city_name"].strip()
			if debugMode:
				logger.debug("city_name = %s" %(str(city_name)))
			if city_name.lower() not in [city.lower() for city in self.selectedCityList]:
				logger.info("City : %s not in area where Foodie operates" %(city_name))
				return {"location_found":'tier3'}
			else:
				return {"location_found":'found'}
		except Exception as e:
			logger.error("Exception is searching through zomato, exception : %s" %(str(e)))
			logger.error("%s" %(str("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))))
			return {"location_found":"notfound"}


	def getDetails(self,location,cuisine,lowerRateLimit=0,upperRateLimit=300,debugMode=True):

		try:
			# get the location details -> latitude and longitude #
			loc = json.loads(self.zomato.get_location(location,limit=1))
			city_lat = loc["location_suggestions"][0]["latitude"]
			city_long = loc["location_suggestions"][0]["longitude"]
			city_id = loc["location_suggestions"][0]["city_id"]
			city_name = loc["location_suggestions"][0]["city_name"].strip()
			#print(city_name)
			#print("Bangalore" in self.selectedCityList)
			if debugMode:
				logger.debug("city_name = %s, city_lat = %s, city_long = %s, city_id = %s" %(str(city_name),str(city_lat),str(city_long),str(city_id)))
			if city_name.lower() not in [city.lower() for city in self.selectedCityList]:
				logger.info("City : %s not in area where Foodie operates" %(city_name))

				return {"results_found" : [],"cuisine_found":"","price_found":""}
			# get cuisine #
			selected_cuisine_info = dict()
			available_cuisines = self.zomato.get_cuisines(city_id)
			if cuisine not in [cu.lower() for cu in available_cuisines.values()]:
				logger.info("In City : %s, selected cuisine : %s not available" %(city_name,cuisine))
				#dispatcher.utter_message("-----\n"+"In City : %s, selected cuisine : %s not available" %(city_name,cuisine))
				return {"results_found" : [],"cuisine_found":'notfound',"price_found":""}
				
			else:
				for key,value in available_cuisines.items():
					if value.lower() == cuisine.lower():
						#print(value)
						selected_cuisine_info[value.lower()] = key
			# Get restaurant details #
			list1 = [0,20,40,60,80]
			zomato_results= []
			if upperRateLimit==300:
				order='asc'
				sort='cost'
			else:
				order=""
				sort=""
			for i in list1:
				#results = self.zomato.restaurant_search("", city_lat, city_long, str(selected_cuisine_info.get(cuisine)), limit=i)
				#print(str(selected_cuisine_info.get(cuisine)))
				
				results = self.zomato.restaurant_search_sort("", city_lat, city_long, str(selected_cuisine_info.get(cuisine.lower())),start=i,limit=20,sort_by=sort,order=order)
				
				temp_result= json.loads(results)
				zomato_results.extend(temp_result['restaurants'])
				#print("Number of Zomato results :",len(zomato_results))
			#zomato_result = json.loads(self.zomato.restaurant_search("", city_lat, city_long, str(selected_cuisine_info.get(cuisine)), limit=100))
			result_list = list()
			user_rating_list = list()
			
			for rest in zomato_results:
				#print("In rest")
				#rest_data = rest["restaurant"]
				rest_data=rest['restaurant']
				if rest_data["average_cost_for_two"] > lowerRateLimit and rest_data["average_cost_for_two"] <= upperRateLimit:
					result_data = { "name" : rest_data["name"],"location" : rest_data["location"]["address"],"user_rating" : rest_data["user_rating"]["aggregate_rating"],"budget":rest_data["average_cost_for_two"]}
					user_rating_list.append(rest_data["user_rating"]["aggregate_rating"])
					result_list.append(result_data)
			if debugMode:
				#logger.debug("Unsorted result list:\n%s" %(str(result_list)))
				logger.debug("Length of unsorted list = %d" %(len(result_list)))
			if len(result_list) > 0:
				# Sort by user_rating
				price_found="found"
				result_list = list(np.array(result_list)[np.argsort(np.array(user_rating_list))])
				# Since above was ascending order, lets 
				result_list.reverse()
				result_list = result_list[0:10]
			else:
				price_found="notfound"

			if debugMode:
				#logger.debug("Final result list:\n%s" %(str(result_list)))
				logger.debug("Length of final result list = %d" %(len(result_list)))
			return {"results_found" : result_list,"cuisine_found":"found",'price_found':price_found}

		except Exception as e:
			logger.error("Exception is searching through zomato, exception : %s" %(str(e)))
			logger.error("%s" %(str("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))))
			return {"results_found" : [] ,"cuisine_found":"",price_found:""}

class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		price = tracker.get_slot('price')
		logger.info("User information as present in slots are:\nlocation=%s\ncuisine=%s\nprice=%s" %(str(loc),str(cuisine),str(price)))
		if price == "lesser than 300":
			lowerRateLimit = 0
			upperRateLimit = 300
		elif price == "between 300 to 700":
			lowerRateLimit = 300
			upperRateLimit = 700
		elif price == "more than 700":
			lowerRateLimit = 700
			upperRateLimit = 10000   # assuming a maximum limit of 10000 #
		else:
			pass
		zomatoInfoObj = ZomatoInfo()
		results = zomatoInfoObj.getDetails(location=loc,cuisine=cuisine,lowerRateLimit=lowerRateLimit,upperRateLimit=upperRateLimit)
		logger.info("Zomato API provided results as :\n%s" %(str(results)))
		response=""
		display_response=""
		if results["price_found"]=='notfound':
			price_found="notfound"
		else:
			price_found="found"
		if len(results['results_found'])==0 and results['cuisine_found']=='notfound':
			response="In City : %s, selected cuisine : %s not available" %(loc,cuisine)
			display_response=response
			cuisine_found='notfound'
		elif len(results['results_found'])==0 and results['cuisine_found']!='notfound':
			response="No Results Found"
			display_response=response
			cuisine_found='found'
		else:
			cuisine_found='found'
			response="Here are the top " + " results around " + loc + " for " + str(cuisine) + " from Foodie:"
		
			for idx,restaurant in enumerate(results["results_found"]):
				
				response=response + "\n" + str(idx+1) + ". " + str(restaurant["name"].encode("utf-8"))[2:-1] + "\n"
				response=response + "  in " + str(restaurant["location"].encode("utf-8"))[2:-1] + "\n"
				response=response + " Avg Budget for Two People is "+str(restaurant['budget'])+"\n"
				response=response + "  User Rating : " + str(restaurant["user_rating"])
				if idx < 5:
					display_response=response
		logger.info("Final utterance given by chat bot for restaurant search:\n%s" %(display_response))
		dispatcher.utter_message("-----\n"+display_response)
		
		# Set the information for other slots here and return that data
		#return [SlotSet('search_results',response),SlotSet('location_found',"found" if len(results["results_found"]) != 0 else "notfound")]
		#return [SlotSet('search_results',response),SlotSet('location_found',results['location_found'])]
		return [SlotSet('search_results',response),SlotSet('cuisine_found',cuisine_found),SlotSet('price_found',price_found)]

class SendMail(Action):
	def name(self):
		return 'action_sendmail'
	
	def run(self,dispatcher,tracker,domain):
		try:
			fromaddr="upgradcasestudybuddies@gmail.com"
			toaddrs=tracker.get_slot('email')
			cuisine=tracker.get_slot('cuisine')
			location=tracker.get_slot('location')
			restaurant_data=tracker.get_slot('search_results')
			message = "From: upgradcasestudybuddies@gmail.com\r\nTo: " + str(toaddrs) + "\r\nSubject :Your query for restaurants\r\n\nHowdy,\n\nYou recently asked me to send details about " + cuisine + " restaurants around " + location + ", and the details are\n\n" + restaurant_data + "\n\n Thank you for using our services\n\nBest Wishes\nFoodie AI Team"
			logger.info("Email Message being sent is :\n%s" %(str(message)))
			username='upgradcasestudybuddies@gmail.com'
			password='JingleBell'
			server=smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr,toaddrs,message)
			server.quit()
			dispatcher.utter_message("-----\n"+"Email has been sent successfully")
			return [SlotSet('emailsent',"OK")]
		except Exception as e:
			logger.error("Unable to send email, Exception as : %s" %(str(e)))
			logger.error("%s" %(str("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))))
			dispatcher.utter_message("-----\n"+"Email Could not be sent")
			return [SlotSet('emailsent',"FAILED")]

	
class CheckLocation(Action):
	def name(self):
		return 'action_check_location'
	
	def run(self,dispatcher,tracker,domain):
		try:
			loc=tracker.get_slot('location')
			logger.info("In Check Location, checking location = %s" %(loc))
			zomatoInfoObj = ZomatoInfo()
			results = zomatoInfoObj.isLocationAvailable(loc,debugMode=True)
			return [SlotSet('location_found',results['location_found'])]
		except Exception as e:
			logger.error("Unable to check location, exception : %s" %(str(e)))
			logger.error("%s" %(str("\n".join([ line.rstrip('\n') for line in traceback.format_exception(e.__class__, e, e.__traceback__) ]))))
			return [SlotSet('location_found',"Not Found")]




			
			
		
		

