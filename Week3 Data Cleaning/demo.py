import pandas as pd


def print_dataframe(dataframe, print_cols=True, print_rows=True):
    if print_cols:
        print(','.join(column for column in dataframe))

    if print_rows:
        for index, row in dataframe.iterrows():
            print(' '.join(str(row[column]) for column in dataframe))


if __name__ == '__main__':
    """
    Section1: Dropping Unwanted Columns
    """

    book_file = 'Books.csv'
    df = pd.read_csv(book_file)

    columns_to_drop = ['Edition Statement',
                      'Corporate Author',
                      'Corporate Contributors',
                      'Former owner',
                      'Engraver',
                      'Contributors',
                      'Issuance type',
                      'Shelfmarks'
                      ]
    print("The percentage of NaN in the data per column:")
    num_of_rows = df.shape[0]
    for column in df:
        percent = 100 * df[column].isnull().sum() / num_of_rows
        print(column, str(percent) + '%')

    print("****************************************")
    print("Dataframe before dropping the columns")
    print_dataframe(df, print_rows=False)

    print("****************************************")
    print("Dataframe after dropping the columns")
    df.drop(columns_to_drop, inplace=True, axis=1)
    print_dataframe(df, print_rows=False)

    """
    Section2: Cleaning Columns
    """

    print(df['Place of Publication'])

    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))

    print(df['Place of Publication'])

    print(df['Date of Publication'])
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)

    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date
    print(df['Date of Publication'])

    """
    Section3: Filtering Rows
    """
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df = df.query('Date_of_Publication > 1866 and Place_of_Publication == "London"')
    print(df['Date_of_Publication'])
    print(df.columns)
    print()
    """
    Section4: Merging Two Dataframes
    """
    city_file = 'City.csv'
    df_city = pd.read_csv(city_file)

    df = pd.merge(df, df_city, how='left', left_on='Place_of_Publication', right_on='City')

    # gb_df is a groupby object that contains information about the groups. It is not a dataframe.
    gb_df = df.groupby(['Country'], as_index=False)

    df = gb_df['Identifier'].count()
    print_dataframe(df)

