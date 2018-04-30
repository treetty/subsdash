from flask import Flask

from subsdash import views


DEFAULT_APP_NAME = 'subsdash'

DEFAULT_MODULES = (
    (views.frontend, ""),
)


def create_app(config=None, modules=None):

    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(DEFAULT_APP_NAME)

    # config
    app.config.from_pyfile(config)

    # register module
    configure_modules(app, modules)

    return app


def configure_modules(app, modules):

    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)
