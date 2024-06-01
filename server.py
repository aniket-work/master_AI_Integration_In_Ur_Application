from flask import Flask, request, jsonify
from data_retriever import SupplyChainDataRetriever
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
data_retriever = SupplyChainDataRetriever('database')

@app.route('/supply-chain-data', methods=['GET'])
def supply_chain():
    """
    Flask route to handle supply chain data retrieval requests.

    Query Parameters:
        query (str): The user's query related to a supply chain activity.

    Returns:
        JSON response: The corresponding supply chain data or an error message.
    """
    query = request.args.get('query', '')
    if not query:
        logger.error("Missing query parameter")
        return jsonify({'error': 'Missing query'}), 400

    logger.info(f"Received query: {query}")
    data = data_retriever.get_supply_chain_data(query)
    logger.info(f"Returning data: {data}")
    return jsonify(data)

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)