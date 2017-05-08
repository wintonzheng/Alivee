import requests

from utils.requests.zillow.zillow_base_request_meta import ZillowBaseRequestMeta


class ZillowDeepSearchResultsRequestMeta(ZillowBaseRequestMeta):
    '''
    Request metadata for zillow GetDeepSearch-Results API:
    https://www.zillow.com/howto/api/GetDeepSearchResults.htm
    '''
    PATH = 'howto/api/GetDeepSearchResults.htm'

    def __init__(self,
                 service_id,
                 address,
                 city=None,
                 state=None,
                 zipCode=None,
                 rentEstimate=False):
        params = {
            'address': address,
            'citystatezip': self.getArea(city, state, zipCode),
            'rentzestimate': rentEstimate
        }
        super(ZillowDeepSearchResultsRequestMeta, self).__init__(service_id, self.PATH, params)

    def make_request(self):
        response = requests.request(self.method, self.url)
        return response
