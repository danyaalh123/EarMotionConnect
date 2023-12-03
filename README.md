
# EarMotion Connect

EarMotion Connect provides a user interface to show real time data from the EarMotion v1 EEG Sensors. Using the Spotify Web API, it controls playlist playback based on the data and shows the currently playing music on the dashboard. This project utilises an open-source Flask/Jinja Template, based on a modern Bootstrap 5 dashboard design. 

## Initial Setup

1. **Configure Spotify API Credentials**:
   - Obtain your Spotify API credentials (Client ID and Client Secret) from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/). For the Spotify Redirect URL, use your_flask_app_url/redirect.html.
   - Create a `.env` file in the root of the project with the following content, replacing the placeholders with your actual credentials:
     ```
     # General Flask configuration
     DEBUG=False
     FLASK_APP=run.py
     FLASK_ENV=development
     ASSETS_ROOT=/static/assets

     # Spotify API configuration
     SPOTIFY_CLIENT_ID=your_spotify_client_id_here
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
     SPOTIFY_REDIRECT_URL=your_spotify_redirect_url_here
     ```

2. **Install Dependencies**:
   - Set up a virtual environment and install dependencies:
     ```bash
     $ virtualenv env
     $ source env/bin/activate  # On Unix or MacOS
     $ .\env\Scripts\activate  # On Windows
     $ pip3 install -r requirements.txt
     ```

3. **Run the Application**:
   - Start the Flask application:
     ```bash
     $ flask run
     ```
   - The app will be running at `http://127.0.0.1:5000/`.

## Code-base Structure

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |-- __init__.py
   |    |-- config.py
   |    |-- views.py
   |    |-- static/
   |    |    |-- <css, JS, images>
   |    |-- templates/
   |         |-- home/
   |         |    |-- index.html
   |         |    |-- page-403.html
   |         |    |-- page-404.html
   |         |    |-- page-500.html
   |         |    |-- profile.html
   |         |    |-- redirect.html
   |         |-- includes/
   |         |    |-- navigation.html
   |         |    |-- sidebar.html
   |         |    |-- scripts.html
   |         |    |-- footer.html
   |         |-- layouts/
   |         |    |-- base.html
   |         |    |-- base-fullscreen.html
   |
   |-- requirements.txt
   |-- run.py
   |-- ************************************************************************
```

---

EarMotion Connect - An open-source project based on Flask/Jinja.
