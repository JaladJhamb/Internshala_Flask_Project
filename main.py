from flask import Flask, render_template, request, redirect, url_for,jsonify,make_response, session
import pandas as pd
import matplotlib.pyplot as plt
import pymysql as sql
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def read_data():
    data = pd.read_csv("Internshall.csv")
    data.drop(["Unnamed: 0", "_id"], axis=1, inplace=True)
    return data 


@app.route("/filter/")
def form():
    data = read_data()
    location = list(data['Location'].unique())
    skills_perks = []
    for i in data['Skills and Perks']:
        skills_perks.extend(list(map(lambda x: x[1:-1].strip().lower(), i[1:-1].split(","))))
    skills_perks = pd.Series(skills_perks).unique()
    profile = list(data['profile'].unique())
    duration = list(data['Duration'].unique())
    return render_template("form.html", location=location, skills=skills_perks, profile=profile, duration=duration)

@app.route("/aftersubmit/", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == "GET":
        return redirect(url_for("form"))
        #return render_template("form.html")
    else:
        name = request.form.get("name")
        location = request.form.get("location")
        skills = request.form.get("skills")
        duration = request.form.get("duration")
        profile = request.form.get("profile")
        data = read_data()
        temp = data.copy()
        print(profile, location, duration)
        if profile:
            temp = temp[temp['profile'] == profile]
        if skills:
            temp = temp[temp['Skills and Perks'].apply(lambda x:True if skills in eval(x.lower()) else False)]
        if location:
            temp = temp[temp['Location'] == location]
        if duration:
            temp = temp[temp['Duration'] == duration]
        #if temp.values:
        
        return temp.to_html() 
        # else:
        #     msg = "No Such data"
        #     return render_template("showdata.html", msg=msg)
        # return temp.to_html()
        #return render_template(temp.to_html())


# query --> solution 
# send_mail(email, solution) --> email

@app.route('/aftercontact/', methods = ['POST'])
def aftercontact():
    db = sql.connect(host='localhost',port= 3306,user= 'root',database='internshala_contact')
    cur=db.cursor()

    name= request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    cmd= f"insert into info(name,email,message) values('{name}','{email}','{message}')"
    cur.execute(cmd)
    db.commit()

    return render_template("index.html",msg="data saved successfully, we will revert you back as soon as possible")

app.run(port=80, debug=True)
