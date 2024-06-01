import json
import os
from flask import Flask, jsonify

class MappingAPI:
    """
    A Flask-based API for serving a JSON mapping between centers and departments.

    This API provides a single endpoint (`/mapping`) that returns the contents of a
    JSON file containing the mapping data. It is designed for easy deployment and
    configuration.

    Attributes:
        app (Flask): The Flask application instance.
        mapping_file_path (str): The path to the JSON file containing the mapping data.

    Methods:
        __init__(self, mapping_file_path=None): Initializes the MappingAPI object.
        get_mapping(self): Retrieves and returns the mapping data as a JSON response.
        run(self, host='0.0.0.0', port=5001): Starts the Flask development server.
    """

    def __init__(self, mapping_file_path=None):
        """
        Initializes the MappingAPI object.

        Args:
            mapping_file_path (str, optional): The path to the JSON file.
                Defaults to 'center_dept_database/mapping.json'.
        """
        self.app = Flask(__name__)
        self.app.add_url_rule('/mapping', 'mapping', self.get_mapping, methods=['GET'])

        if mapping_file_path is None:
            mapping_file_path = os.path.join('center_dept_database', 'mapping.json')
        self.mapping_file_path = mapping_file_path

    def get_mapping(self):
        """
        Retrieves the mapping data from the JSON file and returns it as a JSON response.
        """
        with open(self.mapping_file_path, 'r') as file:
            mapping_data = json.load(file)
        return jsonify(mapping_data)

    def run(self, host='0.0.0.0', port=5001):
        """
        Starts the Flask development server.

        Args:
            host (str, optional): The hostname to listen on. Defaults to '0.0.0.0' (all interfaces).
            port (int, optional): The port of the webserver. Defaults to 5001.
        """
        print(f"Starting MappingAPI on {host}:{port}")
        self.app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    mapping_api = MappingAPI()
    mapping_api.run()
