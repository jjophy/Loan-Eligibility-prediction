from flask import Blueprint,render_template,request
import pickle
import numpy as np
import sklearn
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from models import db, UserDetails

predict_view = Blueprint('prediction', __name__, template_folder="templates")
model = pickle.load(open('model.pkl', 'rb')) # loading the trained model

@predict_view.route('/prediction.enter_details') ## for entering details
def enter_details():
    return render_template('predict.html')

@predict_view.route('/prediction.predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    print(int_features)
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    for k, v in zip(request.form.keys(), request.form.values()):
        if k == 'Gender':
            gender = 'male' if v == '1' else 'female'

        elif k == 'married':
            married = 'yes' if v == '1' else 'no'

        elif k == 'dependents':
            dependents = request.form['dependents']

        elif k == 'education':
            education = 'graduate' if v == '1' else 'not graduate'

        elif k == 'self_employed':
            self_employed = 'yes' if v == '1' else 'no'

        elif k == 'applicantincome':
            applicantincome = request.form['applicantincome']

        elif k == 'coapplicantincome':
            coapplicantincome = request.form['coapplicantincome']

        elif k == 'loanamount':
            loanamount = request.form['loanamount']

        elif k == 'loan_amount_term':
            loan_amount_term = request.form['loan_amount_term']

        elif k == 'credit_history':
            credit_history = 'yes' if v == '1' else 'no'

        elif k == 'property_area':
            if v == '0' :
                property_area = 'rural'
            elif v == '1' :
                property_area = 'urban'
            elif v == '2' :
                property_area = 'semiurban'

    applicationStatus = 'Approved' if prediction[0] == 1 else 'Not Approved'


    user_details = UserDetails(user_id=current_user.username,gender=gender,married=married,dependents=dependents,
               education=education,self_employed=self_employed,applicantincome=applicantincome,
               coapplicantincome=coapplicantincome,loanamount=loanamount,loan_amount_term=loan_amount_term,
                               credit_history=credit_history,property_area=property_area,
                               applicationStatus=applicationStatus)

    db.session.add(user_details)
    #try:
        #print("in try block")
    db.session.commit()

        if prediction==0:
            return render_template('predict.html', prediction_text='Sorry:( you are not eligible for the loan ')
        else:
            return render_template('predict.html', prediction_text='Congrats!! you are eligible for the loan')
    # except IntegrityError as err:
    #     db.session.rollback()
    #     if "UNIQUE constraint failed: user_details.user_id" in str(err):
    #         return False, "error, username already exists (%s)" % current_user.username
    #     elif "FOREIGN KEY constraint failed" in str(err):
    #         return False, "user does not exist"
    #     else:
    #         return False, "unknown error adding user details"