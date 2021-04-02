from flask import Flask , render_template, request, redirect, url_for, session
app = Flask(__name__)

# Enterpreuner routes

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


@app.route("/startuppage")
def startuppage():
    return render_template('StartupPage.html')

# route for intern ******


@app.route("/intern")
def internhome():
    return render_template('Intern-home.html')


@app.route("/Ilogin")
def internLogin():
    return render_template('Intern-login.html')



@app.route("/signup")
def internSignup():
    return render_template('Intern-Signup-page.html')
    
@app.route("/signup1",methods=['GET','POST'])
def internSignup2():
    return render_template('Intern-Signup-page2.html')

@app.route("/das")
def internDash():
    return render_template('Intern-login-startup-list.html')

@app.route("/setup")
def internSetup():
    return render_template('Intern-Startup-Setup.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0',  port= 80,debug='true')

