from django.core.urlresolvers import resolve
from django.http import HttpResponse
from django.core import urlresolvers
from fuzzywuzzy import fuzz
from SampleApp.models import *
from constants import *
import time

class printer(object):

	def __init__(self):	


		#the user_dict stores the user against the rating of the user
		self.all_user_dict = {}
		#get the user dict from here

		#the decision settings
		self.super_admin = {
		'time_delta':0,
		'time_rating':0
		}
		self.time_measure = {}
		#initializing the sequence matcher

	def get_client_ip(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
		    ip = x_forwarded_for.split(',')[0]
		else:
		    ip = request.META.get('REMOTE_ADDR')
		return ip

	def detect_on_api(self, resolved_name, user_address):
		user_dict =  self.all_user_dict[user_address]
		detect_pattern_list = []
		#get the sequencer
		user_pattern = user_dict['user_pattern']
		detect_pattern = user_dict['detect_pattern']
		if len(detect_pattern) == 0:
			detect_pattern = detect_pattern + resolved_name
		found_pattern = None
		pattern_differential_time = 0
		if user_pattern.endswith(resolved_name):
			if resolved_name != detect_pattern[len(detect_pattern) - 1]:
				found_pattern = detect_pattern + resolved_name
			else:
				found_pattern = detect_pattern
			pattern_dict = user_dict['pattern_list']

			try: 
				pattern_time = pattern_dict[found_pattern]
				prev_pattern_time = pattern_time[1]
				pattern_time = [pattern_time[0] + 1, time.time()]
				pattern_dict[found_pattern] = pattern_time
				detect_pattern = ''
				pattern_differential_time = prev_pattern_time - time.time()
			except Exception as e:
				pattern_dict[found_pattern] = [1,  time.time()]#create an array

		else:
			try:
				detect_pattern[len(detect_pattern) - 1]
			except Exception as e:
				detect_pattern = detect_pattern + resolved_name
			user_pattern = user_pattern + resolved_name

			if resolved_name != detect_pattern[len(detect_pattern) - 1]:
				detect_pattern = detect_pattern + resolved_name
			else:
				detect_pattern = detect_pattern

		t_dict = self.all_user_dict[user_address]
		t_dict['user_pattern'] = user_pattern
		t_dict['detect_pattern'] = detect_pattern
		t_dict['pattern_differential_time'] = 0
		if abs(pattern_differential_time) < .1:
			t_dict['api_detection_rating'] = t_dict['api_detection_rating'] + .001
		else:
			t_dict['api_detection_rating'] = t_dict['api_detection_rating'] - .001
		self.all_user_dict[user_address] = t_dict
		if found_pattern:
			return found_pattern
		return None

	def rate_the_user(self, user_dict):

		previous_time = user_dict['previous_request_time']
		rating = user_dict['rating']
		prev_time_delta = user_dict['time_delta']
		exec_time = user_dict['exec_time']

		#setting the previous time now
		user_dict['previous_request_time'] = time.time()

		#perform the time based rating system
		current_time = time.time()

		time_difference = current_time - previous_time
		if time_difference > 2:
			time_difference = prev_time_delta
		time_delta = ( prev_time_delta + time_difference ) / 2 # to be set
		user_dict['time_delta'] = time_delta
		delta_rating = time_delta - prev_time_delta
		if prev_time_delta == 0:
			pass
		else:
			user_dict['differential_rating'] = user_dict['differential_rating'] + delta_rating
		return user_dict

	def process_request(self, request):

		request_path = request.get_full_path()
		resolved_name = resolve(request.path_info).url_name
		user_address = self.get_client_ip(request)
		try:

			user_dict = self.all_user_dict[user_address]
			if user_dict['differencial_rating'] < 7.4 or user_dict['processing_rating'] < 7.4 or user_dict['api_detection_rating'] < 7.4:
				user_dict['status'] = 0

		except Exception as e:

			user_dict = {}
			user_dict['rating'] = BASE_RATING
			user_dict['previous_request_time'] = 0
			user_dict['time_delta'] = 0
			user_dict['exec_time'] = 0
			user_dict['user_pattern'] = '1'
			user_dict['detect_pattern'] = ''
			user_dict['pattern_list'] = {}
			user_dict['processing_rating'] = 7.5
			user_dict['differencial_rating'] = 7.5
			user_dict['api_detection_rating'] = 7.5
			user_dict['pattern_differential_time'] = 0
			user_dict['status'] = 1

		self.all_user_dict[user_address] = user_dict
		final_pattern = self.detect_on_api(resolved_name, user_address)
		self.all_user_dict[user_address] = user_dict
		self.all_user_dict[user_address] = self.rate_the_user(user_dict)
		self.time_measure[request] = time.time()
		print all_user_dict
		if user_dict['status'] == 0:
			return HttpResponse("User Blocked!!! Please contact administrator to unblock")
		return None

	def process_response(self, request, response):
		user_address = self.get_client_ip(request)
		exec_time = abs(self.time_measure[request] - time.time())
		user_dict = self.all_user_dict[user_address]
		try:
			previous_exec_time = user_dict['exec_time']
			user_dict['exec_time'] = (user_dict['exec_time'] + exec_time) / 2
			del self.time_measure[request]

			#managing the ratings over heres
			rating_differential = (exec_time - previous_exec_time) 
			user_dict['processing_rating'] = user_dict['processing_rating'] - rating_differential

		except Exception as e:
			pass
		#todo: write a logic for exec time ratings
		#we have set the the time delta # admin can set the percentage of what load can be accepted
		#repeated increase will cause a back drop
		return response