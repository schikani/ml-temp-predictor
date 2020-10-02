import pandas as pd
from joblib import load
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

# Here we define some of the GLOBAL variables which will be changed and used later
PREDICTION_DAY = ""
MEAN_PREDICTED_TEMP = 0
MEDIAN_PREDICTED_TEMP = 0

try:
    # load_input_data
    data_mean = pd.read_csv('data/data_mean.csv')
    data_median = pd.read_csv('data/data_median.csv')

    # load the model
    clf = load('data/trained_model.joblib')

# Here with an exception of FileNotFoundError we: 
# import data_preprocessing to get the trained model after going throungh data manipulation in data_preprocessing.py.
except FileNotFoundError:
    import data_preprocessing

    # load_input_data
    data_mean = pd.read_csv('data/data_mean.csv')
    data_median = pd.read_csv('data/data_median.csv')

    # load the model
    clf = load('data/trained_model.joblib')


# Making a function for prediction. Here we also use Python's 'datetime.datetime.strptime()' and
# 'datetime.datetime.strftime()' to get a Month name and corresponding date.
def make_prediction(model, month, day):
    _translate = QtCore.QCoreApplication.translate

    mean_input = pd.DataFrame(data_mean.query(f'month=={month}').query(f'day=={day}').mean())

    median_input = pd.DataFrame(data_median.query(f'month=={month}').query(f'day=={day}').median())

    prediction_day = datetime.datetime.strptime(str(month) + '/' + str(day), "%m/%d")

    mean_p = float(model.predict(mean_input.T))
    median_p = float(model.predict(median_input.T))

    # Change Global values which will be used in the GUI
    global PREDICTION_DAY, MEAN_PREDICTED_TEMP, MEDIAN_PREDICTED_TEMP
    PREDICTION_DAY = f"Predictions for {prediction_day.strftime('%B %d')}"
    MEAN_PREDICTED_TEMP = round(mean_p, 2)
    MEDIAN_PREDICTED_TEMP = round(median_p, 2)


# GUI related code.
# ______________________________________________________________________________________________________________________

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(602, 325)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 90, 581, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.mean_predicted_temp = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.mean_predicted_temp.setFont(font)
        self.mean_predicted_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.mean_predicted_temp.setObjectName("mean_predicted_temp")
        self.gridLayout.addWidget(self.mean_predicted_temp, 1, 0, 1, 1)
        self.median_number = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.median_number.setFont(font)
        self.median_number.setMode(QtWidgets.QLCDNumber.Dec)
        self.median_number.setProperty("value", 0.0)
        self.median_number.setProperty("intValue", 0)
        self.median_number.setObjectName("median_number")
        self.gridLayout.addWidget(self.median_number, 2, 1, 1, 1)
        self.mean_number = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.mean_number.setFont(font)
        self.mean_number.setObjectName("mean_number")
        self.gridLayout.addWidget(self.mean_number, 1, 1, 1, 1)
        self.median_predicted_temp = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.median_predicted_temp.setFont(font)
        self.median_predicted_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.median_predicted_temp.setObjectName("median_predicted_temp")
        self.gridLayout.addWidget(self.median_predicted_temp, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(32)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(32)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.predict = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(16)
        self.predict.setFont(font)
        self.predict.setObjectName("predict")
        self.gridLayout.addWidget(self.predict, 5, 2, 1, 1)
        self.day_month = QtWidgets.QDateEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(22)
        self.day_month.setFont(font)
        self.day_month.setAlignment(QtCore.Qt.AlignCenter)
        self.day_month.setObjectName("day_month")
        self.gridLayout.addWidget(self.day_month, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.heading = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(26)
        self.heading.setFont(font)
        self.heading.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.heading.setLineWidth(0)
        self.heading.setScaledContents(False)
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
        self.heading.setObjectName("heading")
        self.verticalLayout.addWidget(self.heading)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # self.make_prediction()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ML Temp Predictor"))

        self.heading.setText(_translate("Form", "Go on make some Predictions!"))
        self.mean_predicted_temp.setText(_translate("Form", "Mean predicted temperature"))
        self.median_predicted_temp.setText(_translate("Form", "Median predicted temperature"))
        self.label_5.setText(_translate("Form", "°C"))
        self.label_6.setText(_translate("Form", "°C"))
        self.label.setText(_translate("Form", "Please enter Day and Month in DD/MM format"))
        self.day_month.setDisplayFormat(_translate("Form", "dd/MM"))
        self.day_month.setDate(QtCore.QDate())

        # Changing the values with the predict button pressed.
        self.predict.setText(_translate("Form", "Predict"))
        self.predict.clicked.connect(lambda: make_prediction(model=clf, month=self.day_month.date().month(), day=self.day_month.date().day()))
        self.predict.clicked.connect(lambda: self.heading.setText(_translate("Form", PREDICTION_DAY)))
        self.predict.clicked.connect(lambda: self.mean_number.display(MEAN_PREDICTED_TEMP))
        self.predict.clicked.connect(lambda: self.median_number.display(MEDIAN_PREDICTED_TEMP))

# ______________________________________________________________________________________________________________________


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
