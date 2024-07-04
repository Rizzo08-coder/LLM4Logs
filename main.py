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
    df_training = df_training.drop(columns=['id','attack_cat', 'label'])
    print(df_training.head())

    client = Client(host='http://ollama:11434')
    client.pull('llama3')
    response = client.chat(model='llama3', messages=[
       {
          'role': 'system',
          'content': f'''You are a cybersecurity expert, you have to make a log files analysis, and you know the pattern of them.
           The pattern is this: {df_features} , the first column indicates the acronym of the feature, 
           the second indicates the value type and the last one is the description of the feature.
           You will receive a single log where you have all the features that i explain above 
           separates by a comma and you will tell me if it is a normal log or malicious log and you put the result inside a 
           json: 0 for normal and 1 for malicious'''
           ,
       },
       {
          'role': 'user',
          'content': f'''{df_training.iloc[0]}'''
       },
    ])
    print(response['message']['content'])

    #pipe = pipeline("text-generation", model="Salesforce/codegen-6B-multi")




