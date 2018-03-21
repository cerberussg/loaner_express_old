from flask_restful import Resource, reqparse
from src.models.site import SiteModel
from flask_jwt import jwt_required, current_identity

class SiteList(Resource):
     # pulls in request to parse
    parser = reqparse.RequestParser()
    # Set requirements for parser
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be empty"
    )
    parser.add_argument('loaners_on_site',
        type=str,
        required=False,
        help="Loaners on site can be filled in when adding equipment."
    )
    parser.add_argument('loaners_issued',
        type=str,
        required=False,
        help="This will be needed when issuing equipment"
    )
    @jwt_required()
    # returns a list of all sites
    def get(self):
        identity = current_identity
        if identity.super_user == 1:
            return {'sites': [site.json() for site in SiteModel.query.all()]}, 200
        else:
            return {'message': 'You are not authorized to view page'}, 401
    
    @jwt_required()
    # creates new sites
    def post(self):
        identity = current_identity
        if identity.super_user != 1:
            return {'message': 'You are not authorized.'}, 401

        # loads json data and parses looking for args
        data = SiteList.parser.parse_args()

        # looks for existing site 
        site = SiteModel.site_by_name(data['name'].lower())

        if site is None:
            site = SiteModel(data['name'].lower(), 0, 0, identity.username)
        else:
            return {'message': 'Site name in use already'}, 400
        
        site.save_to_db()

        return site.json()

class Site(Resource):
    pass
