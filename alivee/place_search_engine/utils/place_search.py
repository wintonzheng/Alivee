import googlemaps
import datetime
import json
import time
from place_search_engine.constants.google_place_api import PlaceSearchResponseStatus
from place_search_engine.constants.google_place_api import PlaceSearchPlaceType

MAX_NEXT_PAGE_TOKEN_RETRY_COUNT = 3


class PlaceSearch(object):
	'''
	Wrapped google place search service for our usage.
	Documents: https://developers.google.com/places/web-service/search
	'''
	def __init__(self, location, key, isVerboseMode=False):
		'''
		Init method of place search class.

		param location: A tuple (lat, lng) indicates the location we want to search as the center of the area.
		param key: The Google API key.
		param isVerboseMode: if flag is True, then helper text will be printed for debugging.
		return: None
		'''
		self.location = location
		self.isVerboseMode = isVerboseMode
		# Need to handle exc in caller's method such as `ValueError: Invalid API key provided.`
		self.client = googlemaps.Client(key)

	def _getPlaceFilterKwargs(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None, page_token=None):
		'''
		Private helper method for creating the filter kwargs.
		'''
		filterKwargs = dict(location=self.location)

		if place_type:
			filterKwargs['type'] = place_type
		if radius:
			filterKwargs['radius'] = radius
		if keyword:
			filterKwargs['keyword'] = keyword
		if name:
			filterKwargs['name'] = name
		if rank_by:
			filterKwargs['rank_by'] = rank_by
		if page_token:
			filterKwargs['page_token'] = page_token

		return filterKwargs

	def _checkReponseStatus(self, response):
		'''
		Check whether the status of response is valid.
		'''
		if not response or not 'status' in response:
			raise Exception('Invalid response!')

		status = response['status']

		if status == PlaceSearchResponseStatus.ZERO_RESULTS:
			return None
		elif status == PlaceSearchResponseStatus.OK:
			return True

		raise Exception('Error in response with status code {}'.format(status))

	def _parseNearbySearchResponse(self, response):
		'''
		Private helper method that will parse response of nearby search.
		'''
		try:
			isValidStatus = self._checkReponseStatus(response)
		except:
			raise
		else:
			if not isValidStatus:
				if self.isVerboseMode:
					print 'Empty result!'
				return

			resultMaps = response.get('results', [])
			# Indicate whether there is next page of results
			next_page_token = response.get('next_page_token')

			if resultMaps:
				for index, resultMap in enumerate(resultMaps, 1):
					placeId = resultMap.get('place_id')
					types = resultMap.get('types', [])
					icon = resultMap.get('icon')
					name = resultMap.get('name')
					location = resultMap.get('geometry', {}).get('location', {})
					if self.isVerboseMode:
						print '--' * 20
						print 'index: {}, name: {}, types: {}, location: {}'.format(index, name, types, location)

				if next_page_token:
					retry_count = 0
					isValidStatus = False

					while not isValidStatus and retry_count <= MAX_NEXT_PAGE_TOKEN_RETRY_COUNT:
						# Sometimes there is delay when next_page_token is issued, sleep 1s and retry 3 times.
						time.sleep(2)

						if retry_count and self.isVerboseMode:
							print 'Retry {} times...'.format(retry_count)
						try: 
							self.nearbySearch(page_token=next_page_token)
						except Exception as e:
							retry_count += 1
							if self.isVerboseMode:
								print 'Exception {} when fetching next page by using token.'.format(e)
								if retry_count > MAX_NEXT_PAGE_TOKEN_RETRY_COUNT:
									print 'Already reached maximum retry times: {}, exit...'.format(MAX_NEXT_PAGE_TOKEN_RETRY_COUNT)
						else:
							isValidStatus = True

	def _parseRadarSearchResponse(self, response):
		'''
		Private helper method that will parse response of radar search.
		'''
		try:
			isValidStatus = self._checkReponseStatus(response)
		except:
			raise
		else:
			if not isValidStatus:
				if self.isVerboseMode:
					print 'Empty result!'
				return

			resultMaps = response.get('results', [])

			if resultMaps:
				for index, resultMap in enumerate(resultMaps, 1):
					placeId = resultMap.get('place_id')
					location = resultMap.get('geometry', {}).get('location', {})
					if self.isVerboseMode:
						print '--' * 20
						print 'index: {}, location: {}'.format(index, location)

	def nearbySearch(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None, page_token=None):
		'''
		Google nearby search, 20 results max for 1 page and 60 results max for 1 query.
		'''
		filterKwargs = self._getPlaceFilterKwargs(place_type, radius, keyword, name, rank_by, page_token)
		response = self.client.places_nearby(**filterKwargs)
		self._parseNearbySearchResponse(response)

	def radarSearch(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None):
		'''
		Google radar search, 200 results max for 1 query, less details included.
		'''
		filterKwargs = self._getPlaceFilterKwargs(place_type, radius, keyword, name, rank_by)
		response = self.client.places_radar(**filterKwargs)
		self._parseRadarSearchResponse(response)
