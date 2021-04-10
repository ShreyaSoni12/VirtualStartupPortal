from flask import Flask , render_template, request, redirect, url_for, session,flash
app = Flask(__name__)
from flask_mysqldb import MySQL
import MySQLdb.cursors

from datetime import datetime
now = datetime.now()
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

@app.route("/dash", methods=['GET'])
#enterpruner dasboard showing startup of enterpruner
def stlist():
    if 'loggedin' in session:
        founder_id=session['id']
        cursor = mysql.connection.cursor()
        try:
            
            q4= "SELECT * FROM virtualstartup WHERE founder_id = '%d' " % (founder_id)
            cursor.execute(q4)
            startup=cursor.fetchall()
        except:
            print("error")
        st_list = []
        for st in startup:
            st_list.append(st[2])
             
        # print(startup[0])
        return render_template('startuplist.html', startup=st_list)
    
    return redirect(url_for('login'))

#startup create page route and function
@app.route("/create", methods=['GET','POST'])
def stcreate():
    if 'loggedin' in session:
        if request.method == 'POST' and 'title' in request.form :

            # Create variables for easy access
            vs_name = request.form['title']
            vs_pain = request.form['painarea']
            sloution = request.form['solution']
            session['vs_name']=vs_name
            session['vs_pain']=vs_pain
            session['vs_sol']=sloution

            return redirect(url_for('stcreate2',name=vs_name))
        return render_template('StartupDetatils.html')
    return redirect(url_for('login'))

@app.route("/create/<name>", methods=['GET','POST'])
def stcreate2(name):
    if name == session['vs_name']:
        industry=['Health Care','Retail','Logistics','Agriculture','Aviation','Automobiles']
        projectN =['Software Heavy','Civil Heavy','Pure Mehnical','Mechatronics','IOT & Automation',
                   'Chemical Heavy']
        
        if request.method == 'POST' and 'industry' in request.form:
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            Industry = request.form['industry']
            projectN = request.form['ProjectNature']
            skil = request.form['skill']
            tech = request.form['tech']
            # print(session,"sadik")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            q1 = "insert into virtualstartup(founder_id,vs_name,vs_pain_areas,vs_solution,vs_industry,vs_project_nature,vs_skills_required,vs_technologies,last_updated,updatedby_id) values('%d','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (session['id'],session['vs_name'], session['vs_pain'],session['vs_sol'],Industry,projectN,skil,tech,formatted_date,session['id'])
            try:
                
                cursor.execute(q1)
                mysql.connection.commit()
                flash('You have successfully created!')
                return redirect(url_for('stlist'))
            except:
                flash ("Something Wrong !")
                return render_template('create2.html',industry=industry,project=projectN)
        return render_template('create2.html',industry=industry,project=projectN)
    return redirect(url_for('stcreate'))


#loging for enterpruner
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
        cursor.execute('SELECT * FROM user WHERE emailid = %s AND password = md5(%s)', (email, password,))
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
            flash("Incorrect username/password!")
            # msg= "Incorrect username/password!"
            # print("erro")
            # return render_template('login.html')
    
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
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
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
            q1 = "insert into user(role_id,name,emailid,password,Phone) values('%d','%s','%s',MD5('%s'),%s)" % (role,name,EmailId,passw,phone)
            # q2 = "insert into founder values((select user_id from user where emailId='%s' ),'%s',(select user_id from user where emailId='%s' ))" % (EmailId, ) 
            cursor.execute(q1)
            mysql.connection.commit()
            flash( 'You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')

    return render_template('Resitration.html')


@app.route("/startup/<title>")
def startuppage(title):
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('StartupPage.html', title=title)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route("/hire")
def hire():
    return render_template('Hire-new-team-membear.html')
@app.route("/search")
def search():
    return render_template('search-for-intern.html')

@app.route("/existingapplication")
def application():
    return render_template('existing-application.html')

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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM state_list')
        # Fetch one record and return result
    account = cursor.fetchall()
# t in account:
#         state.append(st[])
#     print(state[1])    state = []
#     for s
    
    return render_template('Intern-Signup-page2.html',state=account)


# intern dashboard
@app.route("/dashboard")
def internDash():
    # founder_id=session['id']
    # cursor = mysql.connection.cursor()
    # try:
            
    #     q4= "SELECT * FROM virtualstartup WHERE founder_id = '%d' " % (founder_id)
    #     cursor.execute(q4)
    #     startup=cursor.fetchall()
    # except:
    #     print("error")
    # st_list = []
    # for st in startup:
    #     st_list.append(st[2])
    return render_template('Intern-login-startup-list.html')

@app.route("/setup")
def internSetup():
    return render_template('Intern-Startup-Setup.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0',  port= 80,debug='true')

