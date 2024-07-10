from ollama import Client
import pandas as pd




def nshots_prediction(row, model):
    client = Client(host='http://ollama:11434')

    response = client.chat(model=model, messages=[{
        'role': 'user',
        'content': f"""
seconds since system boot = {row['timestamp']}
integer label for the process spawning this log = {row['processId']}
integer label for the thread spawning this log = {row['threadId']}
parent's integer label for the process spawning this log = {row['parentProcessId']}
Login integer ID of user spawning this log = {row['userId']}
Set mounting restrictions this process log works within = {row['mountNamespace']}
String command executed = {row['processName']}
Name of host server = {row['hostName']}
ID for the event generating this log = {row['eventId']}
Name of the event generating this log = {row['eventName']}
stack memory addresses relevant to the process = {row['stackAddresses']}
number of args = {row['argsNum']}
Value returned from this event log (usually 0) = {row['returnValue']}
List of arguments passed to this process = {row['args']}
"""
    }])

    return int(response['message']['content'])




if __name__ == '__main__':
    model_name = 'Llama3BETH'
    output_filename = './datasets/BETH/output.csv'
    df = pd.read_csv('./datasets/BETH/inference_dataset_BETH.csv')

    df['predicted'] = df.apply(lambda row: nshots_prediction(row, model=model_name),axis=1)
    df.to_csv(output_filename)


