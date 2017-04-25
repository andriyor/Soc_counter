from app import app

from views import main
from auth import auth

app.register_blueprint(main)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(port=3030, debug=True)
