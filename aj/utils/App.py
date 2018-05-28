from flask import Flask

from utils.settings import templates_dir, static_dir, SQLALCHEMY_DATABASE_URI
from utils.functions import init_ext
from user.views import user
from house.views import house
from order.views import orders
from ihome.views import ihome_blueprint


def create_app(config):

    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house, url_prefix='/house')
    app.register_blueprint(blueprint=orders, url_prefix='/orders')
    app.register_blueprint(blueprint=ihome_blueprint)
    app.config.from_object(config)
    init_ext(app)

    return app
