import pandas as pd
from catboost import CatBoostRegressor


def predict_model(selected_date):
    data = pd.read_csv('dataset/bookings_per_year_month_day_season_adults.csv')

    # convert categorical variables to numerical format
    data['month'] = pd.to_datetime(data['month'], format='%B').dt.month
    data['season'] = data['season'].map({'Spring': 0, 'Summer': 1, 'Fall': 2, 'Winter': 3})

    # extract additional features from date columns 
    data['day_of_week'] = pd.to_datetime(data[['year', 'month', 'day']]).dt.dayofweek 
    from sklearn.model_selection import train_test_split 
    from sklearn.metrics import mean_absolute_error, r2_score

    # split the data into training and testing sets 
    X = data[['year', 'month', 'day', 'season', 'adults', 'day_of_week']] 
    y = data['bookings']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # catboost 
    model = CatBoostRegressor(n_estimators=100, learning_rate=0.1, depth=6, random_seed=5, l2_leaf_reg=9)

    # training time 
    model.fit(X_train, y_train) 
    
    # make predictions 
    desired_date = selected_date
    prediction = model.predict(desired_date)
   
   # process the prediction as int
    prediction = prediction.astype('int32')

    # take out [] from the prediction
    bookings = str(prediction).strip("[]")
    
    # return the predicted bookings
    return bookings
