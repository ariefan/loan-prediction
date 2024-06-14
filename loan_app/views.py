import os
from django.shortcuts import render
import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.views import View
import joblib
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Load the trained model (ensure the model file path is correct)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'loan_app', 'ml_model.pkl')
print(MODEL_PATH)
model = joblib.load(MODEL_PATH)

@method_decorator(csrf_exempt, name='dispatch')
class PredictLoan(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        
        # Example of accessing JSON data (modify as per your JSON structure)
        gender = float(data.get('Gender'))
        married = float(data.get('Married'))
        dependents = float(data.get('Dependents'))
        education = int(data.get('Education'))
        self_employed = float(data.get('Self_Employed'))
        applicant_income = float(data.get('ApplicantIncome'))
        coapplicant_income = float(data.get('CoapplicantIncome'))
        loan_amount = float(data.get('LoanAmount'))
        loan_amount_term = float(data.get('Loan_Amount_Term'))
        credit_history = float(data.get('Credit_History'))
        property_area = int(data.get('Property_Area'))

        # Create a DataFrame for the input data
        data = pd.DataFrame({
            'Gender': [gender],
            'Married': [married],
            'Dependents': [dependents],
            'Education': [education],
            'Self_Employed': [self_employed],
            'ApplicantIncome': [applicant_income],
            'CoapplicantIncome': [coapplicant_income],
            'LoanAmount': [loan_amount],
            'Loan_Amount_Term': [loan_amount_term],
            'Credit_History': [credit_history],
            'Property_Area': [property_area]
        })

        # Make prediction
        prediction = model.predict(data)
        result = {'prediction': int(prediction[0])}

        return JsonResponse(result, safe=False)
