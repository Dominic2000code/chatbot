# Gemini Chatbot

A simple interactive chatbot built with Google Gemini via the `google-genai` Python client.

The script `chatbot.py` loads environment variables from a `.env` file using `python-dotenv`, connects to Gemini, and allows conversation with three personalities: a friendly coding tutor, a pirate captain, and a romantic poet.

## Features

- Select or switch between personalities during the chat
- Stream Gemini responses in real time
- Friendly prompts and ASCII banner art for each personality
- Conversation history shown after exiting

## Requirements

- Python 3.10+ recommended
- `python-dotenv`
- `google-genai`

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Gemini API Key Setup

This project uses the Google Gemini (Generative AI) client, which requires authentication to work.

1. Go to the Google Cloud Console: https://aistudio.google.com/
2. Sign in with your Google account.
3. Click Get API Key in the left sidebar.
4. Click Create API key.
5. Copy the key that appears and save it somewhere safe (you will need it in the next substep).

Example `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
````

The script already calls `load_dotenv()`, so it will automatically load these values from `.env`.

## Run the Chatbot

From the project directory:

```bash
python chatbot.py
```

## How to Use

- Type any question or prompt and press Enter.
- Type `/switch` to change personality.
- Type `quit` or `exit` to end the chat.

## Personalities

- `tutor` — Sparky, the friendly coding tutor
- `pirate` — Captain Blackbeard, the adventurous pirate
- `poet` — William Wordsworth, the lyrical poet

## Notes

- If you see authentication errors, confirm that your `.env` file is present and that `GEMINI_API_KEY` is set correctly.
- The script uses `client = genai.Client()` and reads credentials from environment variables.
- feel free to fork and add more personalities
