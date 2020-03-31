import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle


def load_diet(diet_path, split_percentage):
    df = pd.read_csv(diet_path, index_col=0)

    df = shuffle(df)
    diet_x = df.drop('weight6weeks', axis=1).values
    diet_y = df['weight6weeks'].values

    split_point = int(len(diet_x) * split_percentage)
    diet_X_train = diet_x[:split_point]
    diet_y_train = diet_y[:split_point]
    diet_X_test = diet_x[split_point:]
    diet_y_test = diet_y[split_point:]

    return diet_X_train, diet_y_train, diet_X_test, diet_y_test


if __name__ == "__main__":
    diet_X_train, diet_y_train, diet_X_test, diet_y_test = load_diet("diet.csv", split_percentage=0.7)
    model = linear_model.LinearRegression()

    model.fit(diet_X_train, diet_y_train)
    y_pred = model.predict(diet_X_test)

    for i in range(len(diet_y_test)):
        print("Expected:", diet_y_test[i], "Predicted:", y_pred[i])

    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(diet_y_test, y_pred))
