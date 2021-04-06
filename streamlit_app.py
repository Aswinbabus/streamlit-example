# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 08:58:48 2021

@author: aswin babu
"""

import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import pickle
from bokeh.models.widgets import Div
st.sidebar.markdown("# Loan Prediction")
st.sidebar.write("Click here to open Loan Prediction Application")
image = Image.open('loan.jpg')
st.image(image)
if st.sidebar.button('Predict Loan'):
    js = "window.open('https://www.streamlit.io/')"  
    js = "window.location.href = 'https://www.streamlit.io/'"  
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
st.markdown("<h1 style='text-align: center;'>Various Algorithms and Its Accuracy</h1>", unsafe_allow_html=True)
df=pd.DataFrame({
    
    'Algorithm': ["Logistic Regression"," Decision Tree","SVM","Random Forest","XGBoost"],
    'Accuracy': [0.806331,0.671589,0.808421,0.783191,0.806316]
})
st.table(df)
pickle_in = open('model.pkl', 'rb') 
model = pickle.load(pickle_in)
 

# defining the function which will make the prediction using the data which the user inputs 
def prediction(Gender, Married, ApplicantIncome,CoApplicantIncome,LoanAmount,Loan_Amount_Term,Property_Area,Education,Self_Employed,Dependents,Credit_History):   
 
    if Credit_History == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1  
     
    if Dependents == "3+":
        Dependents = "3"
    
         
 
    LoanAmount = LoanAmount * 1000
    Total_Income = ApplicantIncome + CoApplicantIncome
    
    
    if Total_Income == 0 :
        st.warning('Applicant Income Cannot be Zero')
        return
    if LoanAmount == 0 :
        st.warning('Loan Amount Cannot be Zero')
        return
    if Loan_Amount_Term == 0 :
        st.warning('Loan Amount Term Cannot be Zero')
        return
    
    EMI = LoanAmount / Loan_Amount_Term
    Balance_Income = Total_Income - EMI
    if Balance_Income < 0 :
        st.error('Your loan is Rejected')
        return
    Balance_Income_log = np.log(Balance_Income)
    dict = {
           'Gender': [Gender],
           'Married': [Married],
           'Balance_Income_log':[Balance_Income_log],
           'Credit_History':[Credit_History],
           'Property_Area':[Property_Area],
           'Education':[Education],
           'Self_Employed':[Self_Employed],
           'Dependents':[Dependents],
           'Loan_Amount_Term':[Loan_Amount_Term]
           }
    df = pd.DataFrame(dict)
    df_processed = pd.get_dummies(df)
    ohe_col=['Loan_Amount_Term', 'Credit_History', 'Balance_Income_log',
       'Gender_Female', 'Gender_Male', 'Married_No', 'Married_Yes',
       'Dependents_3', 'Dependents_0', 'Dependents_1', 'Dependents_2',
       'Education_Graduate', 'Education_Not Graduate', 'Self_Employed_No',
       'Self_Employed_Yes', 'Property_Area_Rural', 'Property_Area_Semiurban',
       'Property_Area_Urban' ]
    newdict={}
    for i in ohe_col:
        if i in df_processed.columns:
            newdict[i]=df_processed[i].values
        else:
            newdict[i]=0
    newdf=pd.DataFrame(newdict)
    y_pred=model.predict(newdf)
    prediction=(y_pred>0.58)
     
    if prediction == 0:
        st.error('Your loan is Rejected') 
    else:
        st.success('Your loan is Approved')  
      
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Loan Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    Gender = st.selectbox('Gender',("Male","Female"))
    Married = st.selectbox('Marital Status',("Unmarried","Married")) 
    ApplicantIncome = st.number_input("Applicants monthly income") 
    CoApplicantIncome = st.number_input("CoApplicants monthly income") 
    LoanAmount = st.number_input("Loan Amount in Thousands")
    Loan_Amount_Term = st.number_input("Loan Amount Term")
    Property_Area = st.selectbox('Property Area',("Rural","Urban","Semiurban")) 
    Education = st.selectbox('Education',("Graduate","Not Graduate"))
    Self_Employed = st.selectbox('Self-Employed',("Yes","No"))
    Dependents = st.selectbox('Dependents',("0","1","2","3+"))
    Credit_History = st.selectbox('Credit_History',("Unclear Debts","No Unclear Debts"))
    result =""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(Gender, Married, ApplicantIncome,CoApplicantIncome,LoanAmount,Loan_Amount_Term,Property_Area,Education,Self_Employed,Dependents,Credit_History) 
     
if __name__=='__main__': 
    main()
