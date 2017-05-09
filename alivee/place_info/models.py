# Put Third Party/Django Imports Here:
from django.db import models

# Put Alivee Imports Here:
from general_utils.models import TruncatingCharField
from general_utils.models import ValidationMixin
from general_utils.requests.google.place_search.constants import PlaceSearchPlaceType


class Location(models.Model):
    '''
    Anstract model for geo location of place, considering the precision of the distance, documents:
    `http://stackoverflow.com/questions/15965166/what-is-the-maximum-length-of-latitude-and-longitude?noredirect=1&lq=1`
    `0.0000001` difference in degree results in `0.01 m` difference in distance which is accurate enough.
    '''
    lat = models.DecimalField(verbose_name='latitude of location', max_digits=9, decimal_places=7)
    lng = models.DecimalField(verbose_name='longitude of location', max_digits=10, decimal_places=7)

    class Meta:
        abstract = True


class Place(Location, ValidationMixin):
    '''
    Model for featured place, it may be associated with multiple place types.
    '''
    placeId = models.CharField(verbose_name='unique google place_id foreign key', max_length=255)
    name = TruncatingCharField(max_length=255, null=True)
    icon = TruncatingCharField(max_length=255, null=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'place'


class PlaceType(models.Model):
    '''
    Model for place type.
    '''
    value = models.CharField(max_length=255, choices=PlaceSearchPlaceType.__members__)
    isActive = models.BooleanField(default=True)
    place = models.ForeignKey(Place, related_name='placeTypes')

    class Meta:
        db_table = 'place_type'
