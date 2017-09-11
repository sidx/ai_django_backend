import os.path
import sys
import json
from todo_client import process_tasks

try:
    import apiai
except ImportError:
    sys.path.append(
            os.path.joins(os.path.dirname(os.path.realpath(__file__)), os.pardir)
        )
    import apiai

CLIENT_ACCESS_TOKEN = 'bdc1904d09de4420964286b9386fb254'

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    while True:
        user_message = raw_input('>')
        if user_message == 'exit':
            break
        request = ai.text_request()
        request.lang = 'en' # Default
        request.query = user_message

        response = json.loads(request.getresponse().read())
        print response['result']
        if response['result']['action'] == 'input.unknown':
            print response['result']['fulfillment']['speech']
            continue
        if not response['result']['actionIncomplete']:
            task_result = process_tasks(response['result'])
        print response['result']['fulfillment']['speech']


if __name__ == '__main__':
    main()

