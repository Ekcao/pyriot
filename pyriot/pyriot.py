import os.path
import json
import riotlol

#Testing
def main():
    file_name = 'info.json'

    if os.path.isfile(file_name):
        f = open(file_name, 'r')
        info = json.load(f)
    else:
        f = open(file_name, 'w')
        api_key = input("Enter Riot Games API key: ")

        info = {'api_key': api_key}
        json.dump(info, f, indent=4)

    riot = riotlol.RiotLOL(info['api_key'])
    f.close()

if __name__ == '__main__':
    main()
