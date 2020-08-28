import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from joblib import dump

##-------------------------------------------------------------------------------------------------------
# Clean the data

# Import data and make the dt_iso column to pandas date format using 'parse_dates'
# Here add your file name in "data/your-file-name.csv"
df = pd.read_csv("data/opole-weather-data.csv", parse_dates=['dt_iso'])

# Drop the missing values which has missing values in every row.
df.drop("sea_level", axis=1, inplace=True)
df.drop("grnd_level", axis=1, inplace=True)
df.drop("rain_3h", axis=1, inplace=True)
df.drop("snow_3h", axis=1, inplace=True)

# Drop other columns which aren't important
df.drop("lat", axis=1, inplace=True)
df.drop("lon", axis=1, inplace=True)
df.drop("dt", axis=1, inplace=True)
# Fill rain_1h and snow_1h missing values with 0

for label, content in df.items():
    if pd.isnull(content).sum():
        df[label] = content.fillna(0)

# Turn categorical values into numbers.
for label, content in df.items():
    if pd.api.types.is_object_dtype(content):
        # Here we add +1 because Categorical codes assign -1 in case of missing values)
        df[label] = pd.Categorical(content).codes + 1

# Make "month", "day" columns from "dt_iso" column
df["month"] = df.dt_iso.dt.month
df["day"] = df.dt_iso.dt.day

# Now drop "dt_iso" column as we don't need it anymore
df.drop("dt_iso", axis=1, inplace=True)

# Save the new dataframe
df.to_csv('data/cleaned_data.csv', index=False)

##-------------------------------------------------------------------------------------------------------
# Train and test the model

# Load the cleaned data
df = pd.read_csv('data/cleaned_data.csv')

# Split data into Training and Test sets.
df_train = df[:328473]  # 90% of total data
df_test = df[328473:]  # 10% of total data

# Make X_train, y_train, X_test, y_test

# X_train, y_train
X_train = df_train.drop("temp", axis=1)
y_train = df_train["temp"]

# X_test, y_test
X_test = df_test.drop("temp", axis=1)
y_test = df_test["temp"]


# Create function to evaluate model on few different levels
def show_scores(model):
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    scores = {"Training MAE": mean_absolute_error(y_train, train_preds),
              "Test MAE": mean_absolute_error(y_test, test_preds),
              "Training R^2": r2_score(y_train, train_preds),
              "Test R^2": r2_score(y_test, test_preds)}
    return scores


# Here we try to find the best hyperparameters on 10000 samples to reduce the compute power needed for doing the same in the whole dataset.
# If you want to find the best hyperparameter by your own, uncomment below lines.
# Note: It can take a lot of time! depending on you compute power.

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # Different RandomForestRegressor hyperparameters
# rf_grid = {"n_estimators": np.arange(10, 100, 10),
#            "max_depth": [None, 3, 5, 10],
#            "min_samples_split": np.arange(2, 20, 2),
#            "min_samples_leaf": np.arange(1, 20, 2),
#            "max_features": [0.5, 1, "sqrt", "auto"],
#            "max_samples": [10000]}
#
# # Instantiate RandomizedSearchCV model
# rs_model = RandomizedSearchCV(RandomForestRegressor(n_jobs=-1, random_state=42),
#                               param_distributions=rf_grid,
#                               cv=5,
#                               n_iter=50,
#                               verbose=True)
#
# # Fit the RandomizedSearchCV model
# rs_model.fit(X_train, y_train)
#
# # Find the best model hyperparameters
# print(f"The best hyperparameters for this model are:{rs_model.best_params_}")
#
# # Evaluate the RandomizedSearch model
# show_scores(rs_model)

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# I found the best hyperparameters for my model by running the above code. It goes as below
# Now we train the whole dataset with most ideal hyperparameters found in 10000 samples.
ideal_model = RandomForestRegressor(n_estimators=70,
                                    min_samples_split=6,
                                    min_samples_leaf=1,
                                    max_features=0.5,
                                    max_depth=10,
                                    n_jobs=-1,
                                    max_samples=None,
                                    random_state=42)

# Fit the ideal model
ideal_model.fit(X_train, y_train)

# Scores for ideal model (trained on all the data)
show_scores(ideal_model)

# Save the ideal_model to a joblib file to use it later.
dump(ideal_model, 'data/opole_weather_prediction.joblib')

##-------------------------------------------------------------------------------------------------------
# Make the input data ready for our model.

# Import the cleaned dataset
df = pd.read_csv('data/cleaned_data.csv')

# Drop 'temp' column as this the value we are predicting
df.drop('temp', axis=1, inplace=True)

# Lets make our data ready!
# Here we make mean and median of all the columns as per 'month' and 'day'
data_mean = df.groupby(['month', 'day']).mean()
data_median = df.groupby(['month', 'day']).median()

# Now we save the new 'mean' and 'median' DataFrame to csv files
data_mean.reset_index().to_csv('data/data_mean.csv', index=False)
data_median.reset_index().to_csv('data/data_median.csv', index=False)

##-------------------------------------------------------------------------------------------------------
