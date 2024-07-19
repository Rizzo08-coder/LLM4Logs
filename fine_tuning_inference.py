from ollama import Client
import pandas as pd
import prompts

def zeroshot(row, model):
    client = Client(host='http://ollama:11434')

    response = client.chat(model=model, messages=[{
        'role': 'user',
        'content': prompts.prompt_beth(row)
    }])

    return int(response['message']['content'])




if __name__ == '__main__':
    model_name = 'llama3-beth'
    output_filename = './finetune-llama3-beth.csv'
    df = pd.read_csv('datasets/BETH/inference_dataset.csv')

    df['predicted'] = df.apply(lambda row: zeroshot(row, model=model_name), axis=1)
    print(sum(abs(df['evil'] - df['predicted'])))
    df.to_csv(output_filename)


