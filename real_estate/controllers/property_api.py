from urllib.parse import parse_qs

from odoo import http
from odoo.http import request
import json
from datetime import datetime

class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)

            if 'owner' in vals:
                owner_name = vals.pop('owner')
                owner_rec = request.env['owner'].sudo().search([('name', '=', owner_name)], limit=1)

                if owner_rec:
                    vals['owner'] = owner_rec.id
                else:
                    new_owner = request.env['owner'].sudo().create({'name': owner_name, 'phone': '01064068910'})
                    vals['owner'] = new_owner.id


            if 'date_availability' in vals:
                date_str = vals['date_availability']
                date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
                vals['date_availability'] = date_obj


            if 'line_ids.area' in vals:
                area_value = vals.pop('line_ids.area')

                vals['line_ids'] = [
                    (0, 0, {
                        'area': area_value,
                        'description': 'Created from API'
                    })
                ]

            new_property = request.env['property'].sudo().create(vals)

            return request.make_response(
                json.dumps({
                    'message': 'Property created successfully',
                    'id': new_property.id,
                    'ref': new_property.ref
                }),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=400
            )


    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_rec = request.env["property"].sudo().search([("id", "=", property_id)], limit=1)

            if not property_rec:
                return request.make_response(
                    json.dumps({'error': 'Property not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                    )

            args = request.httprequest.data.decode()
            vals = json.loads(args)

            if 'owner' in vals:
                owner_name = vals.pop('owner')
                owner_rec = request.env['owner'].sudo().search([('name', '=', owner_name)], limit=1)

                if owner_rec:
                    vals['owner'] = owner_rec.id
                else:
                    new_owner = request.env['owner'].sudo().create({'name': owner_name, 'phone': '01064068910'})
                    vals['owner'] = new_owner.id

            if 'date_availability' in vals:
                date_str = vals['date_availability']
                date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
                vals['date_availability'] = date_obj

            if 'line_ids.area' in vals:
                area_value = vals.pop('line_ids.area')
                if property_rec.line_ids:
                    existing_line_id = property_rec.line_ids[0].id
                    vals['line_ids'] = [
                        (1, existing_line_id, {
                            'area': area_value,
                            'description': 'Updated from API'
                        })
                        ]
                else:
                    vals['line_ids'] = [
                        (0, 0, {
                            'area': area_value,
                            'description': 'Created from API (Update)'
                        })
                        ]

            property_rec.write(vals)

            return request.make_response(
                    json.dumps({
                        'message': 'Property updated successfully',
                        'id': property_rec.id,
                        'name': property_rec.name
                    }),
                    headers={'Content-Type': 'application/json'},
                    status=200
                )

        except Exception as e:
                return request.make_response(
                    json.dumps({'error': str(e)}),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_rec = request.env["property"].sudo().search([("id", "=", property_id)], limit=1)

            if not property_rec:
                return request.make_response(
                    json.dumps({'error': 'Property not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )

            property_rec.unlink()

            return request.make_response(
                json.dumps({'message': 'Property deleted successfully'}),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property_rec = request.env["property"].sudo().search([("id", "=", property_id)], limit=1)

            if not property_rec:
                return request.make_response(
                    json.dumps({'error': 'Property not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )

            return request.make_response(
                json.dumps({'message': 'Property read done successfully with data ==>',
                            "id" :property_rec.id,
                            "name": property_rec.name,
                            "owner": property_rec.owner.name,
                            "Num of Bedrooms": len(property_rec.line_ids)
                            }),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

    @http.route("/v1/property", methods=["GET"], type="http", auth="none", csrf=False)
    def get_list_of_properties(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("UTF-8"))
            property_domain=[]
            limit=0
            page = offset = None
            if params:

               if params.get("state"):
                   property_domain += [("state","=",params.get("state")[0])]

               if params.get("owner"):
                   owner_name_list = params.get("owner")

                   owner_rec = request.env["owner"].sudo().search([("name", "=", owner_name_list[0])], limit=1)

                   if owner_rec:
                       property_domain += [
                           ("owner", "=", owner_rec.id)]
                   else:
                       return request.make_response(
                           json.dumps({'error': f'no owner with name {owner_name_list[0]} was found'}),
                           headers={'Content-Type': 'application/json'},
                           status=404
                       )
               if params.get("limit"):
                    limit = int(params.get("limit")[0])

               if params.get("page"):
                   page = int(params.get("page")[0])
                   offset=(limit*page)-limit

            property_records = request.env["property"].sudo().search(property_domain,limit=limit,offset=offset,order='id desc')

            if not property_records:
                return request.make_response(
                    json.dumps({'error': 'Property not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )

            return request.make_response(
                json.dumps([{'message': f'Property {property_rec.name} with id {property_rec.id} It was read successfully with data :',
                            "id" :property_rec.id,
                            "name": property_rec.name,
                            "owner": property_rec.owner.name,
                            "Num of Bedrooms": len(property_rec.line_ids),
                            "page": page if page else 1,
                            "record num in page" : i+1
                            }for i,property_rec in enumerate(property_records)]),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

    @http.route("/v1/property", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_list_of_properties(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("UTF-8"))
            property_domain=[]
            if params:

               if params.get("state"):
                   property_domain += [("state","=",params.get("state")[0])]

               if params.get("owner"):
                   owner_name_list = params.get("owner")

                   owner_rec = request.env["owner"].sudo().search([("name", "=", owner_name_list[0])], limit=1)

                   if owner_rec:
                       property_domain += [
                           ("owner", "=", owner_rec.id)]
                   else:
                       return request.make_response(
                           json.dumps({'error': f'no owner with name {owner_name_list[0]} was found'}),
                           headers={'Content-Type': 'application/json'},
                           status=404
                       )

            property_records = request.env["property"].sudo().search(property_domain)

            if not property_records:
                return request.make_response(
                    json.dumps({'error': 'Property not found'}),
                    headers={'Content-Type': 'application/json'},
                    status=404
                )

            for p in property_records:
                p.state = "draft"

            return request.make_response(
                json.dumps([{'message': f'Property {property_rec.name} with id {property_rec.id} Its status was edited successfully with data :',
                            "id" :property_rec.id,
                            "name": property_rec.name,
                            "owner": property_rec.owner.name,
                            "Num of Bedrooms": len(property_rec.line_ids),
                            "state" : property_rec.state,
                            }for property_rec in property_records]),
                headers={'Content-Type': 'application/json'},
                status=200
            )

        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=400
            )
