import sys
from mychat.core.service import ChatService

def run_cli():
    print("Initializing mychat CLI...")
    try:
        service = ChatService()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Session ID: {service.current_session.id}")
    print("Type 'exit' or 'quit' to end. Type 'new' to start a new session.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            break

        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        if user_input.lower() == "new":
            service.start_new_session()
            print(f"Started new session: {service.current_session.id}")
            continue

        print("Assistant: ", end="", flush=True)
        for chunk in service.chat(user_input):
            print(chunk, end="", flush=True)
        print() # Newline at end
