# [Small URL](https://smallurl-server.onrender.com)

This project implements a TinyURL generator web application using Django, a Python web framework. Users can input or paste YouTube video links, and the system generates a short/tiny URL for easy sharing. Additionally, the application provides features to view recently pasted video embeds and track access logs.

You can find the application **[here](https://smallurl-server.onrender.com)**

**Note**: Navigating the hosted application may experience a significant delay in the initial load due to the application emerging from quarantine on the Render platform.


## Features

1. **Input YouTube Link Page**: Users can input or paste YouTube video links on this page.

2. **TinyURL Generation**: Upon submission of a YouTube link, the system generates a short/tiny URL that users can share with others.

3. **Recently Pasted Videos Page**: Users can access a page that displays recently pasted video embeds. Clicking on an embed plays the video in the embedded player.

4. **Access Logs Page**: The application provides a page to track when a link was accessed, sorted by time and accompanied by IP addresses.


## Tech Stack used

- Django (Python Web Framework)
- HTML (Frontend)
- Bootstrap (Frontend Styling)
- PostgreSQL (Database for production)
- Render (Deployment Platform)


## Project Setup

To get this project up and running locally on your computer follow the following steps.

1. Clone this repository to your local machine.
2. Create a python virtual environment and activate it. We have used Poetry here.
3. Open up your terminal and run the following command to install the packages used in this project.


```
$ pip install poetry
$ poetry install
```

4. Set up a Postgres database for the project.
5. Rename the `.env.example` file found in the root directory of the project to `.env` and update
   the environment variables accordingly.
6. Run the following commands to setup the database tables and create a super user.

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

7. Run the development server using:

```
$ python manage.py runserver
```

8. Open a browser and go to http://localhost:8000/.

## More Info

- Implemention of Encryption on generated urls is not done.
- Authentication is not implmeneted in this project.

## License

Usage is provided under the [MIT License](http://opensource.org/licenses/mit-license.php). See LICENSE for the full details.