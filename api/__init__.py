from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict


# this is import of db instant, then models for Order and User class.
from .utils import db
from .models.orders import Order
from .models.users import User
# this is for migrate all models to sqllite db.
from flask_migrate import Migrate
# JWT authorisation .
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed


# this method will create the instance of the app.
def create_app(config = config_dict['dev']):
    app = Flask(__name__)
    # 
    app.config.from_object(config)
    # configuring database with flask app.
    db.init_app(app)
    # migrate the db model to database.
    migrate = Migrate(app,db)   

    # create JWT authorisation token.
    jwt = JWTManager(app)
    
    # authorization variable holding value of authorization header for jwt access token
    authorizations ={
        "Bearer Auth":{
            'type':"apiKey",
            'in': "header",
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize, create the login request it will generate access token put it  here in value OR First sign in and then login"
        }
    }

    # Api is the class here.
    api = Api(app,
        title="Pizza Delivery API",
        description= "A REST API for a Pizza Delivery Service",
        authorizations= authorizations,
        security="Bearer Auth"
    )


    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace,path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error":"Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"},405

    # make flask shell context.
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Order':Order
        }
    return app
