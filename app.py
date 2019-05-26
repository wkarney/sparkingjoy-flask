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
    
    if request.method=='POST':
        result=request.form
        test_text = [result['test_text']]

        if result['model-type'] == 'vc':
            with open('./pickled-models/sparkingjoy-model-vc.pickle', 'rb') as f:
                model = pickle.load(f)
            modeltype = "vc"
        elif result['model-type'] == 'nb':
            with open('./pickled-models/sparkingjoy-model-nb.pickle', 'rb') as f:
                model = pickle.load(f)
            modeltype = "nb"
        else:
            with open('./pickled-models/sparkingjoy-model-logreg.pickle', 'rb') as f:
                model = pickle.load(f)
            modeltype = "lr"
    
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
