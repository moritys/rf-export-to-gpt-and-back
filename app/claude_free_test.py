from claude_api import Client
import os

cookie = os.environ.get('cookie')
claude_api = Client(cookie)


prompt = "Hello, Claude!"
conversation_id = "<conversation_id>" or claude_api.create_new_chat()['uuid']
response = claude_api.send_message(prompt, conversation_id)
print(response)
