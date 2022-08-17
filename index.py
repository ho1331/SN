from src.app import app
from src.models.likes import *
from src.models.posts import *
from src.models.users import *
from src.views import api   


api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
