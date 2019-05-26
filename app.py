from flask import Flask, render_template, url_for, request
import pickle
import re


# create the flask object
app = Flask(__name__)

# routes go here
@app.route('/')
@app.route('/konmari')
def konmari():
    return render_template('konmari.html')
    

@app.route('/sparkjoy',methods=['POST','GET'])
def sparkjoy():
    
    with open('./konmari-vc-model.pickle', 'rb') as f:
        vcmodel = pickle.load(f)
    
    if request.method=='POST':
        result=request.form
        test_text = [result['test_text']]

        if result['model-type'] == 'model-type-vc':
            model = vcmodel
            modeltype = "vc"
        elif result['model-type'] == 'model-type-nb':
            model = vcmodel # haven't loaded in fitted naive bayes yet
            modeltype = "nb"
            # model = nbmodel
        else:
            model = vcmodel # haven't loaded in fitted logistic regression yet
            modeltype = "lr"
            # model = logregmodel
    
    # cleaned_test_text = [re.sub("[^a-zA-Z]+"," ", test_text)]
    prediction = model.predict(test_text)
    if prediction == 1:
        result = "Sparks joy!"
    else:
        result = "Doesn't spark joy - are you a hoarder?!"
    prob_tidy = f"{round(model.predict_proba(test_text)[0][1]*100,0)}%"
        
    return render_template('sparkjoy.html', outcome=prediction, probs=prob_tidy, words=test_text[0], modeltype=modeltype)

# script initialization
if __name__ == '__main__':
    app.run(debug=True)
