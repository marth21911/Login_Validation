from flask_app import app
#drawing info from users_controller
from flask_app.controllers import user_controller



if __name__ == "__main__":
    app.run(debug=True)