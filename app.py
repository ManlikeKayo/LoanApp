# Steps in building streamlit web app
# 1. Importing the required libraries
# 2. Load your pickle files 
# 3. Write a prediction function  def
# 4. build the streamlit interface
# 5 setup your prediction button

# 1. Importing the required libraries
import pickle
import numpy as np
import streamlit as st

# 2. Load your pickle files 
### loading the pickle files 
loaded_model = pickle.load(open('loan_model.sav', 'rb'))  ## rb means read binary mode
loaded_scaler = pickle.load(open('scaler.sav', 'rb'))  ## rb means read binary mode

# 3. Write a prediction function  def
def loan_prediction(input_data):
    
    # changing the input data to a numpy array and reshaping it
    convert_data_to_numpy = np.array(input_data).reshape(1, -1)

    # standardize the input data using the same scaler used for training
    std_data = loaded_scaler.transform(convert_data_to_numpy)     
     # Generate the prediction from the loaded model
    prediction = loaded_model.predict(std_data)[0]

    ### The prediction
    if prediction == 0:
        return('You are not eligible for the loan')
    else:
        return('You are eligible for the loan')
    

# 4. Build the streamlit interface

## check the total number of your data columns to be able to determing your interface structure
## 3 columns

def main():
    # My loan app title
    st.title('Loan Predictive System')
    
    # using my 3 columns structure
    col1, col2, col3 = st.columns(3)
    #-------------------------------- Column 1
    with col1:
        gender = st.selectbox('Gender', options=['Male', 'Female'])
        married = st.selectbox('Married', options=['No', 'Yes'])
        dependents = st.selectbox('Dependents', options=['0', '1', '2', '3+'])
        education = st.selectbox('Education', options=['Graduate', 'Not Graduate'])
    
    #-------------------------------- Column 2
    with col2:
        self_employed = st.selectbox('Self_Employed', options=['Yes', 'No'])
        applicant_income = st.number_input('ApplicantIncome', min_value=0, value=0)
        Coapplicant_income = st.number_input('CoapplicantIncome', min_value=0, value=0)
        loan_amount = st.number_input('LoanAmount', min_value=0, value=0)

    #------------------------------------Coulmn 3 
    with col3:
        loan_amount_term = st.number_input('Loan_Amount_Term', min_value=1, max_value=360)
        credit_history = st.selectbox('Credit_History', options=['1 (Good)', '0 (Bad)'])
        property_area = st.selectbox('Property_Area',options=['Rural', 'Semiurban', 'Urban'])
        

    # 5 setup your prediction button
    if st.button('Loan_Predictive_System'):
        try:
            gender_value = 1 if gender == 'Male' else 0
            married_value = 1 if married == 'Yes' else 0
            dependents_value = 3 if dependents == '3+' else int(dependents)
            education_value = 1 if education == 'Graduate' else 0
            self_employed_value = 1 if self_employed == 'Yes' else 0
            credit_history_value = 1 if credit_history == '1 (Good)' else 0
            ##### handling property area 
            rural_value = 1 if property_area == 'Rural' else 0
            semiurban_value = 1 if property_area == 'Semiurban' else 0
            srban_value = 1 if property_area == 'Urban' else 0
            
            ## putting all my column names  together
            input_data = [gender_value, married_value, dependents_value, education_value, self_employed_value, applicant_income, Coapplicant_income, 
                         loan_amount, loan_amount_term, credit_history_value, rural_value, semiurban_value, srban_value]

            #call the step 3 prediction function
            result = loan_prediction(input_data)
            
            ### Error hadling output
            if 'not' in result:
                st.success(result)
            else:
                st.error(result)
        except ValueError as ex:
            st.error(f'Value Error (Please Enter a Valid Value) {ex}')



### to run the app 
if __name__ == '__main__':
    main()