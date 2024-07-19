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
            'content': f'''You are a cybersecurity expert. You have to make an analysis of some log files, and you know the pattern of them.
             You will receive the contents of a single log event, with the meaning of each value field explained
             and you will tell me if the log corresponds to normal traffic or to a malicious activity.
             Print 0 if it is a log identifying a normal / legit activity or 1 if it is a log identifying a malicious activity.
             Do not print anything else, print only the correct digit, and do not provide explanations.'''
        },
    ]
    for idx in range(shots):
        messages.append({
            'role': 'user',
            'content': f'{df_training.drop(columns=['label']).iloc[idx]}'
        })
        messages.append({
            'role': 'assistant',
            'content': f'{df_training.iloc[idx]['label']}'
        })
    messages.append({
        'role': 'user',
        'content': f'{row.drop(columns=['label'])}'
    })

    response = client.chat(model=model, messages=messages)
    return int(response['message']['content'])

if __name__ == '__main__':
    model_name = 'codellama'
    number_of_shots = 1
    output_filename = f'out-{model_name}-{number_of_shots}.csv'

    features_dataset = './datasets/UNSW/features/NUSW-NB15_features.csv'
    df_features = pd.read_csv(features_dataset)
    df_features = df_features.drop(columns=['No.'])

    training_dataset = './datasets/UNSW/subsets/fine_tune_dataset.csv'
    df_training = pd.read_csv(training_dataset)
    col_map = {l[0]: l[1] for l in df_features[['Name', 'Description']].replace(to_replace=r'\(\d+\)', value='', regex=True).to_dict(index=False, orient='tight')['data']}
    df_training = df_training.rename(columns=col_map)

    test_dataset = './datasets/UNSW/subsets/inference_dataset.csv'
    df_test = pd.read_csv(test_dataset)
    col_map = {l[0]: l[1] for l in df_features[['Name', 'Description']].replace(to_replace=r'\(\d+\)', value='', regex=True).to_dict(index=False, orient='tight')['data']}
    df_test = df_test.rename(columns=col_map)

    client = Client(host='http://ollama:11434')
    client.pull(model_name)

    df_test['predicted'] = df_test.apply(lambda row: nshots_prediction(row, model=model_name, shots=number_of_shots), axis=1)

    print(sum(abs(df_test['label'] - df_test['predicted'])))
    df_test.to_csv(output_filename)




