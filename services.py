from flask import Blueprint, jsonify

import grequests
import json

from myocen import constants 

LENDERS = [
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002"
]

LOAN_REQUESTS = {

}
services = Blueprint("services", __name__)

headers = {
    'Content-Type': 'application/json',
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def read_json_file(file_name):
    with open(file_name) as input_file:
        data = json.load(input_file)
    return data


def make_request(data, url):
    lenders = []
    for host in LENDERS:
        resp = grequests.post(url=host + url, data=data, headers=headers)
        lenders.append(resp)
    responses = grequests.map(lenders)
    return responses


@services.route("/createLoanRequest")
def loan_application_request():
    global LOAN_REQUESTS

    data = read_json_file("./static/loan-request.json")
    responses = make_request(data, constants.LOAN_REQUEST_PATH)
    message = {
        "message": "submitted successfully to lenders"
    }
    request_id = data["metadata"]["requestId"]
    for resp in responses:
        loan_obj = LOAN_REQUESTS.get(request_id, {})
        loan_obj.update({1: 'PENDING'})
    return jsonify(message), 200


@services.route("/consentHandleRequest")
def consent_handle_request():
    data = read_json_file("./static/consent-request.json")
    make_request(data, constants.CONSENT_HANDLE_REQUEST_PATH)
    message = {
        "message": "submitted consent handle request to lenders"
    }
    return jsonify(message), 200


@services.route("/consentStatusRequest")
def consent_status_request():
    data = read_json_file("./static/consent-status-request.json")
    requests.post(url=LENDERS[0]+constants.CONSENT_STATUS_REQUEST_PATH, data=data)
    message = {
        "message": "submitted consent status request to lenders"
    }
    return jsonify(message), 200


@services.route("/generateOffersRequest")
def generate_offers_request():
    data = read_json_file("./static/generate-offers-request.json")
    make_request(data, constants.GEN_OFFERS_REQUEST_PATH)
    message = {
        "message": "submitted offers request to lenders"
    }
    return jsonify(message), 200


@services.route("/setOffersRequest")
def set_offers_request():
    data = read_json_file("./static/set-offers-request.json")
    make_request(data, constants.SET_OFFERS_REQUEST_PATH)
    message = {
        "message": "selected offer sent to lender"
    }
    return jsonify(message), 200

