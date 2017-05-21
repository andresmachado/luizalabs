"""Auxiliary functions."""
import requests
import facebook
from django.conf import settings


def get_gender(obj):
    """
        Define gender by first name of obj based on genderize.io API.

    :param obj: A dictionary with obj info
    :return: String with gender
    """
    gender_url = '{0}{1}'.format(settings.GENDERIZE_URL, obj.get('first_name'))
    req = requests.get(gender_url)
    gender = req.json().get('gender', 'Unknown')

    return gender


def update_gender_info(obj):
    """
        Update a dictionary from facebook info with gender.

    :param obj: A dictionary with facebook user info
    :return: Updated dictionary with gender
    """
    gender = get_gender(obj)
    obj.update({
        'gender': gender
    })

    return obj


def get_facebook_obj(facebook_id):
    """
        Get info about some user based on facebook_id.

    :param facebook_id: A facebook ID
    :return: Dictionary with facebook user info
    """
    req = requests.get(settings.FACEBOOK_OAUTH_URL)
    fb_access_token = req.json().get('access_token')
    fields = 'id, first_name, last_name, name, link, gender'
    graph = facebook.GraphAPI(access_token=fb_access_token, version='2.7')
    obj = graph.get_object(id=str(facebook_id), fields=fields)
    updated_obj = update_gender_info(obj)

    return updated_obj
