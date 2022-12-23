import os

from flask_migrate import Migrate
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.cli.command()
def import_sample_data():
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, "sample_data", "sample_data.sql")
        if os.path.exists(path):
            print("Importing sample data...")
            with open(path, "r", encoding="utf-8") as file:
                data = file.read()
                for line in data.split(";"):
                    db.session.execute(line)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
