from marshmallow import EXCLUDE
from webargs.flaskparser import FlaskParser


class CustomArgumentParser(FlaskParser):
    DEFAULT_UNKNOWN_BY_LOCATION = {
        "query": EXCLUDE,
        "form": EXCLUDE,
        "json": EXCLUDE,
        "view_args": EXCLUDE,
        "path": EXCLUDE,
    }


class QueryUtils:
    CUSTOM_QUERY = {}

    def queries(self, params):
        data = []
        for kp, value in params.items():
            if not value:
                continue

            query = self.CUSTOM_QUERY.get(kp)
            if not query:
                continue

            if callable(query):
                data.append(query(value))
            else:
                data.append(query == value)

        return data
