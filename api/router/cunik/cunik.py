"""Take the parameters from router, parse them, execute and return the results."""
import json

from flask import request, Blueprint
from api.models import cunik_registry
from random import randint

bp = Blueprint('cunik', __name__)


@bp.route('/create', methods=['POST'])
def create():
    image_name = request.form.get('image_name')
    params = {}
    params['ipv4_addr'] = request.form.get('ipv4_addr')
    print(image_name, params, '=======================')
    cunik_registry.create(
        name=image_name + str(randint(0, 1048576)),  # Well, okay for now
        image_name=image_name,
        ipv4_addr=params['ipv4_addr'],
        cmdline=None
    )


@bp.route('/list', methods=['GET'])
def list():
    return json.dumps(CunikApi.list())


@bp.route('/info', methods=['POST'])
def info():
    cid = request.form.get('cid')
    return CunikApi.info(cid=cid)


@bp.route('/stop', methods=['POST'])
def stop():
    cid = request.form.get('cid')
    return CunikApi.stop(cid=cid)


@bp.route('/remove', methods=['POST'])
def remove():
    cid = request.form.get('cid')
    return CunikApi.remove(cid=cid)
