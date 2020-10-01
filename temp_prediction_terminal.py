import pandas as pd
from joblib import load
import datetime

try:
    # load_input_data
    data_mean = pd.read_csv('data/data_mean.csv')
    data_median = pd.read_csv('data/data_median.csv')

    # load the model
    clf = load('data/trained_model.joblib')

except FileNotFoundError:
    import data_preprocessing

    # load_input_data
    data_mean = pd.read_csv('data/data_mean.csv')
    data_median = pd.read_csv('data/data_median.csv')

    # load the model
    clf = load('data/trained_model.joblib')


# Define months with a dictionary


# Making a function for prediction. Here we also use Python's 'datetime.datetime.strptime()' and
# 'datetime.datetime.strftime()' to get a Month name and corresponding date.
def make_prediction(model, month, day):
    mean_input = pd.DataFrame(data_mean.query(f'month=={month}').query(f'day=={day}').mean())
    # mean_temp_min = round(float(mean_input.T["temp_min"]), 2)
    # mean_temp_max = round(float(mean_input.T["temp_max"]), 2)

    median_input = pd.DataFrame(data_median.query(f'month=={month}').query(f'day=={day}').median())
    # median_temp_min = round(float(median_input.T["temp_min"]), 2)
    # median_temp_max = round(float(median_input.T["temp_max"]), 2)

    prediction_day = datetime.datetime.strptime(str(month) + '/' + str(day), "%m/%d")

    try:
        mean_p = float(model.predict(mean_input.T))
        median_p = float(model.predict(median_input.T))
        print("*"*35)
        print(f"    Predictions for {prediction_day.strftime('%B %d')}")
        print("*"*35)
        print(f"Mean predicted temperature: {str(round(mean_p, 2))}°C")
        print("~"*40)
        print(f"Median predicted temperature: {str(round(median_p, 2))}°C")
        print("~"*40)


    except ValueError:
        print("The combination of month and date is incorrect! Please type a correct month-day combination")
        ask(clf)


def ask(model):
    while True:
        try:
            month = int(input("Please select a month (format: mm)\n"))

            if month not in range(1, 13):
                print("Incorrect input! Please enter a month number in 'mm' format between(1-12)")
                continue
            if month in range(1, 13):
                break

        except ValueError:
            print("Incorrect input! Please enter a month number!")
            continue

    while True:
        try:
            day = int(input("Please select a day (format: dd)\n"))

            if day not in range(1, 32):
                print("Incorrect input! Please enter a day number in 'dd' format between(1-31)")
                continue
            if day in range(1, 32):
                break

        except ValueError:
            print("Incorrect input! Please enter a day number!")
            continue

    make_prediction(model=model, month=month, day=day)


if __name__ == '__main__':
    ask(clf)
