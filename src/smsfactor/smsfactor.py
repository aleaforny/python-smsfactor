import requests, json
from requests.exceptions import HTTPError, ConnectionError
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

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
        status = error.get('status', -1337)
        if status == -1337:
            raise SMSFactorException(f"Couldn't find status code in the error message")
        if status != 1:
            raise SMSFactorException(f"Error {error.get('status')}: {error.get('message', 'no_message')} ({error.get('details', 'no_details')})")

    @staticmethod
    def validate_data(data):
        """Verifies the data's structure to ensure its properly handled."""
        if not isinstance(data, dict):
            raise SMSFactorException(f"Expected 'data' to be a dictionary, but got {type(data).__name__}.")

    def search_key_and_update_value(self, dictionary, key, fn):
        if key in dictionary:
            dictionary[key] = fn(dictionary[key])
        for v in dictionary.values():
            if isinstance(v, dict):
                self.search_key_and_update_value(v, key, fn)
        return dictionary
    
    def encode_message_data(self, data):
        data = self.search_key_and_update_value(data, "links", lambda links: [self.encode_url(url) for url in links])
        return data

    @staticmethod
    def encode_url(url):
        """Method to handle URL encoding/validation."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        encoded_query = urlencode(query_params, doseq=True)
        encoded_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            encoded_query,
            parsed_url.fragment
        ))

        return encoded_url

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
            self.validate_data(data)
            data = self.encode_message_data(data)

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
