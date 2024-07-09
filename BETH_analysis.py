import pandas as pd

training_dataset = './datasets/BETH/labelled_testing_data.csv'

if __name__ == '__main__':
    df = pd.read_csv(training_dataset)
    df.drop('sus', axis=1, inplace=True)
    print(df.head())

    csv_file_path = './datasets/BETH/BETH_df.csv'
    df.to_csv(csv_file_path, index=False)