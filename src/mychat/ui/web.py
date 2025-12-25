import gradio as gr
import sys
from mychat.core.service import ChatService

def run_web():
    try:
        # We start a service. Note: This creates/loads a session on startup.
        service = ChatService()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    def predict(message, history):
        # Gradio history is provided but we rely on internal service state for persistence validation
        # We accumulate chunks to yield full message for Gradio real-time update
        full_response = ""
        for chunk in service.chat(message):
            full_response += chunk
            yield full_response

    # Create a nice UI
    with gr.Blocks(fill_height=True, title="MyChat Web") as demo:
        gr.Markdown("# 🤖 MyChat AI")
        
        # We can implement a mechanism to load history into Chatbot if needed, 
        # but for now standard ChatInterface is sufficient.
        # Note: If we really wanted to show per-session history on reload, we'd need more complex Gradio state.
        
        gr.ChatInterface(
            fn=predict,
            examples=["Hello", "What is the capital of Vietnam?", "Write a python script"],
            submit_btn="Send",
            stop_btn="Stop",
        )

    demo.launch(inbrowser=True)
