from flask import render_template,redirect,url_for
from ..models import Community
from .forms import RegistrationForm
from .. import db
from . import auth

@auth.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        community = Community