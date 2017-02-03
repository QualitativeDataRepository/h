# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from h.util.view import json_view
from h.exceptions import APIError


log = logging.getLogger(__name__)


@json_view(route_name='status')
def status(request):
    _check_database(request)
    _check_search(request)
    _check_realtime(request)
    return {'status': 'okay'}


def _check_database(request):
    try:
        request.db.execute('SELECT 1')
    except Exception as exc:
        log.exception(exc)
        raise APIError('Database connection failed')


def _check_search(request):
    try:
        info = request.es.conn.cluster.health()
        if info['status'] not in ('green', 'yellow'):
            raise APIError('Search cluster state is %s' % info['status'])
    except Exception as exc:
        log.exception(exc)
        raise APIError('Search connection failed')


def _check_realtime(request):
    try:
        request.realtime.connection.release()
        request.realtime.connection.connect()
    except Exception as exc:
        log.exception(exc)
        raise APIError('Realtime connection failed')
