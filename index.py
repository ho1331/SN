from src.app import app
from src.views import api

api.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
