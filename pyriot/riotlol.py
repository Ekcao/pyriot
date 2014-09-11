import requests


class RiotLOL():

    api_versions = {
        'champion': 1.2,
        'game': 1.3,
        'league': 2.5,
        'lol-static-data': 1.2,
        'match': 2.2,
        'matchhistory': 2.2,
        'stats': 1.3,
        'summoner': 1.4,
        'team': 2.4
    }

    api_urls = {
        'lol-static-data': '{base}/static-data/{region}/v{version}/{field}'
    }

    def __init__(self, api_key, region='na'):
        self.region = region
        self.api_key = {'api_key': api_key}
        self.base_url = 'https://{region}.api.pvp.net/api/lol'.format(
            region=self.region
        )

    def latest_version(self):
        return self.make_request('lol-static-data', 'versions')[0]

    def make_request(self, api_url, api_field):
        url = RiotLOL.api_urls[api_url].format(
            base=self.base_url,
            region=self.region,
            version=RiotLOL.api_versions[api_url],
            field=api_field
        )

        return requests.get(url, params=self.api_key).json()
