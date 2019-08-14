"""
passwordHandler.py
----------------------
Create,Delete,Update and GrantAccess method implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

#encoding=utf-8
from models import *



@app.route('/create_password')
@login_required
def create_password():
    """
    Password Creation Page
    :return: create_password.html
    """
    return render_template('create_password.html')


@app.route('/submit_password', methods=['POST'])
@login_required
def submit_password():
    """
    Submission of Created Password
    """
    user = request.form['username']
    pwd = request.form['password']
    name = request.form['name']
    note = request.form['note'] if request.form['note'] != '' else None
    host = request.form['host'] if request.form['host'] != '' else None
    try:
        engine = create_engine(Conf.SQLALCHEMY_DATABASE_URI)
        encrypted = engine.execute(func.encrypt_aes(pwd)).first()[0]
        new_pass = engine.execute("insert into authorizer_password(name, host, username, password, note, owner_id) values(%s, %s, %s, %s, %s, %s);",
                                  [name,host,user,encrypted,note, session['user_id']])
        pass_id = engine.execute("select pass_id from authorizer_password where name=%s and username=%s and password=%s;", [name,user,encrypted]).first()[0]
        if session['user_id'] != 1:
            self_assign = engine.execute("insert into authorizer_access(pass_id,user_id) values(%s, %s),(%s,%s);", [pass_id,session['user_id'],pass_id,1])
        else:
            self_assign = engine.execute("insert into authorizer_access(pass_id,user_id) values(%s, %s);", [pass_id,1])
    except Exception as ex:
        print (ex)#.orig.diag.message_detail)
        return redirect('/err1')
    return redirect('/created')


@app.route('/edit/<id>')
@login_required
def edit(_id):
    """
    Password Edit Page

    :param id: identifier
    :return: edit_password.html
    """
    if session['user_id'] == 1:
        edit_pass = Auth_Pass.query.filter_by(pass_id=_id).first()
    else:
        edit_pass = Auth_Pass.query.filter_by(pass_id=_id, owner_id=session['user_id']).first()
    if edit_pass:
        return render_template('edit_password.html', pwd=edit_pass)
    return redirect('/err0') #Redirect in case user has no access.


@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    """
    Password Update
    """
    _id = request.form['id']
    user = request.form['username']
    pwd = request.form['password']
    name = request.form['name']
    note = request.form['note'] if request.form['note'] != '' else None
    host = request.form['host'] if request.form['host'] != '' else None
    try:
        engine = create_engine(Conf.SQLALCHEMY_DATABASE_URI)
        encrypted = engine.execute(func.encrypt_aes(pwd)).first()[0]
        new_pass = engine.execute("update authorizer_password set name=%s, host=%s, username=%s, password=%s, note=%s where pass_id=%s;",
                                  [name,host,user,encrypted,note,_id])
    except Exception as ex:
        print (ex)#.orig.diag.message_detail)
        return redirect('/err2')
    return redirect('/updated')


@app.route('/delete', methods=['POST'])
@login_required
def delete_pass():
    """
    Deletion of existing Password
    """
    id = request.form['id']
    Auth_Pass.query.filter_by(pass_id=id).delete()
    db.session.commit()
    return ("Deleted password with id '%s'" %id)


@app.route('/grantaccess', methods=['POST'])
@login_required
def grantAccess():
    """
    Grant Access to a Pass to specific User
    """
    uid = request.form['user_id']
    pid = request.form['pass_id']
    try:
        engine = create_engine(Conf.SQLALCHEMY_DATABASE_URI)
        new_access = engine.execute("insert into authorizer_access(user_id,pass_id) values(%s,%s);", [uid, pid])
    except Exception as ex:
        print(ex)  # .orig.diag.message_detail)
        return ('/accessview/err0')
    return ('/accessview')


@app.route('/revokeaccess', methods=['POST'])
@login_required
def revokeAccess():
    """
    Revoke Access to a Pass to specific User
    """
    id = request.form['id']
    uid, pid = id.split('-')
    Auth_Access.query.filter_by(pass_id=pid, user_id=uid).delete()
    db.session.commit()
    return ('/accessview/succ0')