'''
File includes constants needed for google place search API.
'''
# Put Standard Library Imports Here:
from enum import Enum


class PlaceSearchResponseStatus(Enum):
	'''
	Class includes all statuses of response from Google place search API.
	Documents: https://developers.google.com/places/web-service/search#PlaceSearchStatusCodes
	'''
	OK = 'OK'
	ZERO_RESULTS = 'ZERO_RESULTS'
	OVER_QUERY_LIMIT = 'OVER_QUERY_LIMIT'
	REQUEST_DENIED = 'REQUEST_DENIED'
	INVALID_REQUEST = 'INVALID_REQUEST'


class PlaceSearchRankByMethod(Enum):
	'''
	class includes all methods rank_by param can use.
	Documents: https://developers.google.com/places/web-service/search#PlaceSearchRequests
	'''
	PROMINENCE = 'prominence'
	DISTANCE = 'distance'


class PlaceSearchPlaceType(Enum):
	'''
	Class includes all place types we can use in place service query, deprecated types are not listed.
	Documents: https://developers.google.com/places/web-service/supported_types
	'''
	ACCOUNTING = 'accounting'
	AIRPORT = 'airport'
	AMUSEMENT_PARK = 'amusement_park'
	AQUARIUM = 'aquarium'
	ART_GALLERY = 'art_gallery'
	ATM = 'atm'
	BAKERY = 'bakery'
	BANK = 'bank'
	BAR = 'bar'
	BEAUTY_SALON = 'beauty_salon'
	BICYCLE_STORE = 'bicycle_store'
	BOOK_STORE = 'book_store'
	BOWLING_ALLEY = 'bowling_alley'
	BUS_STATION = 'bus_station'
	CAFE = 'cafe'
	CAMPGROUND = 'campground'
	CAR_DEALER = 'car_dealer'
	CAR_RENTAL = 'car_rental'
	CAR_REPAIR = 'car_repair'
	CAR_WASH = 'car_wash'
	CASINO = 'casino'
	CEMETERY = 'cemetery'
	CHURCH = 'church'
	CITY_HALL = 'city_hall'
	CLOTHING_STORE = 'clothing_store'
	CONVENIENCE_STORE = 'convenience_store'
	COURTHOUSE = 'courthouse'
	DENTIST = 'dentist'
	DEPARTMENT_STORE = 'department_store'
	DOCTOR = 'doctor'
	ELECTRICIAN = 'electrician'
	ELECTRONICS_STORE = 'electronics_store'
	EMBASSY = 'embassy'
	FIRE_STATION = 'fire_station'
	FLORIST = 'florist'
	FUNERAL_HOME = 'funeral_home'
	FURNITURE_STORE = 'furniture_store'
	GAS_STATION = 'gas_station'
	GYM = 'gym'
	HAIR_CARE = 'hair_care'
	HARDWARE_STORE = 'hardware_store'
	HINDU_TEMPLE = 'hindu_temple'
	HOME_GOODS_STORE = 'home_goods_store'
	HOSPITAL = 'hospital'
	INSURANCE_AGENCY = 'insurance_agency'
	JEWELRY_STORE = 'jewelry_store'
	LAUNDRY = 'laundry'
	LAWYER = 'lawyer'
	LIBRARY = 'library'
	LIQUOR_STORE = 'liquor_store'
	LOCAL_GOVERNMENT_OFFICE = 'local_government_office'
	LOCKSMITH = 'locksmith'
	LODGING = 'lodging'
	MEAL_DELIVERY = 'meal_delivery'
	MEAL_TAKEAWAY = 'meal_takeaway'
	MOSQUE = 'mosque'
	MOVIE_RENTAL = 'movie_rental'
	MOVIE_THEATER = 'movie_theater'
	MOVING_COMPANY = 'moving_company'
	MUSEUM = 'museum'
	NIGHT_CLUB = 'night_club'
	PAINTER = 'painter'
	PARK = 'park'
	PARKING = 'parking'
	PET_STORE = 'pet_store'
	PHARMACY = 'pharmacy'
	PHYSIOTHERAPIST = 'physiotherapist'
	PLUMBER = 'plumber'
	POLICE = 'police'
	POST_OFFICE = 'post_office'
	REAL_ESTATE_AGENCY = 'real_estate_agency'
	RESTAURANT = 'restaurant'
	ROOFING_CONTRACTOR = 'roofing_contractor'
	RV_PARK = 'rv_park'
	SCHOOL = 'school'
	SHOE_STORE = 'shoe_store'
	SHOPPING_MALL = 'shopping_mall'
	SPA = 'spa'
	STADIUM = 'stadium'
	STORAGE = 'storage'
	STORE = 'store'
	SUBWAY_STATION = 'subway_station'
	SYNAGOGUE = 'synagogue'
	TAXI_STAND = 'taxi_stand'
	TRAIN_STATION = 'train_station'
	TRANSIT_STATION = 'transit_station'
	TRAVEL_AGENCY = 'travel_agency'
	UNIVERSITY = 'university'
	VETERINARY_CARE = 'veterinary_care'
	ZOO = 'zoo'
	ADMINISTRATIVE_AREA_LEVEL_1 = 'administrative_area_level_1'
	ADMINISTRATIVE_AREA_LEVEL_2 = 'administrative_area_level_2'
	ADMINISTRATIVE_AREA_LEVEL_3 = 'administrative_area_level_3'
	ADMINISTRATIVE_AREA_LEVEL_4 = 'administrative_area_level_4'
	ADMINISTRATIVE_AREA_LEVEL_5 = 'administrative_area_level_5'
	COLLOQUIAL_AREA = 'colloquial_area'
	COUNTRY = 'country'
	ESTABLISHMENT = 'establishment'
	FINANCE = 'finance'
	FLOOR = 'floor'
	FOOD = 'food'
	GENERAL_CONTRACTOR = 'general_contractor'
	GEOCODE = 'geocode'
	HEALTH = 'health'
	INTERSECTION = 'intersection'
	LOCALITY = 'locality'
	NATURAL_FEATURE = 'natural_feature'
	NEIGHBORHOOD = 'neighborhood'
	PLACE_OF_WORSHIP = 'place_of_worship'
	POLITICAL = 'political'
	POINT_OF_INTEREST = 'point_of_interest'
	POST_BOX = 'post_box'
	POSTAL_CODE = 'postal_code'
	POSTAL_CODE_PREFIX = 'postal_code_prefix'
	POSTAL_CODE_SUFFIX = 'postal_code_suffix'
	POSTAL_TOWN = 'postal_town'
	PREMISE = 'premise'
	ROOM = 'room'
	ROUTE = 'route'
	STREET_ADDRESS = 'street_address'
	STREET_NUMBER = 'street_number'
	SUBLOCALITY = 'sublocality'
	SUBLOCALITY_LEVEL_5 = 'sublocality_level_5'
	SUBLOCALITY_LEVEL_4 = 'sublocality_level_4'
	SUBLOCALITY_LEVEL_3 = 'sublocality_level_3'
	SUBLOCALITY_LEVEL_2 = 'sublocality_level_2'
	SUBLOCALITY_LEVEL_1 = 'sublocality_level_1'
	SUBPREMISE = 'subpremise'


