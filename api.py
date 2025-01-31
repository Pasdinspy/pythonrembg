from app import app
from flasgger import Swagger
from src.controller.api_ia import *

swagger = Swagger(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
