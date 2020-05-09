import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

studentid = os.path.basename(sys.modules[__name__].__file__)


#################################################
# Your personal methods can be here ...
#################################################


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    m_df = pd.read_csv(movies)
    c_df = pd.read_csv(credits)
    df1 = pd.merge(c_df, m_df, how='inner', left_on='id', right_on='id')
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    cols2keep = {'id', 'title', 'popularity', 'cast', 'crew',
                 'budget', 'genres', 'original_language', 'production_companies',
                 'production_countries', 'release_date', 'revenue', 'runtime',
                 'spoken_languages', 'vote_average', 'vote_count'}
    all_cols = set(df1.columns)
    col2drop = list(all_cols - cols2keep)
    df2 = df1.drop(col2drop, axis=1)
    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3 = df2.set_index('id')
    #################################################

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    rid_with_budget_0 = []
    for index, row in df3.iterrows():
        if row['budget'] == 0:
            rid_with_budget_0.append(index)
    df4 = df3.drop(rid_with_budget_0)
    #################################################

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df5 = df4
    df5['success_impact'] = (df4['revenue'] - df4['budget']) / df4['budget']
    #################################################

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    maximum = df5['popularity'].max()
    minimum = df5['popularity'].min()
    df6 = df5
    df6['popularity'] = df5[['popularity']].apply(
        lambda x: 100 * (x - minimum) / (maximum - minimum))
    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df7 = df6
    df7['popularity'] = df7['popularity'].astype('int16')
    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    def clean_cast(s):
        new_list = eval(s)
        name_list = []
        for sub_dict in new_list:
            name_list.append(sub_dict['character'])
        return ', '.join(c for c in sorted(name_list))
    df8 = df7
    df8['cast'] = df8['cast'].apply(clean_cast)
    #################################################

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    #################################################
    # Your code goes here ...
    char_dict = {}
    for index, row in df8.iterrows():
        temp = row['cast'].split(',')
        char_dict[index] = len(temp)
    top10 = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    movies = [df8['title'][rid] for rid, num in top10]
    #################################################

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df8['release_date'] = pd.to_datetime(df8['release_date'], dayfirst=True)
    df10 = df8.sort_values(by=['release_date'], ascending=False)
    #################################################

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    genres = df10['genres']

    def get_genres(s):
        new_list = eval(s)
        genre_list = []
        for sub_dict in new_list:
            genre_list.append(sub_dict['name'])
        return genre_list

    genres = genres.apply(get_genres)
    temp = pd.Series(data=[j for i in genres for j in i])
    pie_chart = temp.value_counts()
    percent = [100 * i / pie_chart.sum() for i in pie_chart]
    # print(percent)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(pie_chart.index, percent)]
    # print(labels)
    ax_pie = pie_chart.plot.pie(labels=['' for k in pie_chart], title='Genres')
    ax_pie.set_ylabel('')
    plt.legend(labels=labels, loc='lower right', bbox_to_anchor=(0, 0), fontsize=6)
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    production_countries = df10['production_countries']

    def get_countries(s):
        new_list = eval(s)
        country_list = []
        for sub_dict in new_list:
            country_list.append(sub_dict['name'])
        return country_list

    countries = production_countries.apply(get_countries)
    temp = pd.Series(data=[j for i in countries for j in i])
    bar_chart = temp.value_counts()
    bar_chart = bar_chart.sort_index(ascending=True)
    # print(bar_chart)
    fig, ax = plt.subplots()
    ax = bar_chart.plot.bar(title='Production Country', fontsize=5)
    #################################################

    plt.savefig("{}-Q12.png".format(studentid), bbox_inches='tight')


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    vote_average = df10['vote_average']
    success_impact = df10['success_impact']
    language = df10['original_language']
    scatter_chart = pd.DataFrame({'vote_average': vote_average, 'success_impact': success_impact,
                                  'language': language})
    groups = scatter_chart.groupby('language')

    fig, ax = plt.subplots()
    language_type = list(set(language))

    import numpy as np
    import matplotlib.cm as cm

    colors = cm.rainbow(np.linspace(0, 1, len(language_type)))
    i = 0
    for name, group in groups:
        ax = group.plot.scatter(x='vote_average', y='success_impact', ax=ax, label=name, color=[colors[i]])
        i += 1
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=8, ncol=2)
    plt.title('vote_average vs success_impact')
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)
