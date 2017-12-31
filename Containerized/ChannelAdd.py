import json
import os
import inspect
import sys
from mattermostapi import MatAPI


def main():
    """
        This Script automatically adds the channels the provided user account is a part of to scrum_list.json for scrum message posting.

        :return: None
        """

    config = get_config()

    if config is None:
        sys.exit(1)

    api = MatAPI(url=config["mattermost"]["url"],
                 login=config["mattermost"]["userID"],
                 password=config["mattermost"]["password"],
                 version=config["mattermost"]["version"])
    
    search_for_teams(api)


def search_for_teams(api):
    """
    Iterates through all teams the provided user account is part of 

    :param api: The Mattermost API instance
    """
    
    current_list = get_current_data()

    if current_list is None:
        sys.exit(2)

    team_list = get_teams(api)

    for team in team_list:
        channel_list = get_channels(api, team)

        for channel in channel_list:
            is_found = search_existing_list(team, channel, current_list)

            if not is_found:
                add_to_list(team, channel, current_list)

    write_new_data(current_list)


def search_existing_list(team_id, channel_id, current_data)
    """
    Searches through existing data from list.json for the provided team and channel id
    :param team_id: The team id to be searched
    :param channel_id: The channel id to be searched
    :param current_data: The current data from scrum_list.json file
    :return: Boolean value representing if the provided team and channel id is found
    """

    for channel, team in current_data.items():
        if ((channel == channel_id) and (team == team_id)):
            return True
    
    return False


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
    except IOError:
        print("Config File Not Found")
        return None


def get_teams(api):
    """
    Returns all the teams the user is part of
    :param api: The Mattermost API instance
    :return: The list of teams the user account is part of 
    """

    team_list = api.get('/teams/all')

    return team_list


def get_channels(api, team_id):
    """
    Searches the channel under the user and returns the team id if found
    :param api: The Mattermost API instance
    :param team_id: The team id for which the list of channels is required
    :return: The list of channels for that perticular team
    """

    outgoing_field = '/teams/' + team_id + '/channels/'

    channel_list = api.get(outgoing_field)

    return channel_list


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
    except JSONDecodeError:
        print("File is malformed. Please check if it is properly formatted")
        return None


def write_new_data(data):
    """
    Writes the new data back to the original file
    :param data: new data to be written
    :return: NONE
    """

    filepath = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))) + r"""/scrum_list/scrum_list.json"""

    with open(filepath, "w") as new:
        new.write(json.dumps(data, sort_keys=True, indent=4))
        new.close()


def add_to_list(team_id, channel_id, current_data):
    """
    Adds the found team and channel to JSON file for scrum posting
    :param team_id: The team id to be added
    :param channel_id: The channel id to be added
    :param current_data: The data from scrum_list.json
    :return: NONE
    """

    current_data[channel_id] = team_id


if __name__ == "__main__":
    main()
