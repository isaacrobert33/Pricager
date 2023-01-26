from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from utils import search, get_all_products

app = Flask(__name__)
api = Api(app)
cors = CORS()

class Search(Resource):
    def get(self):
        query = request.args.get("q")
        re = search(query)
        return re

class AllProducts(Resource):
    def get(self):
        limit = request.args.get("limit")
        page = request.args.get("page")
        re = get_all_products(limit, page)
        return re

api.add_resource(Search, "/search")
api.add_resource(AllProducts, "/dynamics")

app.run(debug=True)