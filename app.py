from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blueprints import groups_blueprint
from gevent.wsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_with_reloader

db = SQLAlchemy()


@run_with_reloader
def run():
    app = Flask(__name__)
    db.init_app(app)
    environ['api_CONFIG'] = 'DEV'
    app.config.from_object('config.settings')
    app.template_folder = app.config.get('TEMPLATE_FOLDER', 'templates')
    app.register_blueprint(groups_blueprint)
    app.debug = app.config['DEBUG']
    print('Starting server at %s listening on port %s %s' % (
        app.config['HOST'],
        app.config['PORT'],
        'in DEBUG mode' if app.config['DEBUG'] else ''
    ))
    http_server = WSGIServer((app.config['HOST'], app.config['PORT']), DebuggedApplication(app))
    http_server.serve_forever()
