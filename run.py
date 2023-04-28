from index import app, db


if __name__ == '__main__':
    db.create_all()
    app.run(host="localhost", port=5003, debug=True)