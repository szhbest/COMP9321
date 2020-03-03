import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    """
    Section3: plot two scatter charts about the iris dataset.
    """
    iris_file = 'iris.csv'
    iris_df = pd.read_csv(iris_file)
    # print(iris_df)
    
    setosa = iris_df.query('species == "setosa"')
    virginica = iris_df.query('species == "virginica"')
    versicolor = iris_df.query('species == "versicolor"')

    ax1 = setosa.plot.scatter(x='sepal_length', y='sepal_width', label='setosa')
    ax1 = virginica.plot.scatter(x='sepal_length', y='sepal_width', label='virginica', c='r', ax=ax1)
    ax1 = versicolor.plot.scatter(x='sepal_length', y='sepal_width', label='versicolor', c='g', ax=ax1)

    ax2 = setosa.plot.scatter(x='petal_length', y='petal_width', label='setosa')
    ax2 = versicolor.plot.scatter(x='petal_length', y='petal_width', label='versicolor', color='g', ax=ax2)
    ax2 = virginica.plot.scatter(x='petal_length', y='petal_width', label='virginica', color='r', ax=ax2)
    
    plt.show()
