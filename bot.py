import configparser
import pathlib
import uuid
from random import choice, randrange

import requests

CONFIG_FILE = 'bot_config.ini'


def get_config(config_filename):
    cwd = pathlib.Path(__file__).parent.absolute()
    conf_path = cwd.joinpath(config_filename)

    config = configparser.ConfigParser()
    config.read(conf_path)

    return config


def generate_user_data():
    random_data = {
        'name': uuid.uuid4().hex[:30],
        'email': f'{uuid.uuid4().hex}@email.com',
        'password': uuid.uuid4().hex,
    }

    return random_data


def generate_post_data():
    random_data = {
        'title': uuid.uuid4().hex,
    }

    return random_data


def base_url(host=None):
    if host:
        url = f'http://{host}:5000/api'
    else:
        url = 'http://localhost:5000/api'
    return url


def user_login(params):
    url = base_url()
    response = requests.post(f'{url}/login', json=params)
    token = response.json().get('access_token')

    return f'Bearer {token}'


def generate_users(number_of_users):
    url = base_url()
    auth_list = []
    for _ in range(number_of_users):
        user_data = generate_user_data()
        requests.post(f'{url}/signup', json=user_data)
        user_auth_params = {x: user_data[x] for x in ['email', 'password']}
        auth_list.append(user_auth_params)

    return auth_list


def generate_posts(users_data, number_of_posts):
    url = base_url()
    post_list = []
    for user_data in users_data:
        token = user_login(user_data)
        headers = {"Authorization": token}
        for _ in range(randrange(1, number_of_posts + 1)):
            post_data = generate_post_data()
            response = requests.post(f'{url}/post', json=post_data, headers=headers)
            post_list.append(response.json().get('post_id'))

    return post_list


def generate_likes(users_data, posts_data, number_of_likes):
    url = base_url()
    for user_data in users_data:
        token = user_login(user_data)
        headers = {"Authorization": token}
        for _ in range(randrange(1, number_of_likes + 1)):
            like_data = {'post_id': choice(posts_data)}
            requests.post(f'{url}/like', json=like_data, headers=headers)


def random_activity():
    config = get_config(CONFIG_FILE)
    num_users = config['USER']['number_of_users']
    num_posts = config['POST']['max_posts_per_user']
    num_likes = config['LIKE']['max_likes_per_user']

    users_data = generate_users(int(num_users))
    posts_data = generate_posts(users_data, int(num_posts))
    generate_likes(users_data, posts_data, int(num_likes))


def run_bot():
    return random_activity()


if __name__ == '__main__':
    run_bot()
