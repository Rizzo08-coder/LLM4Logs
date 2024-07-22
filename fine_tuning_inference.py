from ollama import Client
import pandas as pd
import prompts

def zeroshot(client, row, model):
    if model.endswith("beth"):
        content = prompts.prompt_beth(row)
    elif model.endswith("usnw"):
        content = prompts.prompt_unsw(row)
    else:
        content = row["request"]

    response = client.chat(model=model, messages=[{
        'role': 'user',
        'content': content
    }])

    return int(response['message']['content'])


if __name__ == '__main__':
    # Hyperparameters -> either one of these three:
    # - llama3-beth
    # - llama3-unsw
    # - llama3-ecmlpkdd
    model_name = 'llama3-beth'

    output_filename = f'./finetune-{model_name}.csv'

    df = pd.read_csv(f'datasets/{model_name.split("-")[-1].upper()}/inference_dataset.csv')

    client = Client(host='http://ollama:11434')

    df['predicted'] = df.apply(lambda row: zeroshot(client, row, model=model_name), axis=1)

    df.to_csv(output_filename)


