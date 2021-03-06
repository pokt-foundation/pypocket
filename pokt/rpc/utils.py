import json
from typing import Optional
import requests

from . import DEFAULT_GET_HEADERS, DEFAULT_POST_HEADERS, PoktRPCError, PortalRPCError


def make_api_url(provider_url: str, route: str, version: str = "v1") -> str:
    if not provider_url.endswith("/"):
        provider_url += "/"
    if not route.startswith("/"):
        route = "/" + route
    return provider_url + version + route


def get(route: str, session: Optional[requests.Session] = None, **params) -> str:
    if session is None:
        resp = requests.get(route, headers=DEFAULT_GET_HEADERS, params=params)
    else:
        resp = session.get(route, params=params, headers=DEFAULT_GET_HEADERS)
    try:
        data = resp.json()
    except:
        pass
    else:
        if isinstance(data, dict):
            error_obj = data.get("error")
            if error_obj:
                error_code = error_obj.get("code", None)
                if error_code is None:
                    error_code = error_obj.get("statusCode", None)
                raise PortalRPCError(error_code, error_obj.get("message"))

            error_code = data.get("code", None)
            if error_code:
                raise PoktRPCError(error_code, data.get("message"))
    return resp.text


def post(route: str, session: Optional[requests.Session] = None, **payload) -> dict:
    if session is None:
        resp = requests.post(
            route, headers=DEFAULT_POST_HEADERS, data=json.dumps(payload)
        )
    else:
        resp = session.post(
            route, data=json.dumps(payload), headers=DEFAULT_POST_HEADERS
        )
    data = resp.json()
    if isinstance(data, dict):
        error_obj = data.get("error")
        if error_obj:
            raise PortalRPCError(error_obj.get("code"), error_obj.get("message"))

        error_code = data.get("code", None)
        if error_code:
            raise PoktRPCError(error_code, data.get("message"))
    return data
