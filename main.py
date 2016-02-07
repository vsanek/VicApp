#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

welcome_user = ""

form="""
<form method="post">
	Signup
	<br>
	<label>
		Username 
		<input type="text" name="username" value="%(username)s"><div style="color: red">%(username_error)s</div>
	</label>
	<br>
	
	<label>
		Password
		<input type="password" name="password" value=""><div style="color: red">%(password_error)s</div>
	</label>
	<br>

	<label>
		Verify Password
		<input type="password" name="verify" value=""><div style="color: red">%(verify_error)s</div>
	</label>
	<br>

	<label>
		Email (optional)
		<input type="text" name="email" value="%(email)s"><div style="color: red">%(email_error)s</div>
	</label>

	<br>
	<br>
	<br>	
	<input type="submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)
	
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USERNAME_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASSWORD_RE.match(password)

def valid_verify(verify):
	return PASSWORD_RE.match(verify)

def valid_match(password, verify):
	if (password == verify):
		return True
	else:
		return False

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	if not email:
		return True
	return EMAIL_RE.match(email)
	
class MainHandler(webapp2.RequestHandler):
	def write_form(self, username="", username_error="", password_error="", verify_error="", email="", email_error=""):
		self.response.write(form % {"username": username,
									"username_error": username_error,
									"password_error": password_error,
									"verify_error": verify_error,
									"email": email,
									"email_error": email_error})
		
	def get(self):
		self.write_form()

	def post(self):
		global welcome_user
		
		user_username = self.request.get('username')
		user_password = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')

		username = valid_username(user_username)
		password = valid_password(user_password)
		verify = valid_verify(user_verify)
		passwords_match = valid_match(user_password, user_verify)
		email = valid_email(user_email)

		username_error = ""
		password_error = ""
		verify_error = ""
		email_error = ""
		
		iWelcome = 1
		if not (username):
			username_error = "That's not a valid username."
			iWelcome = 0
		if not (password):
			password_error = "That's not a valid password."
			iWelcome = 0
		if not (verify):
			verify_error = "That's not a valid password."
			iWelcome = 0
		if not (passwords_match):
			verify_error = "Yur passwords didn't match."
			iWelcome = 0
		if not (email):
			email_error = "That's not a valid email."
			iWelcome = 0
		
		if(iWelcome == 0):
			self.write_form(user_username, username_error, password_error, verify_error, user_email, email_error)
		else:
			welcome_user = user_username
			self.redirect("/welcome")
			

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Welcome, %(username)s."%{"username":welcome_user})
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', WelcomeHandler)
], debug=True)
