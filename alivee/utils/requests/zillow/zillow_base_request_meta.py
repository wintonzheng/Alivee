from utils.requests.zillow.exceptions import EmptyAreaInputException
from utils.requests.request_meta import RequestMeta


class ZillowBaseRequestMeta(RequestMeta):
    HOST = 'www.zillow.com'

    def __init__(self, service_id, path, params=None):
        self.service_id = service_id
        params = params or {}
        params['zws-id'] = self.service_id
        super(ZillowBaseRequestMeta, self).__init__(self.HOST,
                                                    path=path,
                                                    params=params,
                                                    method='GET',
                                                    protocol='http')

    def validMethods(self):
        return ('GET')

    @staticmethod
    def getArea(city, state, zipCode):
        if not city and not state and not zipCode:
            raise EmptyAreaInputException
        area = ''
        if city:
            area = city
        if state:
            area = '{0}, {1}'.format(area, state)
        if zipCode:
            if area:
                area = '{0} {1}'.format(area, zipCode)
            else:
                area = zipCode
        return area
