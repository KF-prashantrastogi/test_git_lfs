import os
import sys
from flask import Flask, request
import tempfile
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from FlaskAPI import get_flaskapp

# os.path.join(os.path.dirname(__file__), "/FlaskAPI/config.json")

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = get_flaskapp()
    app.config.from_mapping({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_skill_augment(client):
    """
    Asserts response status 200 (OK) and non-null
    response for skillaugment meessage type when
    valid skill_list is passed in request body.
    """
    print('Print this message')
    body = {
        "request": {
            "type": "skillaugment",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                    "sp_id": "ITH0219",
                    "skills_list": "python, java"
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    assert rv.json['response']['data'] != None
    # assert False


def test_skill_augment_empty_skills(client):
    """
    Asserts response status 200 (OK) and non-null response
    for skillaugment meessage type when empty skill_list
    and non-empty sp_id is passed in request body.
    """
    print('Print this message')
    body = {
        "request": {
            "type": "skillaugment",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                    "sp_id": "ITH0219",
                    "skills_list": ""
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    assert not rv.json['response']['data'][0]['kf_skills_input']

    print(rv.json['response']['data'][0])
    # assert False


def test_skill_augment_spaugment(client):
    """
    Asserts response status 200 (OK) and non-null skill-sp_id
    for spaugment meessage type  when valid skill_list and
    non-empty sp_id is passed in request body.
    """
    body = {
        "request": {
            "type": "spaugment",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                    "sp_id": "ITH0219",
                    "skills_list": "python, java"
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    print(rv.json['response']['data'][0])

    assert not not rv.json['response']['data'][0]['kf_skills_spid']


def test_skill_augment_spaugment_empty_spid(client):
    """
    Asserts response status 200 (OK) and non-null skill-sp_id
    for spaugment meessage type  when valid skill_list and
    empty sp_id is passed in request body.
    """
    body = {
        "request": {
            "type": "spaugment",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                    "sp_id": "",
                    "skills_list": "python, java"
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    print(rv.json['response']['data'][0])

    assert not rv.json['response']['data'][0]['kf_skills_spid']


def test_skill_augment_invalid_type(client):
    """
    Asserts response status 200 (OK) and error response (status
    failed) a message type other than skillaugment and spaugment.
    """
    body = {
        "request": {
            "type": "ransomwarea",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                    "sp_id": "ITH0219",
                    "skills_list": "python, java"
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    print(rv.json['response'])
    assert rv.json['response']['error_details']['status'] == 'failed'


def test_reqd_params_not_passed(client):
    """
    Asserts response status 200 (OK) and error response (status
    failed) when sp_id and skill_list are not passed for a valid
    message type.
    """
    body = {
        "request": {
            "type": "skillaugment",
            "id": "",
            "data": [
                {
                    "company_id": 6504,
                    "employee_no": 8372684214,
                    "job_title": "Senior Dealer Money Market & FX Treasury Division",
                    "employee_id": 5369642226,
                    "manager_id": 2750334849,
                }
            ]
        }
    }
    rv = client.post('/kf_augment', json=body)

    assert rv.status_code == 200
    print(rv.json['response'])
    assert rv.json['response']['error_details']['status'] == 'failed'
