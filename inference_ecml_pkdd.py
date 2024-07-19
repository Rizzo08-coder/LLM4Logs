import pandas as pd
from ollama import Client
import json

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
            'content': f'''You are a Web Security Expert specializing in log analysis for system defense.
You are responsible for monitoring and interpreting web server logs to detect and mitigate security threats.
You will receive dumps of HTTP request and you will need to determine if the provided request is legit or identifies as a malicious threat.
Print a JSON object with a key "result" containing a value of 0, if the request logged is legit / normal and 1 if the request logged is instead related to a malicious activity.
Do not print anything else, print only the JSON.'''
        },
    ]
    for idx in range(shots):
        messages.append({
            'role': 'user',
            'content': f'{df_training.iloc[idx]['request']}'
        })
        messages.append({
            'role': 'assistant',
            'content': f'{{ "result": {df_training.iloc[idx]['label']} }}'
        })
    messages.append({
        'role': 'user',
        'content': f'{row["request"]}'
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
    number_of_shots = 1
    output_filename = f'ecmlpkdd-deepseekcoder-{number_of_shots}.csv'

    training_dataset = './datasets/ECML_PKDD/fine_tune_dataset.csv'
    df_training = pd.read_csv(training_dataset)

    test_dataset = './datasets/ECML_PKDD/inference_dataset.csv'
    df_test = pd.read_csv(test_dataset)

    client = Client(host='http://ollama:11434')
    client.pull(model_name)

    df_test['predicted'] = df_test.apply(lambda row: nshots_prediction(row, model=model_name, shots=number_of_shots), axis=1)

    print(sum(abs(df_test['label'] - df_test['predicted'])))
    df_test.to_csv(output_filename)