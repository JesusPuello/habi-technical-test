from flask import Flask
from flask_restful import Api
from controllers import property_controllers

app = Flask(__name__)
api = Api(app)

api.add_resource(property_controllers.PropertyController, "/house")

if __name__ == "__main__":
    app.run()  # run our Flask app
