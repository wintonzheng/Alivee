# Put Standard Library Imports Here:
import math

# Put Third Party/Django Imports Here:
from geopy.distance import vincenty

# Put Alivee Imports Here:
from place_search_engine.constants import CityBoundaryPointsInfo

MAX_BACKFILL_RADIUS_IN_METERS = 1500


def _getDistanceBetweenTwoPoints(point1, point2):
	'''
	Private helper method to get distance in meters for 2 points. 
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


def backfillPlaces(boundaryPointsInfo=None, isVerboseMode=True):
	'''
	Util method for backfilling all places we are insterested in the rectangle area defined by boundary points.
	'''
	if not boundaryPointsInfo:
		boundaryPointsInfo = [CityBoundaryPointsInfo.SAN_FRANCISCO]

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

			if isVerboseMode:
				print 'Width of rectangle area:', areaWidth
				print 'Height of rectangle area:', areaHight
				print 'The center points to include:', backfillCenterPointsToInclude
				print 'Backfill radius in meters:', backfillRadius



