from . import *

# Disconnect - revoke a current user's token and reset their login_session
@auth.route('/gdisconnect')
def gdisconnect():
  access_token = login_session.get('access_token')
  if access_token is None:
    print('Access Token is None')
    response = make_response(json.dumps('Current user not connected'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  print('In gdisconnect access token is %s', access_token)
  print('User name is: ')
  print(login_session['username'])
  url = 'https://accounts.google.com/o.oauth2/revoke?token=%s' % login_session['access_token']
  h = httplib2.http()
  result = h.request(url, 'GET')[0]
  print('result is ')
  print(result)
  if result['status'] == '200':
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
  else:
    response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
    response.headers['Content-Type'] = 'application/json'
    return response
    