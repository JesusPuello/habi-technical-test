from flask_restful import Resource, reqparse
from services import property_services
from utils import property_filters, status_mapper


class PropertyController(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        for possible_arg in property_filters.EXPECTED_ARGS:
            parser.add_argument(
                possible_arg,
                required=False,
                store_missing=False,
                type=property_filters.EXPECTED_ARGS[possible_arg],
            )
        args = parser.parse_args()
        if "status" in args:
            args["status_id"] = status_mapper.STATUS_TO_NUMBER_MAPPER.get(
                args["status"], 0
            )
            args.pop("status")
        data = property_services.find_available_houses(args)
        return {"available_houses": data}, 200
