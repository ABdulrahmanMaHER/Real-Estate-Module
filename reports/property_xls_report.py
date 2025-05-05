import io
import xlsxwriter
from odoo import http
from odoo.http import request, route


class PropertyExcelReport(http.Controller):

    @route("/property/excel/report", type="http", auth="user")
    def download_property_excel_report(self, ids=None):
        if not ids:
            return request.not_found()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Properties")

        # Formatting
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        data_format = workbook.add_format({'border': 1})

        # Headers
        headers = ['Ref', 'Name', 'Bedrooms', 'Garden', 'Owner']
        worksheet.write_row(0, 0, headers, header_format)

        # Convert `ids` from query string to a list of integers
        property_ids = [int(i) for i in ids.split(",")] if ids else []

        # Fetch only selected properties
        properties = request.env["property"].sudo().browse(property_ids)

        row = 1
        for property in properties:
            worksheet.write(row, 0, property.ref or "", data_format)
            worksheet.write(row, 1, property.name or "", data_format)
            worksheet.write(row, 2, property.bedrooms or 0, data_format)
            worksheet.write(row, 3, "Yes" if property.garden else "No", data_format)
            worksheet.write(row, 4, property.owner.name if property.owner else "", data_format)
            row += 1

        workbook.close()
        output.seek(0)

        file_name = "Selected_Properties_Report.xlsx"

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )
