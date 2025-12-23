#from flask import Flask, render_template, request,redirect,url_for
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

import joblib
import numpy as np

app = Flask(__name__)




# Load models
crop_model=joblib.load("crop.pkl")
#with open("crop.pkl", "rb") as f:
#    crop_model = pickle.load(f)

soil_model=joblib.load('soil.pkl')
#with open("model_soil.pkl", "rb") as f:
#    soil_model = pickle.load(f)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/index", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/crop", methods=["GET", "POST"])
def crop():
    prediction = None
    if request.method == "POST":
        features = np.array([[
            float(request.form["N"]),
            float(request.form["P"]),
            float(request.form["K"]),
            float(request.form["temperature"]),
            float(request.form["humidity"]),
            float(request.form["ph"]),
            float(request.form["rainfall"])
        ]])
        prediction = crop_model.predict(features)[0]


    return render_template("crop.html", prediction=prediction)

@app.route("/soil", methods=["GET", "POST"])
def soil():
    prediction = None
    if request.method == "POST":
        features = np.array([[
            float(request.form["N"]),
            float(request.form["P"]),
            float(request.form["K"]),
            float(request.form["ph"])
        ]])
        prediction = soil_model.predict(features)[0]

    return render_template("soil.html", prediction=prediction)




#mysql connection 
app.secret_key="secrete123"
#mysql configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shankar'
app.config['MYSQL_DB'] = 'feedback'

mysql= MySQL(app)

#feedback form 
@app.route('/user_feedback',methods=['POST'])
def feedback():
    if request.method=='POST':
        name=request.form.get('name')
        mo_no=request.form.get('mo_no')
        message=request.form.get('message')

        cur=mysql.connection.cursor()
        cur.execute(
            "Insert into farmer_details(name,mo_no,message) values(%s , %s, %s)",(name,mo_no,message)

        )
        mysql.connection.commit() 
        cur.close()
        flash("Feedback submitted successfully! 🌾", "success")

        #return redirect(url_for('feedback'))
    #return render_template('feedback.html',messages=messages)
    #return redirect(url_for('index'))
    

    #return render_template("feedback.html")
    return " seccussfull Done , pls Go Back"




if __name__ == "__main__":
    app.run(debug=True)




