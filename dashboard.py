from groq import Groq
import os
import json
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = 'llama3-70b-8192'

def get_supply_chain_data(query):
    """Get the supply chain data for a given query by calling the Flask API."""
    url = f'http://127.0.0.1:5000/supply-chain-data?query={query}'
    response = requests.get(url)
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code})

def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a function calling LLM that uses the data extracted from the get_supply_chain_data function to answer questions related to supply chain management. Include the relevant supply chain activity and data in your response."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_supply_chain_data",
                "description": "Get the supply chain data for a given query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query related to a supply chain activity",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "get_supply_chain_data": get_supply_chain_data,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                query=function_args.get("query")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content


import gradio as gr
import os
import time
import threading
from datetime import datetime
import random

def gradio_interface(user_prompt):
    return run_conversation(user_prompt)

def update_stats():
    while True:
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        inventory_level = random.randint(50, 100)
        order_fulfillment_rate = random.uniform(85, 99)
        transport_efficiency = random.uniform(70, 95)
        supplier_on_time_delivery = random.uniform(90, 100)

        stats_text.value = (
            f"Latest System Clock: {current_time}\n"
            f"Inventory Level: {inventory_level}%\n"
            f"Order Fulfillment Rate: {order_fulfillment_rate:.2f}%\n"
            f"Transport Efficiency: {transport_efficiency:.2f}%\n"
            f"Supplier On-Time Delivery: {supplier_on_time_delivery:.2f}%"
        )
        time.sleep(1)

# Ensure the image path is correctly referenced
background_path = os.path.join(os.getcwd(), 'images/background.png')

with gr.Blocks(css=f"""
    .gradio-container {{
        color: #003366;
        font-family: Arial, sans-serif;
    }}
    .header {{
        text-align: center;
        padding: 20px;
    }}
    .header h1 {{
        margin: 0;
        color: #003366;
        font-size: 2.5em;
    }}
    .header p {{
        margin: 0;
        color: #006699;
        font-size: 1.2em;
    }}
    .textbox-label {{
        font-weight: bold;
    }}
    .submit-button {{
        background-color: #006699;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1em;
        cursor: pointer;
    }}
    .submit-button:hover {{
        background-color: #004466;
    }}
    .background-image {{
        width: 100%;
        height: auto;
    }}
    .stats {{
        font-size: 1.2em;
        color: #003366;
        text-align: center;
        margin-top: 20px;
    }}
""") as demo:
    gr.Markdown("""
        <div class="header">
            <h1>SupplyChain Analytics</h1>
            <p>Your AI-powered supply chain management assistant</p>
        </div>
    """)
    gr.Markdown(f"""
        <img src="file://{background_path}" class="background-image">
    """)
    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(
                label="Enter your query",
                placeholder="Ask a question about supply chain management...",
                lines=3,
                elem_id="user-input"
            )
            submit_button = gr.Button("Submit", variant="primary", elem_classes="submit-button")

        with gr.Column(scale=2):
            output_text = gr.Textbox(
                label="Response",
                lines=10,
                elem_id="output-text"
            )

    stats_text = gr.Text(value="Loading...", label="Supply Chain Stats", interactive=False, elem_classes="stats")

    submit_button.click(
        gradio_interface,
        inputs=user_input,
        outputs=output_text,
    )

    threading.Thread(target=update_stats, daemon=True).start()

demo.launch()


