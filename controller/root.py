from flask import Blueprint

import business.player as player_business


blueprint = Blueprint('root', __name__)


@blueprint.post('login')
def login():
    player_business.login()
    return { 'success': True }