# Place types supported as param in place search request query.
# Documents: https://developers.google.com/places/web-service/supported_types#table1
_PLACE_SEARCH_REQUEST_PLACE_MAPS= [
	PlaceSearchPlaceType.ACCOUNTING,
	PlaceSearchPlaceType.AIRPORT,
	PlaceSearchPlaceType.AMUSEMENT_PARK,
	PlaceSearchPlaceType.AQUARIUM,
	PlaceSearchPlaceType.ART_GALLERY,
	PlaceSearchPlaceType.ATM,
	PlaceSearchPlaceType.BAKERY,
	PlaceSearchPlaceType.BANK,
	PlaceSearchPlaceType.BAR,
	PlaceSearchPlaceType.BEAUTY_SALON,
	PlaceSearchPlaceType.BICYCLE_STORE,
	PlaceSearchPlaceType.BOOK_STORE,
	PlaceSearchPlaceType.BOWLING_ALLEY,
	PlaceSearchPlaceType.BUS_STATION,
	PlaceSearchPlaceType.CAFE,
	PlaceSearchPlaceType.CAMPGROUND,
	PlaceSearchPlaceType.CAR_DEALER,
	PlaceSearchPlaceType.CAR_RENTAL,
	PlaceSearchPlaceType.CAR_REPAIR,
	PlaceSearchPlaceType.CAR_WASH,
	PlaceSearchPlaceType.CASINO,
	PlaceSearchPlaceType.CEMETERY,
	PlaceSearchPlaceType.CHURCH,
	PlaceSearchPlaceType.CITY_HALL,
	PlaceSearchPlaceType.CLOTHING_STORE,
	PlaceSearchPlaceType.CONVENIENCE_STORE,
	PlaceSearchPlaceType.COURTHOUSE,
	PlaceSearchPlaceType.DENTIST,
	PlaceSearchPlaceType.DEPARTMENT_STORE,
	PlaceSearchPlaceType.DOCTOR,
	PlaceSearchPlaceType.ELECTRICIAN,
	PlaceSearchPlaceType.ELECTRONICS_STORE,
	PlaceSearchPlaceType.EMBASSY,
	PlaceSearchPlaceType.FIRE_STATION,
	PlaceSearchPlaceType.FLORIST,
	PlaceSearchPlaceType.FUNERAL_HOME,
	PlaceSearchPlaceType.FURNITURE_STORE,
	PlaceSearchPlaceType.GAS_STATION,
	PlaceSearchPlaceType.GYM,
	PlaceSearchPlaceType.HAIR_CARE,
	PlaceSearchPlaceType.HARDWARE_STORE,
	PlaceSearchPlaceType.HINDU_TEMPLE,
	PlaceSearchPlaceType.HOME_GOODS_STORE,
	PlaceSearchPlaceType.HOSPITAL,
	PlaceSearchPlaceType.INSURANCE_AGENCY,
	PlaceSearchPlaceType.JEWELRY_STORE,
	PlaceSearchPlaceType.LAUNDRY,
	PlaceSearchPlaceType.LAWYER,
	PlaceSearchPlaceType.LIBRARY,
	PlaceSearchPlaceType.LIQUOR_STORE,
	PlaceSearchPlaceType.LOCAL_GOVERNMENT_OFFICE,
	PlaceSearchPlaceType.LOCKSMITH,
	PlaceSearchPlaceType.LODGING,
	PlaceSearchPlaceType.MEAL_DELIVERY,
	PlaceSearchPlaceType.MEAL_TAKEAWAY,
	PlaceSearchPlaceType.MOSQUE,
	PlaceSearchPlaceType.MOVIE_RENTAL,
	PlaceSearchPlaceType.MOVIE_THEATER,
	PlaceSearchPlaceType.MOVING_COMPANY,
	PlaceSearchPlaceType.MUSEUM,
	PlaceSearchPlaceType.NIGHT_CLUB,
	PlaceSearchPlaceType.PAINTER,
	PlaceSearchPlaceType.PARK,
	PlaceSearchPlaceType.PARKING,
	PlaceSearchPlaceType.PET_STORE,
	PlaceSearchPlaceType.PHARMACY,
	PlaceSearchPlaceType.PHYSIOTHERAPIST,
	PlaceSearchPlaceType.PLUMBER,
	PlaceSearchPlaceType.POLICE,
	PlaceSearchPlaceType.POST_OFFICE,
	PlaceSearchPlaceType.REAL_ESTATE_AGENCY,
	PlaceSearchPlaceType.RESTAURANT,
	PlaceSearchPlaceType.ROOFING_CONTRACTOR,
	PlaceSearchPlaceType.RV_PARK,
	PlaceSearchPlaceType.SCHOOL,
	PlaceSearchPlaceType.SHOE_STORE,
	PlaceSearchPlaceType.SHOPPING_MALL,
	PlaceSearchPlaceType.SPA,
	PlaceSearchPlaceType.STADIUM,
	PlaceSearchPlaceType.STORAGE,
	PlaceSearchPlaceType.STORE,
	PlaceSearchPlaceType.SUBWAY_STATION,
	PlaceSearchPlaceType.SYNAGOGUE,
	PlaceSearchPlaceType.TAXI_STAND,
	PlaceSearchPlaceType.TRAIN_STATION,
	PlaceSearchPlaceType.TRANSIT_STATION,
	PlaceSearchPlaceType.TRAVEL_AGENCY,
	PlaceSearchPlaceType.UNIVERSITY,
	PlaceSearchPlaceType.VETERINARY_CARE,
	PlaceSearchPlaceType.ZOO,
]
PLACE_SEARCH_REQUEST_PLACE_TYPES = [placeType.value for placeType in _PLACE_SEARCH_REQUEST_PLACE_MAPS]

# Place types could be retured in place search response.
# Documents: https://developers.google.com/places/web-service/supported_types#table2
PLACE_SEARCH_RESPONSE_PLACE_TYPES = [placeType.value for placeType in PlaceSearchPlaceType]

# Documents: Search keyword `radius` in https://developers.google.com/places/web-service/search
MAX_PLACE_SERACH_RADIUS_IN_METERS = 50000
