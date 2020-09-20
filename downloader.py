import os
import requests

def _(*args):
    print('[Tool] ', end='')
    for arg in args:
        print(arg, end=' ')
    print()


class Downloader():
    def __init__(self, fingerprint, assets_url: str):
        self.fingerprint = fingerprint
        self.assets_url = assets_url

    def download(self):
        self.hash = self.fingerprint['sha']

        if not os.path.isdir(self.hash):
            os.mkdir(self.hash)

        for i in self.fingerprint['files']:
            path, name = os.path.split(i['file'])
            request = requests.get(f'{self.assets_url}/{self.fingerprint["sha"]}/{path}/{name}')

            if request.status_code == 200:
                _(f"Downloading {path}/{name}...")
                filedata = request.content

                if not os.path.isdir(path):
                    if not os.path.exists(f'{self.hash}/{path}'):
                        os.makedirs(f'{self.hash}/{path}')

                out = open(os.path.join(f'{self.hash}/{path}/{name}'), 'wb')
                out.write(filedata)
                out.close()
