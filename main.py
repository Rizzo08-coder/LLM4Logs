import pandas as pd
import ollama
from ollama import Client
#from transformers import pipeline

features_dataset = './datasets/UNSW/features/NUSW-NB15_features.csv'
training_dataset = './datasets/UNSW/training_test_set/UNSW_NB15_training-set.csv'
test_dataset = './datasets/UNSW/training_test_set/UNSW_NB15_testing-set.csv'

def oneshot(row):
    response = client.chat(model='llama3', messages=[
        {
            'role': 'system',
            'content': f'''You are a cybersecurity expert. You have to make an analysis of some log files, and you know the pattern of them.
             You will receive the contents of a single log event, with the meaning of each value field explained
             and you will tell me if the log corresponds to normal traffic or to a malicious activity.
             Print 0 if it is a log identifying a normal / legit activity or 1 if it is a log identifying a malicious activity.
             Do not print anything else, print only the correct digit, and do not provide explanations.'''
        },
        {
            'role': 'user',
            'content': f'{df_training.drop(columns=['label']).iloc[0]}'
        },
        {
            'role': 'assistant',
            'content': f'{df_training.iloc[0]['label']}'
        },
        {
            'role': 'user',
            'content': f'{row.drop(columns=['label'])}'
        },
    ])
    return int(response['message']['content'])


if __name__ == '__main__':
    df_features = pd.read_csv(features_dataset)
    df_features = df_features.drop(columns=['No.'])

    df_training = pd.read_csv(training_dataset)
    df_training = df_training.drop(columns=['id','attack_cat'])
    col_map = {l[0]: l[1] for l in df_features[['Name', 'Description']].replace(to_replace=r'\(\d+\)', value='', regex=True).to_dict(index=False, orient='tight')['data']}
    df_training = df_training.rename(columns=col_map)

    df_test = pd.read_csv(test_dataset)
    df_test = df_test.drop(columns=['id','attack_cat'])
    col_map = {l[0]: l[1] for l in df_features[['Name', 'Description']].replace(to_replace=r'\(\d+\)', value='', regex=True).to_dict(index=False, orient='tight')['data']}
    df_test = df_test.rename(columns=col_map)

    results = []

    client = Client(host='http://ollama:11434')
    client.pull('llama3')

    df_test['predicted'] = df_test.apply(lambda row: oneshot(row), axis=1)

    print(sum(abs(df_test['label'] - df_test['predicted'])))
    df_test.to_csv('testrun-one-llama.csv')
    #pipe = pipeline("text-generation", model="Salesforce/codegen-6B-multi")




