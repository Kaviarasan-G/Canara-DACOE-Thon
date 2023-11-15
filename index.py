import numpy as np
from flask import Flask, request, render_template
import joblib
import pandas as pd
import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email1 import email_alert
#Create an app object using the Flask class. 
app = Flask(__name__)

#Load the trained model. (Pickle file)
#model = pickle.load(open('models/model.pkl', 'rb'))

#Define the route to be home. 
#The decorator below links the relative route of the URL to the function it is decorating.
#Here, home function is with '/', our root directory. 
#Running the app sends us to index.html.
#Note that render_template means it looks for the file in the templates folder. 

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def home():
    return render_template('index.html')

#You can use the methods argument of the route() decorator to handle different HTTP methods.
#GET: A GET message is send, and the server returns data
#POST: Used to send HTML form data to the server.
#Add Post method to the decorator to allow for form submission. 
#Redirect to /predict page with the output
@app.route('/predict',methods=['POST'])
def predict():
    df=pd.read_excel(r"C:\Users\PowerBI-In22labs\Downloads\Hackathon_Fraud_Prevention (2)\Hackathon_Fraud_Prevention\dump.xlsx")
    cc_num = request.form['CUSTOMER_ID']
    amt=request.form['AMOUNT']
    category=request.form['CATEGORY']
    CC_ID=df['cc_num']
    model_predict=joblib.load(r"C:\Users\PowerBI-In22labs\Downloads\Hackathon_Fraud_Prevention (2)\Hackathon_Fraud_Prevention\random_forest_pipeline.pkl")
    current_datetime = dt.datetime.now()
    print(current_datetime)
    for i in CC_ID:
        if i==int(cc_num):
           df_final=df[df['cc_num']==i] 
           df_final['amt']=amt
           df_final['category']=category
           df_final['age'] = dt.date.today().year - pd.to_datetime(df_final['dob']).dt.year
           df_final.drop(['dob'],inplace=True,axis=1)
           df_final['hour'] = current_datetime.hour
           df_final['day']=current_datetime.weekday() + 1
           df_final['month']=current_datetime.month
           predictions = model_predict.predict(df_final)
           if predictions==1:
               email_alert()
               return render_template('index.html', prediction_text='fraud') 
           else:
               return render_template('index.html', prediction_text='not_fraud')

             

             
     #Convert string inputs to float.
    #features = [np.array(int_features)]  #Convert to the form [[a, b]] for input to the model
    #prediction = model.predict(features)  # features Must be in the form [[a, b]]

    #output = round(prediction[0], 2)

    #return render_template('index.html', prediction_text='Percent with heart disease is {}'.format(output))
    #print(int_features)

#When the Python interpreter reads a source file, it first defines a few special variables. 
#For now, we care about the __name__ variable.
#If we execute our code in the main program, like in our case here, it assigns
# __main__ as the name (__name__). 
#So if we want to run our code right here, we can check if __name__ == __main__
#if so, execute it here. 
#If we import this file (module) to another file then __name__ == app (which is the name of this python file).

if __name__ == "__main__":
    app.run()