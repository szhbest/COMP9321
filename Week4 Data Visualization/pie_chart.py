import pandas as pd
import matplotlib.pyplot as plt


def clean(df):
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda c: 'London' if 'London' in c else c.replace('-', ' '))
    return df


if __name__ == '__main__':
    book_file = 'Books.csv'
    book_df = pd.read_csv(book_file)

    """
    Section1: plot a pie chart of column named "Place of Publication"
    """
    cl_book_df = clean(book_df)
    pie_chart = cl_book_df['Place of Publication'].value_counts()
    pie_chart.plot.pie(subplots=True)
    plt.show()
