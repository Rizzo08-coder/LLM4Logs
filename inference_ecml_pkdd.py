import pandas as pd
from ollama import Client
import prompts


def nshots_prediction(row, model='llama3', shots=0, useJson=False):
    str_request = ""
    if useJson:
        str_request = """Print a JSON object with a key "result" containing a value of 0, if the request logged is legit / normal and 1 if the request logged is instead related to a malicious activity.
Do not print anything else, print only the JSON."""
    else:
        str_request = """Print 0 if it is a log identifying a normal / legit request or 1 if it is a log identifying a malicious request.
Do not print anything else, print only the correct digit, and do not provide explanations."""

    messages = [
        {
            'role': 'system',
            'content': f'''You are a Web Security Expert specializing in log analysis for system defense.
You are responsible for monitoring and interpreting web server logs to detect and mitigate security threats.
You will receive dumps of HTTP request and you will need to determine if the provided request is legit or identifies as a malicious threat. ''' + str_request
        },
    ]
    for idx in range(shots):
        messages.append({
            'role': 'user',
            'content': f'''>>> These are the attributes from the logged HTTP request:
            {df_training.iloc[idx]["request"]}
            >>> The HTTP request provided represents a normal or a malicious activity?
            '''
        })
        messages.append({
            'role': 'assistant',
            'content': f'{{ "result": {df_training.iloc[idx]["label"]} }}'
        })
    messages.append({
        'role': 'user',
        'content': f'''>>> These are the attributes from the logged HTTP request:
        {row["request"]}
        >>> The HTTP request provided represents a normal or a malicious activity?
        '''
    })

    response = client.chat(model=model, messages=messages)
    response = response['message']['content']
    try:
        if useJson:
            return int(prompts.extract_json(response)['result'])
        else:
            return int(response)
    except:
        return 2

if __name__ == '__main__':
    #iperparametri: modificare a piacere
    model_name = 'deepseek-coder:6.7b'
    number_of_shots = 1
    useJson = True

    output_filename = f'ecmlpkdd-{model_name if ":" not in model_name else model_name.split(":")[0]}-{number_of_shots}.csv'

    training_dataset = './datasets/ECMLPKDD/fine_tune_dataset.csv'
    df_training = pd.read_csv(training_dataset)

    inference_dataset = './datasets/ECMLPKDD/inference_dataset.csv'
    df_inference = pd.read_csv(inference_dataset)

    client = Client(host='http://ollama:11434')
    client.pull(model_name)

    df_inference['predicted'] = df_inference.apply(lambda row: nshots_prediction(row, model=model_name, shots=number_of_shots, useJson=useJson), axis=1)

    print(sum(abs(df_inference['label'] - df_inference['predicted'])))
    df_inference.to_csv(output_filename)