import pandas as pd
import ollama
from ollama import Client

file_path = './datasets/UNSW/training_test_set/UNSW_NB15_training-set.csv'

if __name__ == '__main__':
    #df = pd.read_csv(file_path)
    #df = df.drop(columns=['id','attack_cat'])
    #print(df.head())
    client = Client(host='http://ollama:11434')
    #client.pull('llama3')
    for i in range(3):
        response = client.chat(model='llama3', messages=[
            {
              'role': 'user',
              'content': 'Chi è john Cerutti?',
            },
        ])
        print(response['message']['content'])


