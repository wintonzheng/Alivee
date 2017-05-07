'''
File includes rectangle boundary points info for cities.

Format: A list of rectangle boundary points included for that city, one city may exist multiple rectangle boundaries
for backfill purpose (divide poly to multiple rectangles): [upperLeft, upperRight, lowerRight, lowerLeft].

Use rectangle for now to represent boundary of city so it will be easy to find backfill center points.
'''
# Put Standard Library Imports Here:
from enum import Enum


SAN_FRANCISCO = [
	[
		[37.815689, -122.517018],
		[37.815689, -122.366381],
		[37.708184, -122.366381],
		[37.708184, -122.517018],
	],
]


class CityBoundaryPointsInfo(Enum):
	SAN_FRANCISCO = SAN_FRANCISCO
