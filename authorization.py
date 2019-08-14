"""
authorization.py
------------------
*Definition of the login/logout/register/delete User*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


#encoding=utf-8
from models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    """
    *Retrieve logged users' ID*

    :param user_id:
    :return: User
    """
    return Auth_User.query.get(int(user_id))


@app.route('/login')
def login():
    """
    *Login Page*

    :return: login.html
    """
    return render_template('login.html')


@app.route('/verify', methods=['POST'])
def verify():
    """
    *Verifies User Credentials*

    :return: index page
    """
    user = request.form['username']
    pwd = request.form['psw']
    cur_user = db.session.query(func.public.verify_password(pwd,user)).first()[0]
    #print (cur_user)
    if (cur_user):
        cur_user = Auth_User.query.filter_by(username=user).first()
    # if (cur_user.pwd_verify(pwd)):
        login_user(cur_user)
        session['logged_in'] = True
        session['user'] = cur_user.username
        session['token'] = cur_user.token
        session['user_id'] = cur_user.user_id
        return redirect('/')
    else:
        session['logged_in'] = False
    return redirect('/login')


@app.route('/register')
def register():
    """
    *Register Page*

    :return: register.html
    """
    return render_template('register.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    """
    *User Creation(Registration)*
    """
    user = request.form['username']
    pwd = request.form['password']
    name = request.form['name'] if request.form['name'] != '' else None
    surname = request.form['surname'] if request.form['surname'] != '' else None
    email = request.form['email']
    note = request.form['note'] if request.form['note'] != '' else None
    try:
        engine = create_engine(Conf.SQLALCHEMY_DATABASE_URI)
        engine.execute("insert into authorizer_user(name,surname,username,email,password,note,token) values"
                       " (%s, %s, %s, %s, crypt(%s,gen_salt('md5')),%s,uuid_generate_v4());", [name,surname,user,email,pwd,note])
    except Exception as ex:
        print (ex)#.orig.diag.message_detail)
        return render_template('register.html', msg='Username (%s) already exists!' %user)
    return redirect('/login')


@app.route('/deleteuser', methods=['POST'])
@login_required
def delete_user():
    """
    *Deletes User*
    """
    uid = request.form['id']
    Auth_User.query.filter_by(user_id=uid).delete()
    db.session.commit()
    return ('/usersview/succ0')


@app.route('/profile/<user>')
@login_required
def profile(user=None):
    """
    :param user:
    :return: User's Profile
    """
    if user == session['user']:
        usr = Auth_User.query.filter_by(username=user).first()
        return render_template('profile.html', user=usr)
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    """
    *Logout User*

    :return: login page
    """
    logout_user()
    return redirect('/login')
