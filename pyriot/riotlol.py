import requests


class RiotLOL():

    api_versions = {
        'champion': 1.2,
        'game': 1.3,
        'league': 2.5,
        'static-data': 1.2,
        'match': 2.2,
        'matchhistory': 2.2,
        'stats': 1.3,
        'summoner': 1.4,
        'team': 2.4
    }

    def __init__(self, api_key, region='na'):
        self.region = region
        self.api_key = api_key
        self.base_url = 'https://{region}.api.pvp.net/api/lol'.format(
            region=self.region
        )
        self.url = '{base}/{category}/{region}/v{version}/{field}'

    def champion_list(self, champ_data=None):
        """Retrieves champion list.

        Keyword arguments:
        champ_data -- tags for additional data (default None)
        """
        return self.make_request(
            'static-data',
            'champion',
            champData=champ_data
        )['data']

    def champion(self, id, champ_data=None):
        """Retrieves a champion by its id.

        Keyword arguments:
        champ_data -- tags for additional data (default None)
        """
        return self.make_request(
            'static-data',
            'champion/{}'.format(id),
            champData=champ_data
        )

    def version(self):
        """Retrieves version data."""
        return self.make_request('static-data', 'versions')

    def latest_version(self):
        """Retrieves most recent version."""
        return self.version()[0]

    def make_request(self, api_url, api_field, **kwargs):
        args = {'api_key': self.api_key}

        for kw in kwargs:
            if kwargs[kw] is not None:
                args[kw] = kwargs[kw]

        url = self.url.format(
            base=self.base_url,
            category=api_url,
            region=self.region,
            version=RiotLOL.api_versions[api_url],
            field=api_field
        )

        r = requests.get(url, params=args)
        r.raise_for_status()

        return r.json()
