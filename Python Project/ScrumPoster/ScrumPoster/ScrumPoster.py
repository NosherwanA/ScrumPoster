import json
import os
import inspect
import sys
from mattermostapi import MatAPI


def main():
    """
    This script posts the daily scrum message to all channels inside the JSON file
    :return: NONE
    """
    config = get_config()

    if config is None:
        sys.exit(1)

    api = MatAPI(url=config["mattermost"]["url"],
                 login=config["mattermost"]["userID"],
                 password=config["mattermost"]["password"],
                 version=config["mattermost"]["version"])

    user_data = api.get('users/me')
    user_id = user_data['id']

    data = get_current_data()

    mattermost_post(api, user_id, data)


def get_config():
    """
    Opens the config file and returns a Python dictionary
    :return: Python dictionary containing config variables
    """

    filepath = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))) + r"""/config/config.json"""

    try:
        data = json.load(open(filepath))
        return data
    except FileNotFoundError:
        print("Config File Not Found")
        return None


def get_current_data():
    """
    Gets the data in the existing JSON file and returns is
    :return: data from JSON file
    """

    filepath = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))) + r"""/scrum_list/scrum_list.json"""

    try:
        data = json.load(open(filepath))
        return data
    except FileNotFoundError:
        print("Current list Not Found")
        return None
    except IOError:
        print("File is malformed. Please check if it is properly formatted")
        return None


def mattermost_post(api, user_id, data):
    """
    Cycles through all channels and posts the scrum message
    :param api: The Mattermost API instance
    :param user_id: The id used to post the message
    :param data: JSON object containing the team and channel ids
    :return: NONE
    """

    for k, v in data.items():
        channel_id = k
        team_id = v
        post_message(api, user_id, team_id, channel_id)


def post_message(api, user_id, team_id, channel_id):
    """
    Post the scrum message to the specified channel
    :param api: The Mattermost API instance
    :param user_id: The id used to post the message
    :param team_id: id of the team to whcih channel is part of
    :param channel_id: id of the channel where to post the message
    :return: NONE
    """

    text_body = {
        "used_id": user_id,
        "channel_id": channel_id,
        "message": "@all \n"
                   "1)What did you do yesterday that helped the development team meet the sprint "
                   "goal? \n"
                   "2)What will you do today to help the development team meet the sprint goal? \n"
                   "3)Do you see any impediment that prevents you or the development team from "
                   "meeting the sprint goal"
                   "? \n"

    }

    endpoint = '/teams/' + team_id + '/channels/' + channel_id + '/posts/create'

    api.post(endpoint, text_body)


if __name__ == "__main__":
    main()
