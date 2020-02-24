import pandas as pd


def read_csv(csv_file):
    return pd.read_csv(csv_file)


def write_csv(dataframe, file):
    return dataframe.to_csv(file, sep=',', encoding='utf-8')


def print_dataframe(dataframe, print_col=True, print_row=True):
    if print_col:
        print(' '.join(column for column in dataframe))
    '''
    if we want to get the column of the dataframe, we can use
    list(df) or
    list(df.columns) or
    df.columns.tolist()
    '''

    if print_row:
        for index, row in dataframe.iterrow():
            print(' '.join(str(row[column]) for column in dataframe))


if __name__ == '__main__':
    csv_file = 'Demographic_Statistics_By_Zip_Code.csv'
    dataframe = read_csv(csv_file)
    print('Loading the csv file')

    print_dataframe(dataframe)

    print('Write the dataframe as a csv file')
    write_csv(dataframe, 'week2_wrt_csv.csv')
