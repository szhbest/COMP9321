import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt


if __name__ == '__main__':
    c_file = 'credits.csv'
    m_file = 'movies.csv'
    c_df = pd.read_csv(c_file)
    m_df = pd.read_csv(m_file)

    """
    q1: merge two datasets based on "id" columns
    """
    merge_df = pd.merge(c_df, m_df, how='inner', left_on='id', right_on='id')
    # print(merge_df.shape, c_df.shape, m_df.shape)

    """
    q2: remove irrelevant columns
    """
    cols2keep = {'id', 'title', 'popularity', 'cast', 'crew',
                 'budget', 'genres', 'original_language', 'production_companies',
                 'production_countries', 'release_date', 'revenue', 'runtime',
                 'spoken_languages', 'vote_average', 'vote_count'}
    all_cols = set(merge_df.columns)
    col2drop = list(all_cols - cols2keep)
    merge_df.drop(col2drop, inplace=True, axis=1)
    # print(merge_df)

    """
    q3: set the index of the resultant dataframe as 'id'
    """
    merge_df.set_index('id', inplace=True)
    # print(merge_df)

    """
    q4: drop all rows where budget is 0
    """
    rid_with_budget_0 = []
    for index, row in merge_df.iterrows():
        if row['budget'] == 0:
            rid_with_budget_0.append(index)
    merge_df.drop(rid_with_budget_0, inplace=True)
    # print(merge_df)

    """
    q5: add a new column defined by "(revenue - budget)/budget", name it "success_impact"
    """
    merge_df['success_impact'] = (merge_df['revenue'] - merge_df['budget']) / merge_df['budget']
    # print(merge_df)

    """
    q6: normalize the "popularity" by scaling between 0 to 100.(float number)
    """
    maximum = merge_df['popularity'].max()
    minimum = merge_df['popularity'].min()
    merge_df['popularity'] = merge_df[['popularity']].apply(
        lambda x: 100 * (x - minimum) / (maximum - minimum))
    # print(merge_df['popularity'])

    """
    q7: change the data type of the "popularity" column to (int16)
    """
    merge_df['popularity'] = merge_df['popularity'].astype('int16')
    # print(merge_df['popularity'])

    """
    q8: clean the "cast" column 
    """
    def clean_cast(s):
        new_list = eval(s)
        name_list = []
        for sub_dict in new_list:
            name_list.append(sub_dict['character'])
        return ', '.join(c for c in sorted(name_list))
    merge_df['cast'] = merge_df['cast'].apply(clean_cast)
    # print(merge_df['cast'])

    """
    q9: return a list containing the names of the top 10 movies according to the number of movie characters
    """
    char_dict = {}
    for index, row in merge_df.iterrows():
        temp = row['cast'].split(',')
        char_dict[index] = len(temp)
    top10 = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_movie_list = [merge_df['title'][rid] for rid, num in top10]

    """
    q10: sort the dataframe by the release date
    """
    merge_df['release_date'] = pd.to_datetime(merge_df['release_date'], dayfirst=True)
    sort_merge_df = merge_df.sort_values(by=['release_date'], ascending=False)
    # print(sort_merge_df['release_date'].to_string())


    """
    q11:  Plot a pie chart, showing the distribution of genres in the dataset
    """
    genres = merge_df['genres']

    def get_genres(s):
        new_list = eval(s)
        genre_list = []
        for sub_dict in new_list:
            genre_list.append(sub_dict['name'])
        return genre_list

    genres = genres.apply(get_genres)
    temp = pd.Series(data=[j for i in genres for j in i])
    pie_chart = temp.value_counts()
    # print(pie_chart)
    percent = [100 * i / pie_chart.sum() for i in pie_chart]
    # print(percent)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(pie_chart.index, percent)]
    # print(labels)
    ax_pie = pie_chart.plot.pie(labels=['' for k in pie_chart], title='Genres', figsize=(7, 7))
    ax_pie.set_ylabel('')
    plt.legend(labels=labels, loc='lower right', bbox_to_anchor=(0, 0), fontsize=10)
    plt.show()

    """
    q12:  Plot a bar chart of the countries in which movies have been produced. 
          For each county you need to show the count of movies.
          Countries should be alphabetically sorted according to their names.
    """
    production_countries = merge_df['production_countries']

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
    bar_chart.plot.bar(fontsize=8)
    plt.title('Production Country')
    plt.show()

    """
    q13: Plot a scatter chart with x axis being "vote_average" and y axis being "success_impact".
          Ink bubbles based on the movie language (e.g, English, French); 
          In case of having multiple languages for the same movie, you are free to pick any one as you wish.
    """
    vote_average = merge_df['vote_average']
    success_impact = merge_df['success_impact']
    language = merge_df['original_language']
    # language = merge_df['spoken_languages'].apply(lambda x: eval(x)[0]['name'])
    scatter_chart = pd.DataFrame({'vote_average': vote_average, 'success_impact': success_impact,
                                  'language': language})
    groups = scatter_chart.groupby('language')

    fig, ax = plt.subplots()
    language_type = list(set(language))

    import numpy as np
    import matplotlib.cm as cm
    from matplotlib import font_manager

    # fontP = font_manager.FontProperties()
    # fontP.set_family(['SimHei', 'nanumgothic'])
    # fontP.set_size(8)

    colors = cm.rainbow(np.linspace(0, 1, len(language_type)))
    i = 0
    for name, group in groups:
        ax = group.plot.scatter(x='vote_average', y='success_impact', ax=ax, label=name, color=[colors[i]])
        i += 1
        # print(name)
    # to put the upper left corner of the legend to the upper left corner of the chart(based on (0, 1))
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=8, ncol=2)
    # plt.title('vote_average vs success_impact')
    # plt.show()
    # print(len(language_type))
    # print(scatter_chart)
    # print(scatter_chart.to_string())
