# -*- coding: utf-8 -*-
"""
Mattermost API driver
"""

# Standard import
from __future__ import unicode_literals
import json
import re
# Libraries
import requests


class MatAPI(object):
    """
    A connector for Mattermost API
    """

    def __init__(self, url, login, password, version=4):
        """
        Initializer
        :param url: URL of Mattermost instance
        :param login: Login (usually mail) for the user
        :param password: Password
        :param version: API version number
        :raises InstanciateException
        """
        # Base URL
        if url.endswith('/'):
            self.url = url[:-1]
        else:
            self.url = url

        # Check if version is an integer.
        # Try to extract the number if it is a string
        if not isinstance(version, int):
            # Accept a version as number string or format like "v3"
            match = re.search("^v?([0-9]{1})$", version)
            if match is not None:
                self.version = int(match.group(1))
            else:
                raise InstanciateException("Invalid API version number")
        else:
            self.version = version

        # Generate base path depending on version
        if self.version == 4:
            self.base_path = "/api/v4"
        elif self.version == 3:
            self.base_path = "/api/v3"
        else:
            raise InstanciateException("Invalid API version number")

        # Credentials
        self.login = login
        self.password = password

        # Set a default timeout
        self.timeout = 20

        try:
            self.__log()
        except (APIError, RequestError) as error:
            raise InstanciateException(unicode(error))

    def __repr__(self):
        """
        Repr function
        """
        return (
            "Mattermost API:\nurl({})\nlogin({})\n"
            "password({})\nversion({})".format(
                self.url, self.login, self.password, self.version
                )
            )

    def __log(self):
        """
        Log to Mattermost API
        :raises APIError, RequestError
        """
        # Credential to POST
        data = {"login_id": self.login, "password": self.password}

        try:
            # Send request
            res = requests.post(
                self.url + self.base_path + "/users/login",
                data=json.dumps(data).encode('utf-8'),
                timeout=self.timeout
                )
        except requests.exceptions.RequestException as error:
            raise RequestError(unicode(error))

        # If error
        if res.status_code != 200:
            # Get error
            try:
                error = json.loads(res.text)
            except ValueError:
                raise RequestError('API return a non-JSON response')
            else:
                raise APIError(error['message'])

        # Authentication token if on response headers
        self.token = res.headers['token']

    def get(self, path):
        """
        GET request
        :param path: Path for the GET request
        :returns: dict return by API
        :raises APIError, RequestError
        """
        # Authentication HEADER
        headers = {"Authorization": "Bearer " + self.token}

        # Format path
        if not path.startswith("/"):
            path = "/" + path

        try:
            # Send request
            res = requests.get(
                self.url + self.base_path + path,
                headers=headers,
                timeout=self.timeout
                )
        except requests.exceptions.RequestException as error:
            raise RequestError(unicode(error))

        # Get content
        try:
            response = json.loads(res.text)
        except ValueError:
            raise RequestError('API return a non-JSON response')

        # If error
        if res.status_code != 200:
            raise APIError(response['message'])

        # Return error (JSON format)
        return response

    def post(self, path, data):
        """
        POST request
        :param path: Path for the POST request
        :param data: dict for data to send
        :returns: dict return by API
        :raises APIError, RequestError
        """
        # Authentication HEADER
        headers = {"Authorization": "Bearer " + self.token}

        # Format path
        if not path.startswith("/"):
            path = "/" + path

        # Check data and serialized it
        if isinstance(data, list) or isinstance(data, dict):
            serialized = json.dumps(data).encode('utf-8')
        else:
            raise BaseMatAPIException(
                'Wrong data format (should be list or dict)'
            )

        try:
            # Send request
            res = requests.post(
                self.url + self.base_path + path,
                data=serialized,
                headers=headers,
                timeout=self.timeout
                )
        except requests.exceptions.RequestException as error:
            raise RequestError(unicode(error))

        # Get content
        try:
            response = json.loads(res.text)
        except ValueError:
            raise RequestError('API return a non-JSON response')

        # If error
        if res.status_code != 200:
            raise APIError(response['message'])

        # Return error (JSON format)
        return response

    def put(self, path, data):
        """
        PUT request
        :param path: Path for the PUT request
        :param data: dict for data to send
        :returns: dict return by API
        :raises APIError, RequestError
        """
        # Authentication HEADER
        headers = {"Authorization": "Bearer " + self.token}

        # Format path
        if not path.startswith("/"):
            path = "/" + path

        # Check data and serialized it
        if isinstance(data, list) or isinstance(data, dict):
            serialized = json.dumps(data).encode('utf-8')
        else:
            raise BaseMatAPIException(
                'Wrong data format (should be list or dict)'
            )

        try:
            # Send request
            res = requests.put(
                self.url + self.base_path + path,
                data=serialized,
                headers=headers,
                timeout=self.timeout
                )
        except requests.exceptions.RequestException as error:
            raise RequestError(unicode(error))

        # Get content
        try:
            response = json.loads(res.text)
        except ValueError:
            raise RequestError('API return a non-JSON response')

        # If error
        if res.status_code != 200:
            raise APIError(response['message'])

        # Return error (JSON format)
        return response

    def delete(self, path):
        """
        DELETE request
        :param path: Path for the DELETE request
        :returns: dict return by API
        :raises APIError, RequestError
        """
        # Authentication HEADER
        headers = {"Authorization": "Bearer " + self.token}

        # Format path
        if not path.startswith("/"):
            path = "/" + path

        try:
            # Send request
            res = requests.delete(
                self.url + self.base_path + path,
                headers=headers,
                timeout=self.timeout
                )
        except requests.exceptions.RequestException as error:
            raise RequestError(unicode(error))

        # Get content
        try:
            response = json.loads(res.text)
        except ValueError:
            raise RequestError('API return a non-JSON response')

        # If error
        if res.status_code != 200:
            raise APIError(response['message'])

        # Return error (JSON format)
        return response


class BaseMatAPIException(Exception):
    """
    Base Mattermost API module exception
    """

    def __init__(self, message):
        """
        :param message: Error message
        """
        super(BaseMatAPIException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class APIError(BaseMatAPIException):
    """
    API return an error
    """

    def __init__(self, message):
        """
        :param message: Error message
        """
        super(APIError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class RequestError(BaseMatAPIException):
    """
    Error with HTTP request
    """

    def __init__(self, message):
        """
        :param message: Error message
        """
        super(RequestError, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class InstanciateException(BaseMatAPIException):
    """
    Exception raise when it is impossible to instanciate the API driver
    """

    def __init__(self, message):
        """
        :param message: Error message
        """
        super(InstanciateException, self).__init__(message)
        self.message = message

    def __str__(self):
        res = 'Error while creating API object !\n'
        res += self.message
        return res
