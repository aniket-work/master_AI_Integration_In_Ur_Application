import json
import os
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupplyChainDataRetriever:
    """
    A class to retrieve supply chain data from JSON files based on user queries.

    Attributes:
        database_folder (str): The path to the directory containing the JSON files.
        query_mapping (dict): A dictionary mapping query keywords to JSON file names.

    Methods:
        get_supply_chain_data(query): Retrieves supply chain data based on the user's query.
    """

    def __init__(self, database_folder, mapping_api_url='http://localhost:5001/mapping'):
        """
        Initializes the SupplyChainDataRetriever instance.

        Args:
            database_folder (str): The path to the directory containing the JSON files.
        """
        self.database_folder = database_folder
        self.query_mapping = self.fetch_query_mapping(mapping_api_url)

    def fetch_query_mapping(self, mapping_api_url):
        try:
            response = requests.get(mapping_api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching query_mapping: {e}")
            return {}
        logger.info(f"SupplyChainDataRetriever instance created with database folder: {database_folder}")

    def get_supply_chain_data(self, query):
        """
        Retrieves supply chain data based on the user's query.

        Args:
            query (str): The user's query related to a supply chain activity.

        Returns:
            dict: The corresponding supply chain data if the query matches a known activity, or an error message.
        """
        query = query.lower()
        logger.info(f"Received query: {query}")

        # Check if the query matches any of the known supply chain activities
        for activity, filename in self.query_mapping.items():
            activity_words = set(activity.split(' '))
            print("Active {activity_words}")
            query_words = set(query.split())
            print(f"Active {activity} query {query}")
            if activity_words & query_words:
                file_path = os.path.join(self.database_folder, filename)
                if os.path.exists(file_path):
                    logger.info(f"Reading data from file: {file_path}")
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    logger.info(f"Retrieved data: {data}")
                    return data
                else:
                    logger.error(f"File not found: {file_path}")

        # If no matching activity is found, return an error message
        error_message = {"error": "No data found for the given query"}
        logger.warning(f"No data found for query: {query}")
        return error_message