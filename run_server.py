import os

# Import the main Flask app
from app import app

# Get Blueprint Apps
from notes import notes_app
from auth import auth_flask_login
from rooms import rooms

# Register Blueprints
app.register_blueprint(notes_app)
app.register_blueprint(auth_flask_login)
app.register_blueprint(rooms)

# start the server
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)