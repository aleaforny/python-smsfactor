import requests, json
from requests.exceptions import HTTPError, ConnectionError


class SMSFactorException(Exception):
    pass


class SMSFactorAPI:
    """ SMS Factor API Object Definition """

    def __init__(self, token):
        """ Object constructor """
        self.token = token
        self.url = "https://api.smsfactor.com"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def __repr__(self):
        """ Object representation (for developers) """
        return f"SMSFactorAPI(token={self.token})"

    def __str__(self):
        """ String representation """
        return f"SMSFactorAPI Object"

    @staticmethod
    def raise_for_smsfactor_exception(error):
        if error['status'] != 1:
            raise SMSFactorException(f"Error {error['status']}: {error['message']} ({error['details']})")

    def get(self, endpoint, data=None, get_response=False):
        """ Attempt a GET action. Returns None if request wasn't successful or raise Exception if attempted to GET when API is not connected """
        try:
            response = requests.get(self.url + endpoint, params=json.dumps(data), headers=self.headers)
            response.raise_for_status()
            self.raise_for_smsfactor_exception(response.json())
            return response if get_response else response.json()
        except HTTPError as error:
            print(error)
        except ConnectionError as error:
            print(error)

    def delete(self, endpoint, get_response=False):
        """ Attempt a DELETE action. Returns None if request wasn't successful or raise Exception if attempted to GET when API is not connected """
        try:
            response = requests.delete(self.url + endpoint, headers=self.headers)
            response.raise_for_status()
            self.raise_for_smsfactor_exception(response.json())
            return response if get_response else response.json()
        except HTTPError as error:
            print(error)
        except ConnectionError as error:
            print(error)

    def post(self, endpoint, data, get_response=False):
        """ Attempt a POST action. Returns None if request wasn't successful or raise Exception if attempted to GET when API is not connected """
        try:
            response = requests.post(self.url + endpoint, data=json.dumps(data), headers=self.headers)
            response.raise_for_status()
            self.raise_for_smsfactor_exception(response.json())
            return response if get_response else response.json()
        except HTTPError as error:
            print(error)
        except ConnectionError as error:
            print(error)

    @property
    def credits(self):
        response = self.get("/credits")
        if response:
            return int(response['credits'])

    # TODO: Need to implement other methods (PUT, etc.)
