#!/usr/bin/python2.5

"""This util provides 3 functions for generating and checking a salted password.

   A relevant article on this topic of salting can be found here:  http://www.codinghorror.com/blog/2007/09/youre-probably-storing-passwords-incorrectly.html
   Given their conclusion that one shouldn't roll your own security, this might
   be inappropriate. Still fun learning!
"""

import base64
import datetime
import hashlib
import random
import string

def create_salt(length=8):
  chars = string.letters + string.digits
  return ''.join([random.choice(chars) for i in range(length)])

def generate_salted_password(raw_password):
  salt = create_salt()
  salted_pass = base64.b64encode((salt+raw_password))  
  sha1 = hashlib.sha1()
  sha1.update(salted_pass)
  return sha1.digest()

def check_password(raw_trial_password, encrypted_pass, salt):
  salted_trial_pass = base64.b64encode((salt+raw_trial_password))
  sha1 = hashlib.sha1()
  sha1.update(salted_trial_pass)
  return sha1.digest() == encrypted_pass
