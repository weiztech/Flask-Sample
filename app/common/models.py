class ModelUtils:

    def set_from_dict(self, dict_data):
        for field, value in dict_data.items():
            setattr(self, field, value)
