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
        url = RiotLOL.api_urls['lol-static-data'].format(
            base=self.base_url,
            region=self.region,
            version=RiotLOL.api_versions['lol-static-data'],
            field='versions'
        )
        r = requests.get(url, params=self.api_key).json()

        return r[0]
