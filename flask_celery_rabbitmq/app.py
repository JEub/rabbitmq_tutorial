from flask import Flask

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: {} %(levelname)s %(message)s'.
           format(os.getpid())
    )
logger = logging.getLogger()


def create_app():
    logger.info(f"Starting app in {config.APP_ENV} environment.")
    app = Flask(__name__)
    app.config.from_object('config')
    api.init_app(app)

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
