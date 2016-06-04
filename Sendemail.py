
from urllib import urlencode
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import httplib2

MAILGUN_DOMAIN_NAME = 'garvitbansal244.appspot.com'
MAILGUN_API_KEY = 'key-5aa6e78db5de8b9d245c9fb7cf9a5664'

class MailHandler(webapp.RequestHandler):
   def post(self):
    user_address = self.request.get('email')
    user_name = self.request.get('client_name')
    message_body = self.request.get('message')
    to = 'garvitbansal244@gmail.com'

    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    url = "https://api.mailgun.net/v3/"+MAILGUN_DOMAIN_NAME+"/messages"
    data = {
            "from": user_address,
            "to": to,
            "subject": "Message from " + user_name,
            "text": message_body
        }
    acknowledge_data = {
        "from": to,
        "to": user_address,
        "subject": "Message successfully send to Garvit Bansal",
        "text": message_body
    }
    resp, content = http.request(url, 'POST', urlencode(data))
    if resp.status == 200:
        http.request(url, 'POST', urlencode(acknowledge_data))
    else:
        http.request(url, 'POST', urlencode("Error in sending Mail"))

    self.redirect('/')


def email_message():
    application = webapp.WSGIApplication ([('/send-email', MailHandler)], debug=True)
    util.run_wsgi_app (application)

if __name__ == '__main__':
  email_message ()