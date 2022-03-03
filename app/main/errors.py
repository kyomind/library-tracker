from flask import render_template

from app.main import main


@main.app_errorhandler(401)
def unauthorized(err):
    return render_template('401.html', err=err), 401


@main.app_errorhandler(404)
def not_found(err):
    return render_template('404.html', err=err), 404


@main.app_errorhandler(500)
def server_error(err):
    return render_template('500.html', err=err), 500
