import os

from flask_migrate import Migrate
from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.cli.command("import-sample")
def import_sample_data():
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, "sample_data", "sample_data.sql")
    if os.path.exists(path):
        print("Importing sample data...")
        with open(path, "r", encoding="utf-8") as file:
            data = file.read().split(";")
            count = len(data)
            ten_percent = int(count/10)
            for i in range(0, count):
                db.session.execute(data[i])
                if i % ten_percent == 0:
                    print(f"Importing sample data {round(100 * i/count, 0)}")
            db.session.commit()
