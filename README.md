# Google Calendar Integration

This Django app provides integration with the Google Calendar API using the OAuth2 mechanism. It provides two API endpoints to initiate the OAuth2 flow and retrieve the user's calendar events.

## Prerequisites

- Python 3.6 or higher
- Django 3.1 or higher
- `google-auth` and `google-api-python-client` packages installed

## Installation

1. Clone the repository: `git clone https://github.com/itsmohitnamdeo/GoogleCalendarIntegration`
2. Install the required packages: `pip install -r requirements.txt`
3. Upload your Google API client secret JSON file.
4. Run the Django migrations: `python manage.py migrate`

## Usage

### API Endpoints

- `/rest/v1/calendar/init/`: This endpoint starts step 1 of the OAuth2 flow, prompting the user for their credentials.
- `/rest/v1/calendar/redirect/`: This endpoint handles the redirect request sent by Google with the authorization code, and retrieves the access token to get the user's calendar events.

### Starting the OAuth2 Flow

To start the OAuth2 flow, make a GET request to `/rest/v1/calendar/init/` endpoint. This will redirect the user to Google's authorization page, where they can grant the application access to their Google Calendar.

### Handling the Redirect

After the user grants access to their Google Calendar, Google will redirect the user to the redirect URI set in the Google API console. This URI should be set to `/rest/v1/calendar/redirect/`.

The `GoogleCalendarRedirectView` class retrieves the authorization code from the request parameters and exchanges it for an access token using the `google-auth` and `google-api-python-client` packages.

If the access token is successfully retrieved, it is used to get the user's calendar events from Google Calendar. The events are returned as a JSON response.

