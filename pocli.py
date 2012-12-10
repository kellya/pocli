#!/usr/bin/python
import argparse
import ConfigParser
import httplib2
import json
import sys
import urllib
import urllib2

defaults = {
    ('msgUrl'):'https://api.pushover.net/1/messages.json',
    ('devUrl'):'https://api.pushover.net/1/users/validate.json',
    ('sndUrl'):'https://api.pushover.net/1/sounds.json',
    ('cfFile'):'./pocli.cfg'
}

#These two variables are oddly out of place since this script grew.  FIXME
#url = "https://api.pushover.net/1/messages.json"
http = httplib2.Http()

def read_config(conf):
  """
  Reads in the contents of the file passed through 'conf' and sets
  global variables for them.  This may be better to return a dict
  I'll look into that later FIXME
  """
  global user
  global token
  try:
    config = ConfigParser.RawConfigParser()
    config.read(conf)
    token = config.get('Main', 'token')
    user = config.get('Main', 'user')
  except ConfigParser.NoSectionError, err:
    print 'Error:  Couldn\'t read config'
    sys.exit(2)
  except ConfigParser.ParsingError, err:
    print 'Couldn\'t parse config file: ', err
    sys.exit(99)

def get_sounds():
  "This gets a list of sounds from a JSON call, and outputs it as a string"
  sounds_url = urllib2.urlopen(defaults['sndUrl'])
  sound_list = json.load(sounds_url)
  sounds_url.close()
  all_sounds =""
  if sound_list['status'] != 1:
    all_sounds = "Error: Could not retreive list of sounds"
  else:
    for sounds, value in sound_list['sounds'].iteritems():
      all_sounds=all_sounds + ' ' + sounds
  return all_sounds

def dev_is_valid(checkdev):
  """
  Return True or False based on validation of the device passed
  through checkdev.
  """
  # This is the URL defined in the API docs at 
  # https://pushover.net/api#identifiers
#  url = 'https://api.pushover.net/1/users/validate.json'
  params = urllib.urlencode({
    'user': user,
    'token': token,
    'device': checkdev
  })

  response, content = http.request(defaults['devUrl'], 'POST', params, 
      headers={'Content-Type': 'application/x-www-form-urlencoded'}
  )
  # The URL will return a 200 if it is good, 400 if bad.  This just
  # generically validates 200 and everything else is bad.
  if response.status == 200:
    return True
  else:
    return False

def build_params ():
  """Builds parameters and returns a dictionary
  well ok, fine.  It only throws them in a dictionary w/o logic at the moment
  """
  return {
      'user': user,
      'token': token,
      'title': args.title,
      'message': args.message,
      'sound': args.sound,
      'priority': args.priority,
      'url': args.url
  }


parser = argparse.ArgumentParser(description='Process command line options')
parser.add_argument('-f', '--config', dest='config',
    help='Config file for persistent options (defaults to '+ defaults['cfFile'])
parser.add_argument('-m', '--message', dest='message', required=True,
    help='Specify the message contents.  Needs to be in quotes if you have spaces')
parser.add_argument('-s', '--sound', dest='sound',
    help='Name of the sound, which can be any of the following: '+ get_sounds())
parser.add_argument('-k', '--token', dest='token', 
    help='Application API token (Required, but may be specified in config)')
parser.add_argument('-t', '--title', dest='title',
    help='The title of the message')
parser.add_argument('-u', '--url', dest='url',
    help="Additional URL to append to the message")
parser.add_argument('-p', '--priority', dest='priority',
    help="Priority of the message.  Can be 1 for high, or -1 for silent")
parser.add_argument('-d', '--device', dest='devid',
    help="The specific device to send the message")
args = parser.parse_args()

if args.config is None:
  read_config('./pocli.cfg')
else:
  read_config(args.config)

if args.devid is not None:
  dev_is_valid(args.devid)

params = urllib.urlencode(build_params())
#params = urllib.urlencode({
#  'user': user,
#  'token': token,
#  'title': args.title,
#  'message': args.message,
#  'sound': args.sound,
#  'priority': args.priority,
#  'url': args.url
#})

response, content = http.request(defaults['msgUrl'], 'POST', params,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
