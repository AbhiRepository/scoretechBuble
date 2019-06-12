from flask import Flask, render_template, url_for, flash, redirect, request, session, logging, jsonify
from forms import RegistrationForm, LoginForm, OTPForm, ForgotForm, ResetForm, AddSchoolForm, EmailRegistrationForm
from passlib.hash import sha256_crypt
from flaskext.mysql import MySQL
from functools import wraps
from flask_wtf import CSRFProtect


application = app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 's3cr3t'

#configuration of MySQL database
# app.config['MYSQL_HOST'] = 'mydb.c6js1o7htm0j.us-east-1.rds.amazonaws.com'
# app.config['MYSQL_USER'] = 'master'
# app.config['MYSQL_PASSWORD'] = 'abhishek123'
# app.config['MYSQL_DB'] = 'scoretech'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# app.config['MYSQL_HOST'] = 'db4free.net'
# app.config['MYSQL_USER'] = 'abhishel@localhost'
# app.config['MYSQL_PASSWORD'] = 'Abhishek@123'
# app.config['MYSQL_DB'] = 'scoretech'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abhishek@123'
app.config['MYSQL_DB'] = 'scoretech'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# init MySQL
mysql = MySQL(app)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#route to the home page
@app.route('/')
def home():
    return render_template('main.html', title='Home')

# route to the about page
@app.route('/about')
# @is_logged_in
def about():
    return render_template('about.html', title='About')

