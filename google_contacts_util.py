#!/usr/bin/python2.5

# Requires that the gdata library have been previously installed
# See http://code.google.com/apis/contacts/docs/1.0/developers_guide_python.html 
# for the gdata library
import gdata.contacts
import gdata.contacts.service

class ContactsFetcher(object):
  """Class to fetch contacts from Google.

     This class can be imported into a handler or other view that has an
     authenticated Google data client (gd_client). An authenticated Google data
     client can be passed in as below and the contacts for that Google Account
     will be returned.

     Example:
     import ContactsFetcher
     #assume you have code here to authenticate a Google Data client

     cf = ContactsFetcher(gd_client)
     contacts = cf.get_contacts()
  """
  contacts = []

  def __init__(self, gd_client):
    self.gd_client = gd_client
        
  def groups_feed(self, feed, ctr):
    if not feed.entry:
      return 0

    for i, entry in enumerate(feed.entry):
      [self.contacts.append(ent.address) for ent in entry.email]

  def get_paginated_feed(self, feed, print_method):
    ctr = 0
    while feed:
      ctr = print_method(feed=feed, ctr=ctr)
      next = feed.GetNextLink()
      feed = None
      if next:
        feed = self.gd_client.GetContactsFeed(next.href)

  def get_contacts(self):
     """Retrieve a list of contacts and return name and primary email."""

      feed = self.gd_client.GetContactsFeed()
      self.get_paginated_feed(feed, self.groups_feed)
      return self.contacts
