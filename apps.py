from flask import Flask

from config import Config as config
from exts import db, csrf
from lock.api.views import bp as api_bp
from lock.cms.views import bp as front_bp
from lock.common.views import bp as common_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(api_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)

    db.init_app(app)
    csrf.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
