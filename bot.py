import configparser
import pathlib
import uuid
from random import choice, randrange

from src.app import app
from src.utils.daos import like_dao, post_dao, user_dao

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


def generate_users(number_of_users):
    for _ in range(number_of_users):
        user_data = generate_user_data()
        user_dao.create_user(user_data)


def generate_posts(users, number_of_posts):
    for user in users:
        for _ in range(randrange(1, number_of_posts + 1)):
            post_data = generate_post_data()
            post_dao.create_post(post_data, user.id)


def generate_likes(users, posts, number_of_likes):
    for user in users:
        for _ in range(randrange(1, number_of_likes + 1)):
            post = choice(posts)
            like_dao.like({'post_id': post.id}, user.id)


def random_activity():
    config = get_config(CONFIG_FILE)
    num_users = config['USER']['number_of_users']
    num_posts = config['POST']['max_posts_per_user']
    num_likes = config['LIKE']['max_likes_per_user']

    with app.app_context():
        generate_users(int(num_users))
        users = user_dao.get_all()
        generate_posts(users, int(num_posts))
        posts = post_dao.get_all()
        generate_likes(users, posts, int(num_likes))


def run_bot():
    return random_activity()


if __name__ == '__main__':
    run_bot()
