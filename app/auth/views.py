from flask import render_template,redirect,url_for
from ..models import Community
from .forms import RegistrationForm
from .. import db
from . import auth

@auth.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        community = Community(username = form.username.data,
                              email = form.email.data,
                              password = form.password.data
                             )
        db.session.add(community)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title =  'Create Account'
    return render_template('auth/register.html',registration_form = form)