# route to register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # If all the condition on form satisfies
    if form.validate_on_submit():
        firstname  = form.firstname.data
        secondname = form.secondname.data
        username   = form.username.data
        school_id   = form.school_id.data
        password   = sha256_crypt.encrypt(str(form.password.data))
        role       = 'admin' # For now it is sticking to admin only

        # Enterting the new user to the database
        cur = mysql.connection.cursor()
        user_exist = cur.execute("SELECT * FROM users WHERE username=%s",[username])
        cur.close()

        # checking if user already exist in database
        if user_exist:
            flash('This user name is already taken!', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(firstname, secondname, username, school_id, role, password) VALUES(%s, %s, %s, %s, 'admin',%s)",(firstname, secondname, username, school_id, password))
            mysql.connection.commit()
            cur.close()
            flash('Account created', 'success')
            return redirect(url_for('home'))

    # If form does not validate render the same page again
    return render_template('register.html', title='Register', form=form)




#route to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    app.logger.info('wwdfffuyfgysgfgyg')
    # If all the condition on form satisfies
    if form.validate_on_submit():
        identification = form.identification.data
        candidate_password = form.password.data

        if identification == 'superadmin' and candidate_password == '123':
            session['logged_in'] = True
            session['user_id']   = '0'
            session['user_role'] = 'superadmin'
            session['school_id'] = '000000'
            return redirect(url_for('admin_options'))

        # checking if user already exist in database
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username=%s", [identification])
        # if a user exist then check the password from the database
        if result:
            current_user=cur.fetchone()
            cur.close()
            password = current_user['password']
            user_id  = current_user['user_id']
            user_role= current_user['role']
            user_school_id = current_user['school_id']
            app.logger.info(user_school_id)

            if sha256_crypt.verify(candidate_password, password):
                #Creating the session for the user
                session['logged_in'] = True
                session['user_id'] = user_id
                session['user_role'] = user_role
                session['school_id'] = user_school_id

                cur = mysql.connection.cursor()
                email_exist = cur.execute("SELECT * FROM users INNER JOIN users_email ON users.user_id = users_email.user_id WHERE users.user_id=%s", [user_id])
                cur.close()

                if email_exist:
                    flash('You are now logged in', 'success')
                    return redirect(url_for('admin_options'))
                else:
                    flash('Enter your email', 'warning')
                    return redirect(url_for('get_email'))
            else:
                flash('Invalid Login','danger')
                return render_template('login.html', title='Login', form=form)
        else:
            flash('Username not found','danger')
            return render_template('login.html', title='Login', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route('/get_email', methods=['GET', 'POST'])
def get_email():
    form=EmailRegistrationForm()
    if form.validate_on_submit():

        email = form.email.data
        app.logger.info(email)
        app.logger.info(int(session['user_id']))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users_email(user_id, email) VALUES(%s, %s)",(session['user_id'], email))
        app.logger.info('query executed sucessfully!!! check the table if it did or not!')
        mysql.connection.commit()
        cur.close()
        flash('Registered email sucessfully!', 'success')
        return redirect(url_for('admin_options'))
    return render_template('get_email.html', title='Register your email', form=form)


@app.route('/add_school', methods=['GET', 'POST'])
def add_school():
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT * FROM school_info WHERE school_id=%s",[session['school_id']])
    if res:
        flash('You have already added a school from your account, Delete the existing school first to add a new school or update the current school', 'warning')
        return redirect(url_for('show_school'))

    form = AddSchoolForm()
    if form.validate_on_submit():

        school_id = session['school_id']
        schoolname = form.schoolname.data
        city = form.city.data
        state = form.state.data
        pincode = form.pincode.data
        addresslineone = form.addresslineone.data
        addresslinetwo = form.addresslinetwo.data
        board = form.board.data
        numberofstudent = form.numberofstudent.data
        pricipalname = form.priciplename.data
        ownername = form.ownername.data
        website = form.website.data
        additionalcomment =form.additionalcomment.data

        cur = mysql.connection.cursor();
        cur.execute("INSERT INTO school_info VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (school_id, schoolname, city, state, pincode, addresslineone, addresslinetwo, board, numberofstudent, pricipalname, ownername, website, additionalcomment))
        mysql.connection.commit()
        cur.close()

        flash('School is Added sucessfully','success')
        return redirect(url_for('show_school'))
    return render_template('add_school.html', title='Add School',form=form)

@app.route('/show_school')
def show_school():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM school_info WHERE school_id=%s",[session['school_id']])
    if result:
        school = cur.fetchone()
        return render_template('show_school.html', title='School', school=school)
    cur.close()
    flash('No existing school yet! Please add a school first', 'warning')
    return redirect(url_for('add_school'))

@app.route('/delete_school')
def delete_school():
    app.logger.info(session['school_id'])
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM school_info WHERE school_id=%s", [session['school_id']])
    mysql.connection.commit()
    cur.close()
    flash('School removed successfully!', 'danger')
    return redirect(url_for('admin_options'))

@app.route('/admin_options', methods=['GET', 'POST'])
def admin_options():
    return render_template('admin_options.html', title='Select Option')



#route for logging out
@app.route('/logout')
def logout():
    session.clear()
    flash('you are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/check', methods=['GET', 'POST'])
def check():
    form = OTPForm()
    if form.validate_on_submit():
        flash('correct otp', 'success')
        return redirect(url_for('home'))
    return render_template('verify.html', title='verify', form=form)

@app.route('/create_user', methods=['GET','POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        flash('New user created', 'success')
        return redirect(url_for('login_or_create'))
    return render_template('create_user.html', title='Create User', form=form)

@app.route('/login_or_create', methods=['GET','POST'])
def login_or_create():
    return render_template('login_or_create.html', title='login or create')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        flash('Mail has been sent to the provided email address','success')
        return redirect(url_for('reset'))
    return render_template('forgot.html', title='Forgot Password', form=form)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        flash('Password is restored','success')
        return redirect(url_for('login'))
    return render_template('reset.html', title='Reset password', form=form)


@app.route('/school_setup', methods=['GET', 'POST'])
def school_setup():
    return render_template('school_setup.html', title='create session')


@app.route('/process', methods=['GET', 'POST'])
def doSomething():
    app.logger.info('happend')
    startdate = request.form['startdate']
    if startdate:
        app.logger.info(startdate)
        return jsonify({'startdate' : startdate})
    app.logger.info('bhag bhosdike')
    return jsonify({'error' : 'Missing data!'})
    # return render_template('school_setup.html', title='create session')

# @app.route('/school_session', methods=['GET', 'POST'])
# def school_session():
#   return render_template('school_session.html')

if __name__ == '__main__':
#   app.config['SECRET_KEY'] = 'supersafe@123'
    app.run(debug=True)

