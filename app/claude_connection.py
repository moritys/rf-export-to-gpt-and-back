import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()
client.api_key = os.getenv('ANTHROPIC_API_KEY')


def send_message(prompt, text):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )
    formatted_output = "\n".join(text_block.text for text_block in message.content if hasattr(text_block, 'text'))
    return formatted_output
