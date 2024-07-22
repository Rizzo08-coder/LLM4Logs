import pandas as pd
from ollama import Client
import prompts


def nshots_prediction(row, model='llama3', shots=0, useJson=False):
    str_request = ""
    if useJson:
        str_request = """Print a JSON with a "result" key containing 0 if the event is legit or 1 if the event is instead related to a malicious activity."""
    else:
        str_request = """Print 0 if it is a log identifying a normal / legit activity or 1 if it is a log identifying a malicious activity.
    Do not print anything else, print only the correct digit, and do not provide explanations."""
    messages = [
        {
            'role': 'system',
            'content': f'''You are a cybersecurity sysadmin expert, tasked with the analysis of some system event
log files. You will receive the properties of an event from a logged system process call.''' + str_request
        },
    ]
    for idx in range(shots):
        messages.append({
            'role': 'user',
            'content': f'''>>> These are the attributes from the logged event:
            {prompts.prompt_beth(df_training.iloc[idx])}
            >>> The event provided represents a normal or a malicious activity?
            '''
        })
        messages.append({
            'role': 'assistant',
            'content': f'{{ "result": {df_training.iloc[idx]["evil"]} }}'
        })
    messages.append({
        'role': 'user',
        'content': f'''>>> These are the attributes from the logged event:
    {prompts.prompt_beth(row)}
    >>> The event provided represents a normal or a malicious activity?
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
    # Hyperparameters: update as you prefer
    model_name = 'deepseek-coder:6.7b'
    number_of_shots = 5 # >= 0
    useJson = True


    output_filename = f'beth-{model_name if ":" not in model_name else model_name.split(":")[0]}-{number_of_shots}.csv'

    training_dataset = './datasets/BETH/fine_tune_dataset.csv'
    df_training = pd.read_csv(training_dataset)

    inference_dataset = './datasets/BETH/inference_dataset.csv'
    df_inference = pd.read_csv(inference_dataset)

    client = Client(host='http://ollama:11434')
    client.pull(model_name)

    df_inference['predicted'] = df_inference.apply(lambda row: nshots_prediction(row, model=model_name, shots=number_of_shots, useJson=useJson), axis=1)

    print(sum(abs(df_inference['evil'] - df_inference['predicted'])))
    df_inference.to_csv(output_filename)