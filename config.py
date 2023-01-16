from flask import Flask

app = Flask(__name__)


class Config():
    user = 'netology_flask'
    password = 'flask'
    database = 'netology_flask'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        f"postgresql://{user}:{password}@localhost:5432/{database}"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    app.config["SECRET_KEY"] = "xhosd6f982yfhowefy29f"


app.config.from_object(Config)
