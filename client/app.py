import gradio as gr
import requests

API_URL = "http://localhost:8000/generate"

def chat_fn(message, history):
    try:
        resp = requests.post(API_URL, json={"prompt": message})
        if resp.status_code == 200:
            return resp.json()["generated_text"]
        return f"Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"API Error: {str(e)}"


gr.ChatInterface(
    fn=chat_fn,
    title="Chatbot by Subrata Kumar Rana"
).launch(server_name="0.0.0.0", server_port=7000)