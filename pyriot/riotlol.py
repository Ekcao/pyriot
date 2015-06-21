import requests
import os.path
import json


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
        """
        Args:
            api_key (str): The user's Riot Games API key.
            region (str, optional): Region for which data will be pulled.
                Defaults to 'na', for 'North America'.
        """
        self.region = region
        self.api_key = api_key
        self.base_url = 'https://{region}.api.pvp.net/api/lol'.format(
            region=self.region)
        self.url = '{base}/{category}/{region}/v{version}/{field}'

    def champion_list(self, champ_data=None):
        """Retrieves static data for all champions.

        Args:
            champ_data (str, optional): What fields to request, such as spells,
                skins, etc. Defaults to None, the basic champion fields.

        Returns:
            dict: JSON representation of the champions and each field.
        """

        return self.make_request('static-data', 'champion',
                                 champData=champ_data)

    def champion_list_from_file(self, champ_data=None):
        """Retrieves champion list from a file.

        Keyword arguments:
        champ_data -- tags for additional data (default None)
        """

        file_name = 'champs.json'
        current_patch = self.latest_version()

        if os.path.isfile(file_name):
            # Require fewer API calls by checking for an existing file
            with open(file_name, 'r+') as f:
                champs = json.load(f)
                if champs['version'] != str(current_patch):
                    # For new patches, update the file.
                    f.seek(0)
                    champs = self.save_champs(f)
        else:
            # Data is most recent, load from file
            with open(file_name, 'w') as f:
                champs = self.save_champs(f)

        return champs

    def champion(self, id, champ_data=None):
        """
        Retrieves a champion by its id.

        Keyword arguments:
        champ_data -- tags for additional data (default None)
        """
        return self.make_request('static-data', 'champion/{}'.format(id),
                                 champData=champ_data)

    def version(self):
        """Retrieves version/patch data."""
        return self.make_request('static-data', 'versions')

    def latest_version(self):
        """Retrieves most recent version/patch."""
        return self.version()[0]

    def make_request(self, api_url, api_field, **kwargs):
        args = {'api_key': self.api_key}

        for kw in kwargs:
            if kwargs[kw] is not None:
                args[kw] = kwargs[kw]
        url = self.url.format(base=self.base_url,
                              category=api_url,
                              region=self.region,
                              version=RiotLOL.api_versions[api_url],
                              field=api_field)

        r = requests.get(url, params=args)
        r.raise_for_status()

        return r.json()

    def save_champs(self, file):
        champs = self.champion_list(champ_data='all')
        json.dump(champs, file,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))

        return champs
