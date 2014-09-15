import os.path
import json
import riotlol


def main():
    file_name = 'info.json'
    if os.path.isfile(file_name):
        f = open(file_name, 'r')
        user_data = json.load(f)
        print(user_data['api_key'])
    else:
        f = open(file_name, 'w')
        api_key = input("Enter Riot Games API key: ")
        riot = riotlol.RiotLOL(api_key)
        info = {'api_key': api_key,
                'version': riot.latest_version()
                }
        json.dump(info, f)

    f.close()

if __name__ == '__main__':
    main()
