"""
main.py
---------
"""

#encoding=utf-8
from models import *
from contextProcessors import *
from authorization import *
from passwordHandler import *

db.create_all()


@app.route('/')
@app.route('/<err>')#In case user tries to type a url he has no access
@login_required
def index(err=None):
    """
    *Index page.*

    :param err:
    :return: index.html
    """
    acs = Auth_Access.query.filter_by(user_id=session['user_id']).all()
    tb =  ([ac.pass_id for ac in acs])
    #tb.append(2)
    pwd = Auth_Pass.query.filter(Auth_Pass.pass_id.in_((tb))).all()
    decrypted = pwd.copy()
    for cnt,epwd in enumerate(pwd):
        decrypted[cnt].password = decryptor(epwd.password)
    return render_template('index.html', pwd=decrypted, user=session['user'], token=session['token'], user_id=session['user_id'], err=err)


@app.route('/accessview')
@app.route('/accessview/<err>')
@login_required
def accessView(err=None):
    """
    *List of Users-Pass only for Administrator account*

    :param err:
    :return: access_table.html
    """
    users = Auth_User.query.filter(Auth_User.user_id != 1).all()
    pwds = Auth_Pass.query.all()
    userpass = Auth_Access.query.join(Auth_User, Auth_User.user_id==Auth_Access.user_id).join(Auth_Pass, Auth_Pass.pass_id==Auth_Access.pass_id)\
        .add_columns(Auth_User.username, Auth_Access.user_id, Auth_Pass.name, Auth_Access.pass_id).filter(Auth_User.user_id != 1).order_by(Auth_User.username).all()
    if session['user_id'] == 1:
        return render_template('access_table.html', user=session['user'], user_id=session['user_id'], userpass=userpass, users=users, pwds=pwds, err=err)
    return redirect('/err3')

@app.route('/usersview')
@app.route('/usersview/<err>')
@login_required
def usersView(err=None):
    """
    *View of Users List*

    :param err:
    :return: users.html
    """
    if session['user_id'] == 1:
        users = Auth_User.query.all()
        return render_template('users.html', user=session['user'], users=users, err=err)
    return redirect('/err3')


@app.route('/token=<token>/name=<name>')
def getPasswordByToken(token=None,name=None):
    """
    *Given user's Token and password's name returns a dict of the passwords credentials*

    :param token: User's Token
    :param name: Password's name
    :return: jsonify(password_dict)
    """
    try:
        user = Auth_User.query.filter_by(token=token).first()
        pwd = Auth_Pass.query.filter_by(name=name).first()
        access_granted = Auth_Access.query.filter_by(user_id=user.user_id,pass_id=pwd.pass_id).first()
        if access_granted:
            passdict = {'pass_id': pwd.pass_id,
                        'name': pwd.name,
                        'host': pwd.host,
                        'username': pwd.username,
                        'password': decryptor(pwd.password),
                        'note': pwd.note}
            print(passdict)
            return jsonify(passdict)
        else:
            return 'Access Denied'
    except Exception as ex:
        print(ex.args[0])
        return 'An error has occured.'


@app.route('/token=<token>')
def getPasswordsByToken(token):
    """
    *Given user's Token returns a list of the password names*

    :param token: User's Token
    :return: list of password names
    """
    try:
        user = Auth_User.query.filter_by(token=token).first()
        userpass = Auth_Pass.query.join(Auth_Access, Auth_Access.user_id == user.user_id) \
            .add_columns(Auth_Pass.name).filter(Auth_User.user_id != 1).order_by(Auth_Pass.name).all()
        passlist = []
        for up in userpass:
            passlist.append(up.name)
        return jsonify(passlist)
    except Exception as ex:
        print(ex.args[0])
        return 'An error has occured.'


if __name__ == "__main__":
    app.run('0.0.0.0', '8000')
