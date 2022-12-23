import os

from flask_migrate import Migrate
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

with app.app_context():
    if os.getenv('IMPORT_SAMPLE_DATA') == "1":
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, "sample_data", "sample_data.sql")
        if os.path.exists(path):
            print("Importing sample data...")
            with open(path, "r", encoding="utf-8") as file:
                data = file.readlines()
                for line in data:
                    db.session.execute(line)
                db.session.commit()
