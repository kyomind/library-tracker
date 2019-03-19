from flask import render_template
from . import main

@main.app_errorhandler(404)
def not_found(err):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def server_error(err):
    return render_template('500.html'),500