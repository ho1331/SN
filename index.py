from src.app import app
# from flask_restx import Api
from src.models.likes import *
from src.models.posts import *
from src.models.users import *


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
