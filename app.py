from flask import Flask , render_template, request, redirect, url_for, session
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('home.html')
@app.route("/list", methods=['GET'])
def stlist():
    return render_template('startuplist.html')
@app.route("/create")
def stcreate():
    return render_template('StartupDetatils.html')

@app.route("/create2", methods=['GET','POST'])
def stcreate2():
    industry=['Health Care','Retail','Logistics','Agriculture','Aviation','Automobiles']
    projectN =['Software Heavy','Civil Heavy','Pure Mehnical','Mechatronics','IOT & Automation','Chemical Heavy'] 
    return render_template('create2.html',industry=industry,project=projectN)


@app.route("/login")
def login():
    return render_template('login.html')
@app.route("/register")
def register():
    return render_template('Resitration.html')



if __name__ == "__main__":
    app.run(host = '0.0.0.0',  port= 80,debug='true')

