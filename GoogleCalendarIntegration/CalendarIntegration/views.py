from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.errors
import googleapiclient.discovery
import urllib.parse

class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            'client_secret.json', 
            scopes=[
                'https://www.googleapis.com/auth/calendar.readonly',
                'https://www.googleapis.com/auth/calendar.events.readonly'
            ],
            redirect_uri=request.build_absolute_uri(reverse('calendar_redirect'))
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return HttpResponseRedirect(auth_url)

class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        try:
            code = request.GET.get('code', None)
            if code:
                flow = Flow.from_client_secrets_file(
                    'client_secret.json', 
                    scopes=[
                        'https://www.googleapis.com/auth/calendar.readonly',
                        'https://www.googleapis.com/auth/calendar.events.readonly'
                    ],
                    redirect_uri=request.build_absolute_uri(reverse('calendar_redirect'))
                )
                flow.fetch_token(code=code)
                creds = flow.credentials

                # Create an authorized API client
                service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
                events_result = service.events().list(calendarId='primary', timeMin='2022-01-01T00:00:00Z',
                                                      maxResults=10, singleEvents=True, orderBy='startTime').execute()
                events = events_result.get('items', [])

                if not events:
                    return Response({'message': 'No events found.'})
                else:
                    return Response(events)
            else:
                return Response({'message': 'Code not found in request.'})
        except Exception as e:
            return Response({'message': 'An error occurred: {}'.format(str(e))})
