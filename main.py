import vkauth.vkauth as vkauth
import config
import urllib.parse
import urllib.request
import json
import getpass


def call_api(method, params):
    """Call VK.Api method"""
    url = "https://api.vk.com/method/%s?%s" % (
        method, urllib.parse.urlencode(params))
    return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))['response']


def get_songs(secret_id, user_id, count=0):
    params = [('access_token', secret_id),
              ('uid', user_id)]
    if count is not 0:
        params.append(('count', count))

    response = call_api('audio.get', params)

    songs_ids = []
    for item in response:
        songs_ids.append(item['aid'])

    return songs_ids


def add_song(secret_id, song_id, owner_id):
    params = [('access_token', secret_id),
              ('aid', song_id),
              ('oid', owner_id)]

    response = call_api('audio.add', params)
    return response


def main():
    api_id = config.authorization_data['api_id']
    api_secret = config.authorization_data['api_secret']
    email = config.authorization_data['email']
    password = config.authorization_data['password']
    source_id = config.authorization_data['source_id']

    if password == '':
        password = getpass.getpass()

    secret_id, destination_id = vkauth.auth(email, password, api_id, "audio")

    for song_id in reversed(get_songs(secret_id, source_id, 2)):
        add_song(secret_id, song_id, source_id)

if __name__ == '__main__':
    main()