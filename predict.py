import pandas as pd
from catboost import CatBoostClassifier


def predict_model(selected_date):
    data = pd.read_csv('dataset/bookings_data.csv')

    # convert categorical variables to numerical format
    data['month'] = pd.to_datetime(data['month'], format='%B').dt.month
    data['season'] = data['season'].map({'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3})

    # extract additional features from date columns 
    data['day_of_week'] = pd.to_datetime(data[['year', 'month', 'day']]).dt.dayofweek 
    from sklearn.model_selection import train_test_split 
    from sklearn.metrics import mean_squared_error, r2_score

    # split the data into training and testing sets 
    X = data[['year', 'month', 'day', 'season', 'day_of_week']] 
    y = data['bookings']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # catboost 
    model = CatBoostClassifier(iterations=100) 

    # training time 
    model.fit(X_train, y_train) 
    
    # make predictions 
    desired_date = selected_date
    prediction = model.predict(desired_date)

    # take out [] from the prediction
    bookings = str(prediction).strip('[]')
    
    # return the predicted bookings
    return bookings
