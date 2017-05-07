from django.test import TestCase

from utils.requests.zillow.zillow_deep_search_result_request_meta \
    import ZillowDeepSearchResultsRequestMeta


class TestZillowDeepSearchResultsRequestMeta(TestCase):

    def testBasic(self):
        city = 'San Francisco'
        state = 'CA'
        zipCode = '11111'
        meta = ZillowDeepSearchResultsRequestMeta(
            'fake_service_id',
            '333 test st',
            city=city,
            state=state,
            zipCode=zipCode
        )
        self.assertEqual(meta.host, 'www.zillow.com')
        self.assertEqual(meta.path, 'howto/api/GetDeepSearchResults.htm')
        self.assertEqual(meta.protocol, 'http')
        self.assertEqual(
            ZillowDeepSearchResultsRequestMeta.getArea(city, state, zipCode),
            'San Francisco, CA 11111'
        )
        self.assertDictEqual(
            meta.params,
            {
                'zws-id': 'fake_service_id',
                'address': '333 test st',
                'citystatezip': 'San Francisco, CA 11111',
                'rentzestimate': False
            }
        )
        self.assertEqual(
            meta.url,
            'http://www.zillow.com/howto/api/GetDeepSearchResults.htm?zws-id=fake_service_id&citystatezip=San+Francisco%2C+CA+11111&rentzestimate=False&address=333+test+st'  # nopep8
        )
