# Put Standard Library Imports Here:
import math
import time

# Put Third Party/Django Imports Here:
from geopy.distance import vincenty

# Put Alivee Imports Here:
from general_utils.requests.google.place_search.constants import PlaceSearchPlaceType
from general_utils.requests.google.place_search.exceptions import ExceedMaximumMainRequestRetryCountException
from general_utils.requests.google.place_search.utils import PlaceSearch
from place_search_engine.constants import CityBoundaryPointsInfo

MAX_BACKFILL_RADIUS_IN_METERS = 1500


def _getDistanceBetweenTwoPoints(point1, point2):
	'''
	Private helper method to get distance in meters for 2 points.

	param point1: First point in tuple format: (lat, lng).
	param point2: Second point in tuple format: (lat, lng).
	return: Distance of 2 points in meters.
	'''
	return vincenty(point1, point2).meters


def _getBackfillCenterPoints(upperLeftPoint, lowerRightPoint, width, height):
	'''
	Private helper method to get backfill center points for rectangle areas.

	param width: The real distance between left and right points, in meters.
	param height: The real distance between upper and lower points, in meters. 
	return: A tuple (backfillRadius, backfillPoints)
	'''
	# Potential count of points in width and height direction when we use max radius to divide. Call it 
	# `potential` since not all points will be included according to our `checkerboard` style backfill strategy.
	potentialPointsCountInWidthDir = int(math.ceil(width / MAX_BACKFILL_RADIUS_IN_METERS)) + 1
	potentialPointsCountInHeightDir = int(math.ceil(height / MAX_BACKFILL_RADIUS_IN_METERS)) + 1

	backfillCenterPointsToInclude = []
	(currentLat, currentLng), (lastLat, lastLng) = upperLeftPoint, lowerRightPoint
	isPointToIncludeInHeightDir = True

	for heightIndex in xrange(potentialPointsCountInHeightDir):
		# Set `currentLng` to current value in height direction by using height index.
		currentLng = currentLng + (lastLng - currentLng) * heightIndex / (potentialPointsCountInHeightDir - 1)
		isPointToIncludeInWidthDir = isPointToIncludeInHeightDir

		for widthIndex in xrange(potentialPointsCountInWidthDir):
			# Set `currentLat` to current value in width direction by using width index.
			currentLat = currentLat + (lastLat - currentLat) * widthIndex / (potentialPointsCountInWidthDir - 1)
			if isPointToIncludeInWidthDir:
				backfillCenterPointsToInclude.append([currentLat, currentLng])

			isPointToIncludeInWidthDir = not isPointToIncludeInWidthDir

		isPointToIncludeInHeightDir = not isPointToIncludeInHeightDir

	backfillRadius = max(width / ((potentialPointsCountInWidthDir - 1)), height / (potentialPointsCountInHeightDir - 1))

	return backfillRadius, backfillCenterPointsToInclude


def backfillPlaces(key, boundaryPointsInfo=None, isVerboseMode=True, saveToDb=True):
	'''
	Util method for backfilling all places we are insterested in the rectangle area defined by boundary points.
	TODO(Yang): Need to consume parsed data to db after completing models.

	param key: The Google API key, generated in google dev console, ask project dev for help.
	param boundaryPointsInfo: The boundary points info, describing the rectangle area we want to backfill. 
	param isVerboseMode: A boolean flag indicates if helper text will be printed for debugging.
	param saveToDb: A boolean flag indicates whether parsed data will be saved to database.
	'''
	if not boundaryPointsInfo:
		boundaryPointsInfo = [boundaryPointsInfo.value for boundaryPointsInfo in CityBoundaryPointsInfo]

	backfillAreaInfos = []

	for boundaryPoints in boundaryPointsInfo:
		for upperLeftPoint, upperRightPoint, lowerRightPoint, lowerLeftPoint in boundaryPoints:
			areaWidth = _getDistanceBetweenTwoPoints(upperLeftPoint, upperRightPoint)
			areaHight = _getDistanceBetweenTwoPoints(upperRightPoint, lowerRightPoint)

			backfillRadius, backfillCenterPointsToInclude = _getBackfillCenterPoints(
				upperLeftPoint=upperLeftPoint, 
				lowerRightPoint=lowerRightPoint,
				width=areaWidth,
				height=areaHight,
			)
			backfillAreaInfos.append((areaWidth, areaHight, backfillCenterPointsToInclude, backfillRadius))

	for areaIndex, (areaWidth, areaHight, centerPoints, radius) in enumerate(backfillAreaInfos, 1):
		if isVerboseMode:
			print '\n' + '==' * 20
			print 'Area index: {}, width: {}, height: {}, # of center points: {}, radius: {}.'.format(
				areaIndex, areaWidth, areaHight, len(centerPoints), radius)

		radius = int(radius)
		for centerPointIndex, centerPoint in enumerate(centerPoints, 1):
			if isVerboseMode:
				print '--' * 20
				print 'Nearby search for center point index: {}, center point: {}, radius: {}.'.format(
					centerPointIndex, centerPoint, radius)

			googlePlaceSearch = PlaceSearch(key=key, location=centerPoint)

			try:
				allParsedResults = googlePlaceSearch.nearbySearch(PlaceSearchPlaceType.RESTAURANT.value, radius)
			except ExceedMaximumMainRequestRetryCountException:
				# Following query with different center point may not fail, skip current center point.
				if isVerboseMode:
					print 'Nearby search failed for {} with radius {}, so skip.'.format(centerPoint, radius)
				pass

			time.sleep(1)
