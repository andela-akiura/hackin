from flask import render_template, session, url_for, Response, redirect, request
from . import main
from forms import FormLogin, NewSession
from .. import db
from ..models import CodeSessions, User
from app import login_mgr
from flask.ext.login import login_user, logout_user, login_required, current_user
import flask
import json


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home')
def home():
    # query for sessions by this user
    user = User.query.get(current_user.id)
    sessions = user.sessions
    return render_template('home.html', sessions=sessions)


@main.route('/sessions')
def sessions():
    return render_template('sessions.html')


@main.route('/myhacks')
@main.route('/new', methods=['GET', 'POST'])
def new_session():
    form = NewSession()
    if form.validate_on_submit():
        session_ = CodeSessions(session_name=form.session_name.data,
                                session_lang=form.language.data)
        user_ = User.query.get(current_user.id)
        user_.sessions.append(session_)
        db.session.add(user_)
        db.session.commit()
        id_ = session_.id
        return render_template('sessions.html', id_=id_)
    return render_template('add_session.html', form=form)


@main.route('/fromajax', methods=['GET', 'POST'])
def from_ajax():
    req_json = request.get_json()
    print req_json['id_']
    session_id = req_json['id_']
    user = User.query.get(current_user.id)

    if session_id:
        codesession = CodeSessions.query.get(session_id)

        codesession.session_address = req_json['session_url']
        user.sessions.append(codesession)
        db.session.add(user)
        db.session.commit()
        resp = {'respose': 'successful',
                'message': 'data received succesfully'}
    else:
        resp = {'response': 'not executed',
                'message': 'data not updated'}

    return flask.jsonify(**resp)
