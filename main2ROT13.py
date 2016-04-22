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

form="""
<form method="post" name="myForm">
	<textarea name="text" style="width:300px; height: 300px">
	%(text)s
	</textarea>
	<br>	
	<input type="submit">
</form>
"""
def escape_html(s):
    return cgi.escape(s, quote = True)

char_table = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}

def new_c (c):
	lower_c = c.lower()
	if(char_table.get(lower_c)):

		if(c.islower()):
			i_lower = 1
		else:
			i_lower = 0

		new_i = char_table.get(lower_c) + 13
		if(new_i > 26):
			new_i = new_i - 26
		new_char = char_table.keys()[char_table.values().index(new_i)]

		if(i_lower == 0):
			new_char = new_char.upper()
		return new_char 
	return c

def new_string (string):
	if(string):
		new_string = ""
		for c in string:
			new_string=new_string+new_c(c)
		return new_string
	
class MainHandler(webapp2.RequestHandler):
	def write_form(self, new_text=''):
		self.response.write(form % {"text": new_text})
		
	def get(self):
		self.write_form()

	def post(self):
		user_textarea = self.request.get('text')

		new_text = escape_html(new_string(str(user_textarea)))
		
		self.write_form(new_text)
		
app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
