class LDPLoginError(Exception):
    """
    """

    _errors = {
        'invalid_request': "The request provider parameter must contains an url or an email",
        'cannot_get_provider_info': "Cannot get provider informations",
        'cannot_register': "Unable to register, is the provider accepting registration ? If not contact <todo : give an email> to make a manual registration"
    }

    def __init__(self, error):
        self.error = error
        self.description = self._errors.get(error)

    def create_dict(self):
        dic = {
            'error': self.error,
            'error_description': self.description,
        }

        return dic
