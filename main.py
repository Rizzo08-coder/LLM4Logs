import pandas as pd
import ollama
from ollama import Client
from transformers import pipeline

features_dataset = './datasets/UNSW/ds_completo/NUSW-NB15_features.csv'
training_dataset = './datasets/UNSW/training_test_set/UNSW_NB15_training-set.csv'

if __name__ == '__main__':

    df_features = pd.read_csv(features_dataset)
    df_features = df_features.drop(columns=['No.'])
    print(df_features)

    df_training = pd.read_csv(training_dataset)
    df_training = df_training.drop(columns=['id','attack_cat'])
    print(df_training.head())

    results = []

    client = Client(host='http://ollama:11434')
    client.pull('llama3')
    # for i in range(175_341):
    for i in range(1000):
        response = client.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': f'''You are a cybersecurity expert, you have to make a log files analysis, and you know the pattern of them.
                 The pattern is this: {df_features}, where the first column indicates the acronym of the feature, 
                 the second indicates the value type and the last one is the description of the feature.
                 You will receive a single log where you have all the features that were explained above in the same order,
                 and you will tell me if the log corresponds to a normal activity or a malicious activity.
                 Print 0 if it is a log identifying a normal activity or 1 if it is a log identifying a malicious activity.
                 Do not print anything else, only the number.'''
            },
            {
                'role': 'user',
                'content': f'{df_training.drop(columns=['label']).iloc[175_337]}'
            },
            {
                'role': 'assistant',
                'content': f'{df_training.iloc[175_337]['label']}'
            },
            {
                'role': 'user',
                'content': f'{df_training.drop(columns=['label']).iloc[i]}'
            },
        ])
        results.append(int(response['message']['content']))

    df_training = df_training.head(n=1000).assign(predicted=pd.Series(results).values)
    print(sum(abs(df_training['label'] - df_training['predicted'])))
    #pipe = pipeline("text-generation", model="Salesforce/codegen-6B-multi")




