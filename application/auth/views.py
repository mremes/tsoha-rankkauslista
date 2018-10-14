from flask import flash, redirect, url_for, render_template, request, abort
from application import app, db
from application.auth.models.user import User
from application.forms import LoginForm, RegisterForm
import application.utils as utils
import application.auth.login as app_login


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(form.name.data, form.username.data, form.role.data, form.password.data)
        db.session().add(user)
        db.session().commit()
        flash(u'Onnistuneesti rekisteröitynyt käyttäjä: %s' % user.username)
        return redirect(utils.get_next_url())
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        flash(u'Tervetuloa %s!' % form.user.name)
        next = request.args.get('next')
        app_login.login_user(form.user)
        if not utils.is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    app_login.logout_user()
    flash(u'Olet kirjautunut ulos.')
    return redirect(url_for('index'))
