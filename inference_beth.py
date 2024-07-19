import pandas as pd
from ollama import Client
import json

def prompt_beth(row):
    return f"""
seconds since system boot = {row['timestamp']}
integer label for the process spawning this log = {row['processId']}
integer label for the thread spawning this log = {row['threadId']}
parent's integer label for the process spawning this log = {row['parentProcessId']}
Login integer ID of user spawning this log = {row['userId']}
Set mounting restrictions this process log works within = {row['mountNamespace']}
String command executed = {row['processName']}
Name of host server = {row['hostName']}
ID for the event generating this log = {row['eventId']}
Name of the event generating this log = {row['eventName']}
stack memory addresses relevant to the process = {row['stackAddresses']}
number of args = {row['argsNum']}
Value returned from this event log (usually 0) = {row['returnValue']}
List of arguments passed to this process = {row['args']}
"""

def extract_json(text):
    jsonstr = ''
    brackets = 0
    for c in text:
        if c == '{':
            brackets += 1
            jsonstr += c
        elif c == '}':
            brackets -= 1
            jsonstr += c
            if brackets == 0:
                break
        elif brackets > 0:
            jsonstr += c

    return json.loads(jsonstr)


def nshots_prediction(row, model='llama3', shots=0):
    messages = [
        {
            'role': 'system',
            'content': f'''You are a cybersecurity sysadmin expert, tasked with the analysis of some system event
log files. You will receive the properties of an event from a logged system process call.
Print a JSON with a "result" key containing 0 if the event is legit or 1 if the event is instead related to a malicious activity.'''
        },
    ]
    for idx in range(shots):
        messages.append({
            'role': 'user',
            'content': f'''>>> These are the attributes from the logged event:
            {prompt_beth(df_training.iloc[idx])}
            >>> The event provided represents a normal or a malicious activity?
            '''
        })
        messages.append({
            'role': 'assistant',
            'content': f'{{ "result": {df_training.iloc[idx]['evil']} }}'
        })
    messages.append({
        'role': 'user',
        'content': f'''>>> These are the attributes from the logged event:
    {prompt_beth(row)}
    >>> The event provided represents a normal or a malicious activity?
    '''
    })

    response = client.chat(model=model, messages=messages)
    response = response['message']['content']
    try:
        return int(extract_json(response)['result'])
        return int(response)
    except:
        return 2

if __name__ == '__main__':
    model_name = 'deepseek-coder:6.7b'
    number_of_shots = 5
    output_filename = f'beth-deepseekcoder-{number_of_shots}.csv'

    training_dataset = './datasets/BETH/fine_tune_dataset_BETH.csv'
    df_training = pd.read_csv(training_dataset)

    test_dataset = './datasets/BETH/inference_dataset_BETH.csv'
    df_test = pd.read_csv(test_dataset)

    client = Client(host='http://ollama:11434')
    # client.pull(model_name)

    df_test['predicted'] = df_test.apply(lambda row: nshots_prediction(row, model=model_name, shots=number_of_shots), axis=1)

    print(sum(abs(df_test['evil'] - df_test['predicted'])))
    df_test.to_csv(output_filename)