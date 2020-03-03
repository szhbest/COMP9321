import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    """
    Section2: plot a bar chart about the iris dataset.
    """
    iris_file = 'iris.csv'
    iris_df = pd.read_csv(iris_file)

    iris_df_gb = iris_df.groupby(['species']).mean()
    print(iris_df_gb)
    # rot here is to rotate the index
    iris_df_gb.plot.bar(rot=0)
    plt.show()
