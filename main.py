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
import logging
from array import *

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

def clrs2_2_2(n, myList):
	for j in range(0, n-1, 1):
		key = j
		logging.debug("for j=%s", str(j))
		for i in range(j+1, n, 1):
			logging.debug("for i=%s", str(i))
			if myList[i] < myList[key]:
				logging.debug("key=%s", str(key))
				key = i
		if key>j:
			logging.debug("switch key=%s|j=%s", str(key), str(j))
			temp = myList[j]
			myList[j] = myList[key]
			myList[key] = temp
	return myList

def clrs2_3_5r(size, start, end, myList, value):
	logging.debug("start=%s|end=%s", str(start), str(end))
	if start > end:
		return
	
	h = (end + start) / 2
	logging.debug("h=%s|myList[h]=%s", str(h), str(myList[h]))
	if (myList[h] == value):
		logging.debug("SUCCESS")
		return h
	if myList[h] < value:
		logging.debug("upper")
		ret = clrs2_3_5r(size, h+1, end, myList, value)
	else:
		logging.debug("lower")
		ret = clrs2_3_5r(size, start, h-1, myList, value)
	return ret

def clrs2_3_5i(size, start, end, myList, value):
	if start > end:
		return

	if value > myList[end] or value < myList[start]:
		return
	
	while (end - start) > 0:
		logging.debug("start=%s|end=%s", str(start), str(end))
		if end - start == 1:
			if myList[start] == value:
				return start
			elif myList[end] == value:
				return end
			else:
				return
		
		mid = (end + start) / 2
		logging.debug("mid=%s|myList[mid]=%s", str(mid), str(myList[mid]))
		
		if (myList[mid] == value):
			logging.debug("SUCCESS")
			return mid
		elif myList[mid] < value:
			logging.debug("upper")
			start = mid
		else:
			logging.debug("lower")
			end = mid

	return

def clrs2_3_5ii(size, start, end, A, value):
	while start < end:
		logging.debug("start=%s|end=%s", str(start), str(end))

		mid = (end + start) / 2
		logging.debug("mid=%s|A[mid]=%s", str(mid), str(A[mid]))
		
		if value == A[mid]:
			logging.debug("SUCCESS")
			return mid
		elif value > A[mid]:
			logging.debug("upper")
			start = mid + 1
		else:
			logging.debug("lower")
			end = mid - 1

	return
	
def dump_array(output, size, myList):
	logging.debug("%s dump_array myList: %s,%s,%s,%s,%s", output, str(myList[0]), str(myList[1]), str(myList[2]), str(myList[3]), str(myList[4]))
	
def dump_leftArray(size, leftArray):
	logging.debug("dump_array leftArray[%s]: %s,%s", size, str(leftArray[0]), str(leftArray[1]))

def dump_rightArray(size, rightArray):
	logging.debug("dump_array rightArray[%s]: %s,%s", size, str(rightArray[0]), str(rightArray[1]))
	
def clrs_merge(size, p, q, r, myList):
	dump_array("clrs_merge START", size, myList)
	logging.debug("clrs_merge:p=%s|q=%s|r=%s", str(p), str(q), str(r))

	leftSize = q-p+1+1
	leftArray = [0] * leftSize
	for i in range(0, leftSize):
		leftArray[i]=myList[p+i]
	leftArray[i]=10000
	dump_leftArray(leftSize, leftArray)
	
	rightSize = r-q+1
	rightArray = [0] * rightSize
	for j in range(0, rightSize):
		rightArray[j]=myList[q+1+j]
	rightArray[j]=10000
	dump_rightArray(rightSize, rightArray)
	
	i = 0
	j = 0
	rightSize -= 1
	leftSize -= 1
	for k in range(p, r):
		if leftSize == 0:
			myList[k] = rightArray[j]
			j += 1
			rightSize -= 1
		elif rightSize == 0:
			myList[k] = leftArray[i]
			i += 1
			leftSize -= 1
		elif leftArray[i] < rightArray[j]:
			myList[k] = leftArray[i]
			i += 1
			leftSize -= 1
		else:
			myList[k] = rightArray[j]
			j += 1
			rightSize -= 1
	
	dump_array("clrs_merge END", size, myList)	
	return myList

