import json
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request

def invalid_response(error, status):
    response_body = {
        'error': error
    }
    return request.make_json_response(response_body, status=status)

def valid_response(data, status):
    response_body = {
        'data': data
    }
    return request.make_json_response(response_body, status=status)

class PropertyApi(http.Controller):
    @http.route("/api/property",methods=["POST"],type="http",auth="public",csrf=False)
    def post_property(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                "message": "field name does not passed !",
            }, status=400)
        try:
            property_record = request.env['property'].sudo().create(vals)
            if property_record:
                return request.make_json_response({
                    "message": "property has been added sucessfully",
                    "id":property_record.id,
                    "name":property_record.name
                },status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)


    @http.route("/api/property/json", methods=["POST"], type="json", auth="public", csrf=False)
    def post_property_json(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        property_record = request.env['property'].sudo().create(vals)
        if property_record:
            return{
            "message":"property has been added sucessfully"
        }

    @http.route("/api/property/<int:property_id>", methods=["PUT"], type="http", auth="public", csrf=False)
    def property_update(self, property_id):
        try:
            # Check if the property exists
            property_record = request.env['property'].sudo().search([('id', '=', property_id)], limit=1)

            if not property_record:
                return request.make_json_response({
                    "message": "Please enter a valid property ID!"
                }, status=400)

            # Read the request data
            args = request.httprequest.data.decode()
            vals = json.loads(args)

            # Validate input data
            allowed_fields = request.env['property']._fields.keys()
            invalid_fields = [key for key in vals.keys() if key not in allowed_fields]

            if invalid_fields:
                return request.make_json_response({
                    "message": "Invalid fields found!",
                    "invalid_fields": invalid_fields
                }, status=400)

            # Update the property
            property_record.write(vals)

            return valid_response({
                "message": "Property has been updated successfully",
                "id": property_record.id,
                "name": property_record.name
            }, status=200)

        except Exception as e:
            return invalid_response({
                "message": "An error occurred while updating the property."
            }, status=500)

    @http.route("/api/property", methods=["GET"], type="http", auth="public", csrf=False)
    def get_property(self):
        try:
            # Default values
            limit = 3
            page = 1  # Default page is 1
            offset = 0
            property_domain = []

            # Get query parameters
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))

            # Handle 'limit' parameter
            if params.get('limit'):
                try:
                    limit = int(params['limit'][0])  # Extract first value and convert to integer
                except ValueError:
                    return invalid_response({
                        "message": "Invalid limit value. Must be an integer."
                    }, status=400)

            # Handle 'page' parameter
            if params.get('page'):
                try:
                    page = int(params['page'][0])  # Extract first value and convert to integer
                except ValueError:
                    return invalid_response({
                        "message": "Invalid page value. Must be an integer."
                    }, status=400)

            # Calculate offset
            offset = (page - 1) * limit  # Adjusting for zero-based indexing

            # Handle 'state' parameter
            if 'state' in params:
                states = params.get('state', [])  # This returns a list
                property_domain.append(('state', 'in', states))  # Use 'in' for multiple values

            # Fetch filtered records
            property_records = request.env['property'].sudo().search(
                property_domain, offset=offset, limit=limit, order='id desc'
            )

            # Check if there are properties
            if not property_records:
                return invalid_response({
                    "message": "There are no properties!"
                }, status=400)

            # Convert recordset to a list of dictionaries
            property_list = [{
                'id': record.id,
                'ref': record.ref,
                'name': record.name,
                'description': record.description,
                'state': record.state
            } for record in property_records]

            return valid_response({
                "properties": property_list,
                "page": page,
                "limit": limit,
                "total": request.env['property'].sudo().search_count(property_domain)
            }, status=200)

        except Exception as error:
            return invalid_response({
                "message": "An error occurred while retrieving properties.",
                "error": error
            }, status=500)


