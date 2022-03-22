from app import app, db
import view


if __name__ == "__main__":
    app.run()


@app.before_first_request
def create_tables():
    db.create_all()
