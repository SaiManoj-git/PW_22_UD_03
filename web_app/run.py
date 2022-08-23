from app.factory import create_app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['IMGRES_DB_URI'] = config['PROD']['IMGRES_DB_URI']
    app.config['IMGRES_NS'] = config['PROD']['IMGRES_NS']
    app.config['SECRET_KEY'] = config['PROD']['SECRET_KEY']         # for session to be writeable

    app.run()
