# ScrumPoster
A Python tool to post daily scrum message to multiple channels in Mattermost. This tool is designed to run independantly without any user interaction apart from initial setup inside an Alpine Linux Docker Container.

## Components
1. ChannelAdd.py
2. ScrumPoster.py
3. Dockerfile
4. cronSchedule.txt

## Folder Structure
```
.  
|  
|__ TeamFinder.py  
|  
|__ ScrumPoster.py  
|
|__ Dockerfile
|
|__ cronSchedule.txt
|  
|__ config 
|   |  
|   |__ config.json  
|  
|__ scrum_list  
    |  
    |__ scrum_list.json  
```

## File Descriptions

* ScrumPoster.py
    * This file is responsible for actually posting the scrum messages in the channels
    * It reads the team and channel ids from the scrum_list.json file and uses them to post scrum message to the channels

* ChannelAdd.py
    * This file monitors the teams and the channels the user account specified inside the the config file is a part of.
    * If the user account is added to a new channel, the file automatically adds the channel and team id to scrum_list.json file

* Dockerfile
    * This file contains the blueprint for the docker container that houses the python scripts

* cronSchedule.txt
    * This file contains the details for scheduling the cron jobs for the python scripts

* config.json
    * This file contains the credentials for the user account that is used for posting scrum messages (Preferably the user account is a separate dedicated acoount)

* scrum_list.json
    * This file contains the list of channels and teams the user specified in config.json is a part of for posting daily scrum messages

## Initial Setup
* Clone the repository from GitHub
* Copy the folder 'Containerized' onto the machine which is going to host the docker container
* Open the config.json file and specify the user credentials that is going to be used for psoting on Mattermost
* Build the docker image using the Dockerfile
    * Example Command `docker build PATH-TO-DOCKERFILE -t IMAGE-NAME`
* Start the docker container using the docker image from previous step
    * Example Command `docker run -dt IMAGE-NAME`

## Adding a new channel to the list
* Just add the user specified inside the config file to the new channel and that's it. ChannelAdd.py will add the new channel to the scrum_list.json

## Future Improvements
* Migrating over from mattermostapi package to mattermostdriver package for cleaner code base
* Replacing v3 API enpoints with v4 API endpoints

## Author
**Nosherwan Ahmed**

## Contributing
Feel free to file a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

