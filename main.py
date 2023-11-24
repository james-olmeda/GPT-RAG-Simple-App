# Import the 'Chat' class from the 'chat' module
from chat import Chat

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Create an instance of the 'Chat' class
    chat_app = Chat()
    
    # Run the chat application
    chat_app.run()
