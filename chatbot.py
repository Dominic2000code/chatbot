from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

# Load environment variables from the .env file
load_dotenv()

# initialize the Gemini client
client = genai.Client()

SPARKY = r"""
     _____                  _          
    /  ___|                | |         
    \ `--. _ __   __ _ _ __| | ___   _ 
     `--. \ '_ \ / _` | '__| |/ / | | |
    /\__/ / |_) | (_| | |  |   <| |_| |
    \____/| .__/ \__,_|_|  |_|\_\\__, |
          | |                     __/ |
          |_|                    |___/ 
"""

BLACK_BEARD = r"""
    ______ _            _     ______                    _ 
    | ___ \ |          | |    | ___ \                  | |
    | |_/ / | __ _  ___| | __ | |_/ / ___  __ _ _ __ __| |
    | ___ \ |/ _` |/ __| |/ / | ___ \/ _ \/ _` | '__/ _` |
    | |_/ / | (_| | (__|   <  | |_/ /  __/ (_| | | | (_| |
    \____/|_|\__,_|\___|_|\_\ \____/ \___|\__,_|_|  \__,_|
    
"""

WORDSWORTH = r"""
    _    _ _ _ _ _                   _    _               _                        _   _     
    | |  | (_) | (_)                 | |  | |             | |                      | | | |    
    | |  | |_| | |_  __ _ _ __ ___   | |  | | ___  _ __ __| |_____      _____  _ __| |_| |__  
    | |/\| | | | | |/ _` | '_ ` _ \  | |/\| |/ _ \| '__/ _` / __\ \ /\ / / _ \| '__| __| '_ \ 
    \  /\  / | | | | (_| | | | | | | \  /\  / (_) | | | (_| \__ \\ V  V / (_) | |  | |_| | | |
    \/  \/|_|_|_|_|\__,_|_| |_| |_|  \/  \/ \___/|_|  \__,_|___/ \_/\_/ \___/|_|   \__|_| |_|
    
"""


# Define the chatbot personality
PERSONALITIES = {
    "tutor": {
        "name": "Sparky",
        "prompt": """You are a friendly and enthusiastic coding tutor named Sparky. You explain technical concepts in simple terms using analogies and examples. You keep responses concise (2-3 paragraphs max) and always encourage the learner. When you don't know something, you say so honestly.""",
        "greeting": "Hi! I'm Sparky, your friendly coding tutor!\nAsk me anything about programming.",
        "name_symbol": SPARKY
    },
    "pirate": {
        "name": "Captain Blackbeard",
        "prompt": """You are a boisterous, swashbuckling pirate captain named Captain Blackbeard. You speak in heavy pirate slang (e.g., "Ahoy", "ye", "matey", "shiver me timbers") and love using sailing metaphors. You answer questions with a dramatic, adventurous flair and often refer to what the "crew" or "the sea" is doing. Keep your responses engaging and bold, and always sign off with a pirate's cheer.""",
        "greeting": "Ahoy there, ye scallywag! Step aboard and state your business! What grand adventure or hidden treasure be ye seekin' today?",
        "name_symbol": BLACK_BEARD
    },
    "poet": {
        "name": " William Wordsworth",
        "prompt": """You are an eloquent, romantic, and deeply reflective poet named William Wordsworth. You see beauty in the mundane and speak with a lyrical, rhythmic, and slightly archaic tone. You often use metaphors, personification, and sensory imagery in your answers. You appreciate quiet, introspective thoughts and encourage users to look deeper into the meaning of their questions.""",
        "greeting": "Welcome, traveler of the digital winds. The ink is ready and the parchment is waiting. What thoughts or stories are blossoming in your mind today?",
        "name_symbol": WORDSWORTH
    }
}


def create_chat(personality_key):
    """Create a new chat session with the system prompt."""
    
    personality = PERSONALITIES[personality_key]
    
    config = types.GenerateContentConfig(
        system_instruction= personality.get('prompt')
    )
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=config,
    )
    
    return chat, personality

def stream_response(response):
    """Print streamin response chunks as they arrive."""
    
    for chunk in response:
        print(chunk.text, end="", flush=True)
    print() # add new line after response completes

def show_personality_menu():
    """Display personality choices for end user"""
    
    persona_dict= {}
    
    print("\n" + "-" * 40)
    print("Available personalities:")
    for i, (key, persona) in enumerate(PERSONALITIES.items(), 1):
        print(f"  {i}. {persona['name']} ({key})")
        persona_dict[i] = key
    print("-" * 40)
    
    while True:
        try:
            personality_choice = int(input("Pick a number between (1-3): ").strip())
            if personality_choice in (1,2,3):
                return persona_dict[personality_choice]
            print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a number")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break



def main():
    """Main chatbot loop."""
    
    
    selected_persona = "tutor"
    
    print("=" * 50)
    print(SPARKY)
    print("Hi! I'm Sparky, your friendly coding tutor!")
    print("Ask me anything about programming.")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("Type '/switch' to change chatbot personality.")
    print("=" * 50)
    print()
    
    chat, personality = create_chat(selected_persona)
    
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == "/switch":
            new_persona = show_personality_menu()
            if new_persona != selected_persona:
                selected_persona = new_persona
                chat, personality = create_chat(selected_persona)
                print("=" * 50)
                print(personality.get('name_symbol'))
                print(f"Hi! I'm {personality.get('name')}, your friendly {selected_persona}!")
                print(f"{personality.get('greeting')}")
                print("Type 'quit' or 'exit' to end the conversation.")
                print("Type '/switch' to change chatbot personality.")
                print("=" * 50)
                print()
            else:
                print(f"\nAlready using {personality.get('name')}!\n")
            continue
        
        if user_input.lower() in ("quit", "exit"):
            print(f"\n{personality.get('name')}: It was great chatting with you! Keep coding! 🚀")
            break
        
        try:
            print(f"{personality.get('name')}: ", end="", flush=True)
            response = chat.send_message_stream(user_input)
            stream_response(response)
            print()
        except Exception as e:
            print(f"\nOops! Something terrible happened: {e}")
            print("Let's try again.\n")

    # Display conversation history
    print("\n" + "=" * 50)
    print("Conversation History:")
    print("=" * 50)
    for message in chat.get_history():
        role = "You" if message.role == "user" else personality.get('name')
        text = message.parts[0].text
        preview = text[:100] + "..." if len(text) > 100 else text
        print(f"  {role}: {preview}")

if __name__ == "__main__":
    main()