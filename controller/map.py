from flask import Blueprint, request

import business.map as map_business
from model.coordinate import Coordinate


blueprint = Blueprint('map', __name__)


@blueprint.post('travel')
def travel():
    content = request.get_json()
    print(content)

    current = Coordinate(
        content['current'].get('system'),
        content['current'].get('planet'),
        content['current'].get('port'),
        content['current'].get('building'))
    destination = Coordinate(
        content['destination'].get('system'),
        content['destination'].get('planet'),
        content['destination'].get('port'),
        content['destination'].get('building'))
    
    success = map_business.travel(current, destination)
    return { 'success': success }