def clrs_merge_sort(size, p, r, myList):
	if p >= r:
		logging.debug("Do not enter clrs_merge_sort:p=%s|r=%s", str(p), str(r))
		return myList
		
	q = (p + r)/2
	dump_array("clrs_merge_sort START", size, myList)	
	logging.debug("clrs_merge_sort:p=%s|q=%s|r=%s", str(p), str(q), str(r))
	dump_array("Before 1. clrs_merge_sort", size, myList)	
	clrs_merge_sort(size, p, q, myList)
	dump_array("Before 2. clrs_merge_sort", size, myList)	
	clrs_merge_sort(size, q + 1, r, myList)
	clrs_merge(size, p, q, r, myList)

	dump_array("clrs_merge_sort END", size, myList)
	return myList
	
class MainHandler(webapp2.RequestHandler):
	def write_form(self, username="", username_error="", password_error="", verify_error="", email="", email_error=""):
		self.response.write(form % {"username": username,
									"username_error": username_error,
									"password_error": password_error,
									"verify_error": verify_error,
									"email": email,
									"email_error": email_error})
	
	logging.debug("***MainHandler***")
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
			
class clrs2_2_2Handler(webapp2.RequestHandler):
	def get(self):
		logging.debug("***clrs2_2_2Handler***")
		myArray = array('i',[4, 5, 1, 3, 2])
		self.response.write("clrs2_2_2: Array %(Array1)s sorted to "%{"Array1":myArray})
		sortedArray = clrs2_2_2(5, myArray)
		#sortedArray = myArray
		self.response.write("Array %(Array2)s."%{"Array2":sortedArray})

class clrs2_3_5rHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug("***clrs2_3_5rHandler***")
		myArray = array('i',[1, 3, 7, 9, 10, 12, 25])
		self.response.write("clrs2_3_5r: Value 25 found in array %(Array1)s sorted to "%{"Array1":myArray})
		index = clrs2_3_5r(7, 0, 6, myArray, 25)
		logging.debug("received index=%s", index)
		if index >= 0:
			index = int(index)
			index += 1
			logging.debug("modified index=%s", str(index))
		self.response.write("Position %(Array2)s."%{"Array2":index})

class clrs2_3_5iHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug("***clrs2_3_5iHandler***")
		myArray = array('i',[1, 3, 7, 9, 10, 12, 25])
		self.response.write("clrs2_3_5i: Value 25 found in array %(Array1)s sorted to "%{"Array1":myArray})
		index = clrs2_3_5i(7, 0, 6, myArray, 25)
		logging.debug("received index=%s", index)
		if index >= 0:
			index = int(index)
			index += 1
			logging.debug("modified index=%s", str(index))
		self.response.write("Position %(Array2)s."%{"Array2":index})

class clrs_merge_sortHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug("***clrs_merge_sortHandler***")
		myArray = array('i',[5, 4, 3, 1, 2])
		self.response.write("clrs_merge_sort: Array %(Array1)s sorted to "%{"Array1":myArray})
		sortedArray = clrs_merge_sort(5, 0, 4, myArray)
		#sortedArray = myArray
		self.response.write("Array %(Array2)s."%{"Array2":sortedArray})

		
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Welcome, %(username)s."%{"username":welcome_user})
		
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/clrs2_2_2', clrs2_2_2Handler),
	('/clrs2_3_5r', clrs2_3_5rHandler),
	('/clrs2_3_5i', clrs2_3_5iHandler),
	('/clrs_merge_sort', clrs_merge_sortHandler),
	('/welcome', WelcomeHandler)
], debug=True)
