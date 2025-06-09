import requests
import json # For handling JSON tool calls
from src.config import TOGETHER_API_KEY, TOGETHER_API_URL, LLAMA_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE, LLM_MAX_TOOL_CALL_TURNS
from search.data_searcher import search_mobiles

AVAILABLE_TOOLS = {
    "search_mobiles": search_mobiles
}

LLM_TOOL_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_mobiles",
            "description": "Searches the electronics store's mobile phone catalog for products based on various criteria like brand, title, price range, storage, and rating. Use this tool if the user is asking to find or list phones with specific attributes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price of the phone (e.g., 500 for $500).",
                        "nullable": True
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price of the phone (e.g., 1000 for $1000).",
                        "nullable": True
                    },
                    "brand": {
                        "type": "string",
                        "description": "Brand of the phone (e.g., 'Apple', 'Samsung', 'Google', 'Xiaomi', 'OnePlus', 'Nokia').",
                        "nullable": True
                    },
                    "title": {
                        "type": "string",
                        "description": "Specific title or model name of the phone (e.g., 'iPhone 15 Pro Max', 'Galaxy S24 Ultra', 'Pixel 8 Pro').",
                        "nullable": True
                    },
                    "min_storage_gb": {
                        "type": "integer",
                        "description": "Minimum storage in GB (e.g., 128 for 128GB).",
                        "nullable": True
                    },
                    "max_storage_gb": {
                        "type": "integer",
                        "description": "Maximum storage in GB.",
                        "nullable": True
                    },
                    "min_rating": {
                        "type": "number",
                        "description": "Minimum user rating (e.g., 4.5).",
                        "nullable": True
                    }
                },
                "required": []
            }
        }
    }
]


def call_together_api(messages: list, tools: list = None):
    """Internal helper to call Together AI API."""
    if not TOGETHER_API_KEY or TOGETHER_API_KEY == "YOUR_TOGETHER_API_KEY_HERE":
        raise ValueError("TOGETHER_API_KEY is not set or is a placeholder.")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLAMA_MODEL,
        "messages": messages,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
        "tools": tools
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response: {response.text}")
        raise requests.exceptions.RequestException(f"Together API HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        raise requests.exceptions.RequestException(f"Together API Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        raise requests.exceptions.RequestException(f"Together API Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong with the API request: {err}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during Together API call: {e}")
        raise


def analyze_with_llama3(text_input: str) -> str:
    """
    Sends transcribed text to Together API for Llama 3 analysis,
    handling potential tool calls for data searching.
    Args:
        text_input (str): The text to be analyzed by Llama 3.
    Returns:
        str: The analysis text from Llama 3 or an error message.
    """
    print("Initiating Llama 3 analysis...")

    messages = [
        {"role": "system", "content": "You are an AI assistant for an electronics store. Your primary task is to analyze customer feedback from call recordings. You can also answer questions about available mobile phones by using the provided `search_mobiles` tool. Your response must be in the first person, as if you are directly speaking to the customer. Address the customer directly. Do not summarize; instead, directly convey the information or analysis. Avoid using any special characters such as asterisks, hyphens, bullet points, or other formatting symbols. Present your response as plain text. If you use the tool, I will tell the customer the results clearly myself."},
        {"role": "user", "content": f"Customer feedback: \"{text_input}\""}
    ]

    for i in range(LLM_MAX_TOOL_CALL_TURNS):
        try:
            print(f"\n--- LLM Turn {i+1} ---")
            print("Sending messages to Llama 3...")
            response_json = call_together_api(messages, tools=LLM_TOOL_SCHEMA)
            choice = response_json.get("choices", [{}])[0]
            message = choice.get("message", {})
            
            # If the LLM wants to call a tool
            if message.get("tool_calls"):
                print("Llama 3 requested a tool call.")
                messages.append(message)

                for tool_call in message["tool_calls"]:
                    function_name = tool_call["function"]["name"]
                    function_args = tool_call["function"]["arguments"]
                    tool_call_id = tool_call["id"]

                    print(f"  Tool Name: {function_name}")
                    print(f"  Tool Args: {json.dumps(function_args, indent=2)}")

                    if function_name in AVAILABLE_TOOLS:
                        try:
                            
                            tool_output = AVAILABLE_TOOLS[function_name](**function_args)
                            print(f"  Tool Output: {tool_output}")
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "content": tool_output
                            })
                        except Exception as e:
                            tool_error_msg = f"Error executing tool '{function_name}': {e}"
                            print(f"  {tool_error_msg}")
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "content": tool_error_msg
                            })
                    else:
                        tool_error_msg = f"Error: Tool '{function_name}' not found."
                        print(f"  {tool_error_msg}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": tool_error_msg
                        })
                continue 

            elif message.get("content"):
                analysis_text = message["content"].strip()
                print("Llama 3 Analysis (Final):\n", analysis_text)
                return analysis_text
            else:
                print("Error: No content or tool calls in Llama 3 response.")
                return "No analysis or valid response could be generated."

        except requests.exceptions.RequestException as e:
            return f"Error contacting Together API: {e}"
        except ValueError as e:
            return f"Configuration Error: {e}"
        except Exception as e:
            print(f"An unexpected error occurred during Llama 3 analysis: {e}")
            return "An unexpected error occurred during analysis."
    
    return "Maximum tool call turns reached without a final answer. Please try again."
