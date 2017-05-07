# Put Standard Library Imports Here:
import time

# Put Third Party/Django Imports Here:
import googlemaps

# Put Alivee Imports Here:
from .constants import MAX_PLACE_SERACH_RADIUS_IN_METERS
from .constants import PLACE_SEARCH_REQUEST_PLACE_TYPES
from .constants import PlaceSearchRankByMethod
from .constants import PlaceSearchResponseStatus
from .exceptions import ConflictRequestRadiusRankByException
from .exceptions import ExceedMaximumNextPageRetryTimesException
from .exceptions import ExceedRequestMaximumRadiusException
from .exceptions import IncompleteRequestRankByRelatedParamsException
from .exceptions import InvalidRequestPlaceTypeException
from .exceptions import InvalidResponseStatusException

MAX_NEXT_PAGE_TOKEN_RETRY_COUNT = 3


class PlaceSearch(object):
	'''
	Wrapped google place search service for our usage.
	Documents: https://developers.google.com/places/web-service/intro

	Usage example: Search all banks in 1000 meters radius area of location (37.7845782, -122.3910999)

	placeSearchInstance = PlaceSearch(
		location=(37.7845782, -122.3910999), 
		key=key,
	)

	placeSearchInstance.nearbySearch(
		place_type=PlaceSearchPlaceType.BANK, 
		radius=1000,
	)
	OR:
	placeSearchInstance.radarSearch(
		place_type=PlaceSearchPlaceType.BANK, 
		radius=1000,
	)
	'''
	def __init__(self, location, key):
		'''
		Init method of place search class.

		param location: A tuple (lat, lng) represents the location we want to set as the center of the search area.
		param key: The Google API key, generated in google dev console, ask project dev for help.
		'''
		self.location = location
		# NOTE: Need to handle exception in caller's method such as `ValueError: Invalid API key provided.`
		self.client = googlemaps.Client(key)

	def _getPlaceFilterKwargs(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None, 
		page_token=None):
		'''
		Private helper method to pre-check and create the filter kwargs in place search query, follow format of
		https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/places.py#L199

		return: A map includes all params in place search query.

		NOTE: Pre-check is needed to avoid obviously invalid API call, thus saving query count.
		'''
		filterKwargs = dict(location=self.location)

		if place_type:
			# Check then include `place type` info.
			if not place_type in PLACE_SEARCH_REQUEST_PLACE_TYPES:
				raise InvalidRequestPlaceTypeException(placeType=place_type)
			filterKwargs['type'] = place_type

		if radius:
			# Check then include `radius` info.
			if radius > MAX_PLACE_SERACH_RADIUS_IN_METERS:
				raise ExceedMaximumRequestRadiusException(radius=radius, maxRadius=MAX_PLACE_SERACH_RADIUS_IN_METERS)
			filterKwargs['radius'] = radius

		if keyword:
			# Check then include `keyword` info.
			filterKwargs['keyword'] = keyword

		if name:
			# Check then include `name` info.
			filterKwargs['name'] = name

		if rank_by:
			# Check then include `rank_by` info.
			if rank_by == PlaceSearchRankByMethod.DISTANCE:

				if radius:
					raise ConflictRequestRadiusRankByException()

				if (not place_type) and (not keyword) and (not name):
					raise IncompleteRequestRankByRelatedParamsException()

			filterKwargs['rank_by'] = rank_by

		if page_token:
			# Check then include `page_token` info.
			filterKwargs['page_token'] = page_token

		return filterKwargs

	def _checkReponseStatus(self, response):
		'''
		Private helper method to check if the status of google place search response is valid.

		param response: Response of google place search query, notice `googlemaps` package already parses the 
		JSON format response to `dict - list` format for us.
		return: `True` means the status in response is valid, otherwise an InvalidResponseStatusException will be raised.
		'''
		response = response or {}
		status = response.get('status')

		if status not in [PlaceSearchResponseStatus.OK.value, PlaceSearchResponseStatus.ZERO_RESULTS.value]:
			raise InvalidResponseStatusException(status=status)

		return True

	def _parseNearbySearchResponse(self, response):
		'''
		Private helper method to parse response of nearby search.

		param response: Response of google place nearby search query.
		return: A list of all parsed results for place search query.

		NOTE: Retry for next page fetch query happens here while retry for base place search query 
		should be handled in caller's method.
		'''
		allParsedResults = []

		try:
			self._checkReponseStatus(response=response)
		except:
			raise
		else:
			resultMaps = response.get('results', [])
			# Indicate whether there is next page of results since maximum results number show in 1 page is 20.
			next_page_token = response.get('next_page_token')

			for resultMap in resultMaps:
				allParsedResults.append(dict(
					placeId=resultMap.get('place_id'),
					types=resultMap.get('types', []),
					icon=resultMap.get('icon'),
					name=resultMap.get('name'),
					location=resultMap.get('geometry', {}).get('location', {}),
				))

			if next_page_token:
				retry_count = 0
				hasNextPageResult = False

				while not hasNextPageResult and retry_count <= MAX_NEXT_PAGE_TOKEN_RETRY_COUNT:
					# Sometimes there is delay when `next_page_token` is issued, sleep 2 seconds and retry 3 times.
					time.sleep(2)

					try: 
						nextPageParsedResults = self.nearbySearch(page_token=next_page_token, isVerboseMode=False)
					except:
						retry_count += 1
						if retry_count > MAX_NEXT_PAGE_TOKEN_RETRY_COUNT:
							raise ExceedMaximumNextPageRetryTimesException(maxRetryTimes=MAX_NEXT_PAGE_TOKEN_RETRY_COUNT)
					else:
						hasNextPageResult = True
						allParsedResults.extend(nextPageParsedResults)

		return allParsedResults

	def _parseRadarSearchResponse(self, response):
		'''
		Private helper method that will parse response of radar search.

		param response: Response of google place radar search query.
		return: A list of all parsed results for place search query.
		'''
		allParsedResults = []

		try:
			hasResult = self._checkReponseStatus(response)
		except:
			raise
		else:
			if hasResult:
				resultMaps = response.get('results', [])

				for resultMap in resultMaps:
					allParsedResults.append(dict(
						placeId=resultMap.get('place_id'),
						location=resultMap.get('geometry', {}).get('location', {}),
					))

		return allParsedResults

	def nearbySearch(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None, page_token=None, 
		isVerboseMode=True):
		'''
		Wrapped google place nearby search, 20 results max for 1 page and 60 results max for 1 query.
		Documents: https://developers.google.com/places/web-service/search

		param isVerboseMode: A boolean flag indicates if helper text will be printed for debugging.
		return: A list of all parsed results for place search query.

		NOTE: Not all params included for query search such as `minprice` and `maxprice`, if needed, more params
		can be added later.
		'''
		filterKwargs = self._getPlaceFilterKwargs(place_type, radius, keyword, name, rank_by, page_token)
		response = self.client.places_nearby(**filterKwargs)
		allParsedResults = self._parseNearbySearchResponse(response)

		if isVerboseMode:
			if not allParsedResults:
				print 'No results found in nearby response, do nothing!'
			else:
				for index, parsedResult in enumerate(allParsedResults, 1):
					print '--' * 20
					# For unicode output, see https://pythonhosted.org/kitchen/unicode-frustrations.html
					print 'index: {}, name: {}, location: {}'.format(
						index, parsedResult.get('name').encode('utf8', 'replace'), parsedResult.get('location'))
					print 'placeId: {}, icon: {}\n'.format(parsedResult.get('placeId'), parsedResult.get('icon'))

		return allParsedResults

	def radarSearch(self, place_type=None, radius=None, keyword=None, name=None, rank_by=None, isVerboseMode=True):
		'''
		Wrapped google place radar search, 200 results max for 1 query, less details included.
		Documents: https://developers.google.com/places/web-service/search#RadarSearchRequests

		param isVerboseMode: A boolean flag indicates if helper text will be printed for debugging.
		return: A list of all parsed results for place search query.

		NOTE: Not all params are included for query search such as `minprice` and `maxprice`, if needed, more params
		can be added later.
		'''
		filterKwargs = self._getPlaceFilterKwargs(place_type, radius, keyword, name, rank_by, page_token=None)
		response = self.client.places_radar(**filterKwargs)
		allParsedResults = self._parseRadarSearchResponse(response)

		if isVerboseMode:
			if not allParsedResults:
				print 'No results found in radar response, do nothing!'
			else:
				for index, parsedResult in enumerate(allParsedResults, 1):
					print '--' * 20
					print 'index: {}, placeId: {}, location: {}\n'.format(
						index, parsedResult.get('placeId'), parsedResult.get('location'))

		return allParsedResults
