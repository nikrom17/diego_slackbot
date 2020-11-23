import os
import time

from requests_oauthlib import OAuth2Session

slack_token = os.environ.get("DIEGO_SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("DIEGO_SLACK_SIGNING_SECRET")

microsoft_app_secret = os.environ.get("DIEGO_MICROSOFT360_CLIENT_SECRET") 
microsoft_app_id = os.environ.get("DIEGO_MICROSOFT360_CLIENT_ID") 
microsoft_calendar_id = os.environ.get("DIEGO_UIFW_CALENDAR_ID")

microsoft_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'



def store_token(request, token):
      request.session['oauth_token'] = token

def get_token(request):
  token = request.session['oauth_token']
  if token != None:
    # Check expiration
    now = time.time()
    # Subtract 5 minutes from expiration to account for clock skew
    expire_time = token['expires_at'] - 300
    if now >= expire_time:
      # Refresh the token
      aad_auth = OAuth2Session(microsoft_app_id,
        token = token,
        scope="openid profile offline_access user.read calendars.read",
        redirect_uri="https://bb1cd90109c0.ngrok.io/callback")

      refresh_params = {
        'client_id': microsoft_app_id,
        'client_secret': microsoft_app_secret,
      }
      new_token = aad_auth.refresh_token(microsoft_token_url, **refresh_params)

      # Save new token
      store_token(request, new_token)

      # Return new access token
      return new_token

    else:
      # Token still valid, just return it
      return token