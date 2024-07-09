import pandas as pd

training_dataset = './datasets/ECML_PKDD/xml_test.txt'

if __name__ == '__main__':

    with open(training_dataset, 'r') as file:
        text_data = file.read()

    data_dict = {'id': [], 'label': [], 'request':[]}
    requestbody = ''
    for line in text_data.splitlines():
        if line.startswith('Start - Id'):
            token = line.split(': ')
            data_dict['id'].append(token[-1])
        elif line.startswith('class'):
            token = line.split(': ')
            data_dict['label'].append(token[-1])
        elif line.startswith('End - Id'):
            data_dict['request'].append(requestbody)
            requestbody = ''
        else:
            requestbody += line
            requestbody += '\n'

    df = pd.DataFrame(data_dict)
    print(df.head())

    df['label'] = df['label'].apply(lambda x: 0 if x == 'Valid' else 1)
    print(df.head())

    csv_file_path = './datasets/ECML_PKDD/ECML_df.csv'
    df.to_csv(csv_file_path, index=False)

    print(df['label'].value_counts())
