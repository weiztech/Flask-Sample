from ast import literal_eval
from marshmallow import ValidationError


def convert_raw_list(field_name, list_data) -> tuple[dict]:
    list_data = list_data or ()
    try:
        new_data = []
        for data in list_data:
            if isinstance(data, (dict, list, tuple)):
                new_data.append(data)
            else:
                new_data.append(literal_eval(data))
        return new_data

    except SyntaxError:
        raise ValidationError({field_name: "Data is invalid"})
