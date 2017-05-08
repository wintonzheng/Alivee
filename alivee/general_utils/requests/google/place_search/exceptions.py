class BaseGooglePlaceSearchException(Exception):
    pass


class InvalidResponseStatusException(BaseGooglePlaceSearchException):
    '''
    Raised when response of google place search does not have invalid status.
    '''
    def __init__(self, status):
        self.status = status
        msg = 'Invalid response status: {}!'.format(self.status)
        super(InvalidResponseStatusException, self).__init__(msg)


class InvalidRequestAPIKeyException(BaseGooglePlaceSearchException):
    '''
    Raised when api key is not valid and declined by google place search server.
    '''
    def __init__(self, key):
        self.key = key
        msg = 'Invalid API key provided: {}!'.format(self.key)
        super(InvalidRequestAPIKeyException, self).__init__(msg)


class InvalidRequestPlaceTypeException(BaseGooglePlaceSearchException):
    '''
    Raised when request of google place search does not include valid place type.
    '''
    def __init__(self, placeType):
        self.placeType = placeType
        msg = 'Invalid request place type: {}!'.format(self.placeType)
        super(InvalidRequestPlaceTypeException, self).__init__(msg)


class ConflictRequestRadiusRankByException(BaseGooglePlaceSearchException):
    '''
    Raised when `rank_by = distance` and `radius` param is included at the same time.
    '''
    def __init__(self):
        msg = 'The radius must not be included if rankby = distance!'
        super(ConflictRequestRadiusRankByException, self).__init__(msg)


class ExceedRequestMaximumRadiusException(BaseGooglePlaceSearchException):
    '''
    Raised when radius in request of google place search exceeds the maximum allowed value.
    '''
    def __init__(self, radius, maxRadius):
        self.radius = radius
        self.maxRadius = maxRadius
        msg = 'Radius: {} exceeds maximum allowed value: {}!'.format(self.radius, self.maxRadius)
        super(ExceedRequestMaximumRadiusException, self).__init__(msg)


class IncompleteRequestRankByRelatedParamsException(BaseGooglePlaceSearchException):
    '''
    Raised when `rank_by = distance` and none of `keyword`, `name` and `type` params is included.
    '''
    def __init__(self):
        msg = 'One or more of keyword, name, or type params is required when rank_by = distance!'
        super(IncompleteRequestRankByRelatedParamsException, self).__init__(msg)


class ExceedMaximumNextPageRequestRetryCountException(Exception):
    '''
    Raised when next page retry count exceed the maximum value.
    '''
    def __init__(self, maxRetryCount):
        self.maxRetryCount = maxRetryCount
        msg = 'Already reached maximum next page request retry count: {}!'.format(self.maxRetryCount)
        super(ExceedMaximumNextPageRequestRetryCountException, self).__init__(msg)


class ExceedMaximumMainRequestRetryCountException(Exception):
    '''
    Raised when main request retry count exceed the maximum value.
    '''
    def __init__(self, maxRetryCount):
        self.maxRetryCount = maxRetryCount
        msg = 'Already reached maximum main request retry count: {}!'.format(self.maxRetryCount)
        super(ExceedMaximumMainRequestRetryCountException, self).__init__(msg)
