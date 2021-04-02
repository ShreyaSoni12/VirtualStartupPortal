from flask import Flask , render_template, request, redirect, url_for, session
app = Flask(__name__)
from flask_mysqldb import MySQL
import MySQLdb.cursors

 # secret_key for session
app.secret_key = 'hello'

# Database conectivity
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sadik'      #use your databse username
app.config['MYSQL_PASSWORD'] = 'admin'    #use your databse password
app.config['MYSQL_DB'] = 'vsp_db'

mysql = MySQL(app)



# ******************* Enterpreuner routes *************

@app.route("/")
def landing():
    return render_template('home.html')
@app.route("/list", methods=['GET'])


#enterpruner dasboard showing startup of enterpruner
def stlist():
    if 'loggedin' in session:
        
        return render_template('startuplist.html', username=session['username'])
    
    return redirect(url_for('login'))

#startup create page route and function
@app.route("/create", methods=['GET','POST'])
def stcreate():
    if request.method == 'POST':
        # Create variables for easy access
        vs_name = request.form['title']
        vs_pain = request.form['painarea']
        sloution = request.form['solution']
        session['vs_name']=vs_name
        session['vs_pain']=vs_pain
        session['vs_sol']=sloution
        print(vs_name)
    return render_template('StartupDetatils.html')

@app.route("/create2", methods=['GET','POST'])
def stcreate2():
    industry=['Health Care','Retail','Logistics','Agriculture','Aviation','Automobiles']
    projectN =['Software Heavy','Civil Heavy','Pure Mehnical','Mechatronics','IOT & Automation','Chemical Heavy'] 
    return render_template('create2.html',industry=industry,project=projectN)


@app.route("/login", methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        print(password,email)
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE emailid = %s AND password = %s', (email, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['name']
            # Redirect to home page

            return redirect(url_for('landing'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        # Create variables for easy access
        FirstName = request.form['firstname']
        LastName = request.form['lastname']
        name=FirstName + " "+LastName
        passw = request.form['password']
        EmailId = request.form['emailid']
        phone = request.form['phone']
        role=1
        # print(FirstName,LastName,passw,EmailId,"Sadik")
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE emailid = %s', (EmailId,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            q1 = "insert into user(role_id,name,emailid,password) values('%d','%s','%s','%s')" % (role,name,EmailId,passw)
            cursor.execute(q1)
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    return render_template('Resitration.html')


@app.route("/startuppage")
def startuppage():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('StartupPage.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# ******************************* route for intern ******


@app.route("/intern")
def internhome():
    return render_template('Intern-home.html')


@app.route("/Ilogin")
def internLogin():
    return render_template('Intern-login.html')


#intern registration
@app.route("/signup")
def internSignup():
    return render_template('Intern-Signup-page.html')

#intern registration
@app.route("/signup1",methods=['GET','POST'])
def internSignup2():
    return render_template('Intern-Signup-page2.html')


# intern dashboard
@app.route("/dashboard")
def internDash():
    return render_template('Intern-login-startup-list.html')

@app.route("/setup")
def internSetup():
    return render_template('Intern-Startup-Setup.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0',  port= 80,debug='true')

