#!/usr/bin/python
import argparse
import ConfigParser
import httplib2
import json
import sys
import urllib
import urllib2

# Set the defaults, these shouldn't really change, but could be moved to
# the config file if that makes sense
# msgUrl = the URL used to post messages to pushover API
# devUrl = the URL for device validation to pushover API
# sndUrl = the URL to get the list of sounds supportted by the pushover API
# cfFile = the default location for the config file
# FIXME: The cfFile could be a dictionary of various likely places instead of
#        one, hard-coded value
defaults = {
    ('msgUrl'):'https://api.pushover.net/1/messages.json',
    ('devUrl'):'https://api.pushover.net/1/users/validate.json',
    ('sndUrl'):'https://api.pushover.net/1/sounds.json',
    ('cfFile'):'./pocli.cfg',
}


def read_config(conf):
  """
  Reads in the contents of the file passed through 'conf' and sets
  global variables for them.  This may be better to return a dict
  I'll look into that later FIXME
  """
  # Create an empty dictionary that will be appended w/ the values
  values={}
  try:
    config = ConfigParser.RawConfigParser()
    config.read(conf)
    values['token'] = config.get('Main', 'token')
    user = config.get('Main', 'user')
    values['user'] = config.get('Main', 'user')
    if config.has_option('Main', 'device'):
      values['device'] = config.get('Main', 'device')
  except ConfigParser.NoSectionError, err:
    print 'Error:  Couldn\'t read config'
    sys.exit(2)
  except ConfigParser.ParsingError, err:
    print 'Couldn\'t parse config file: ', err
    sys.exit(99)
  return values

def get_sounds():
  "This gets a list of sounds from a JSON call, and outputs it as a string"
  sounds_url = urllib2.urlopen(defaults['sndUrl'])
  sound_list = json.load(sounds_url)
  sounds_url.close()
  all_sounds =""
  if sound_list['status'] != 1:
    all_sounds = "Error: Could not retrieve list of sounds"
  else:
    for sounds, value in sound_list['sounds'].iteritems():
      all_sounds=all_sounds + ' ' + sounds
  return all_sounds

def dev_is_valid(checkdev, checkuser, checktoken):
  """
  FIXME!!!
  This section isn't currently called, and is broken
  Return True or False based on validation of the device passed
  through checkdev.
  """
  # This is the URL defined in the API docs at 
  # https://pushover.net/api#identifiers
  params = urllib.urlencode({
    'user': checkuser,
    'token': checktoken,
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
  #start with an empty dictionary, and build what we will eventually return
  #FIXME returnval is a bad name since I use it in non-returny ways w/ device
  returnval={}
  parser = argparse.ArgumentParser(description='Process command line options')
  parser.add_argument('-f', '--config', dest='config',
                      help='Config file for persistent options (defaults to '
                      + defaults['cfFile'])
  parser.add_argument('-m', '--message', dest='message', required=True,
                      help='''Specify the message contents.  Needs to be in
                      quotes if you have spaces''')
  parser.add_argument('-s', '--sound', dest='sound',
                      help='''Name of the sound, which can be any of the 
                      following: '''+ get_sounds())
  parser.add_argument('-k', '--token', dest='token', 
                      help='''Application API token (Required, but may be 
                      specified in config)''')
  parser.add_argument('-t', '--title', dest='title',
                      help='The title of the message')
  parser.add_argument('-u', '--url', dest='url',
                      help="Additional URL to append to the message")
  parser.add_argument('-p', '--priority', dest='priority',
                      help='''Priority of the message.  Can be 1 for high, or -1
                      for silent''')
  parser.add_argument('-d', '--device', dest='devid',
                      help="The specific device to send the message")
  parser.add_argument('-n', '--user', dest='user',
                      help="User information")
  parser.add_argument('--timestamp', dest='epochval',
                      help="""Timestamp to set timestamp to a value other than
                      now.  This is passed in epoch format""")
  args = parser.parse_args()
  
  
  if args.token is not None and args.user is not None:
    #if we were given a token and a user information on the commandline, lets
    #use those
    returnval['token']=args.token
    returnval['user']=args.user
  elif args.config is not None:
    #otherwise, we'll try to get them from the config
    returnval=read_config(args.config)
  else:
    #Well they've got to specified somewhere, so die if we get here
    print """
    Error:
    user and token are required.  They either BOTH need to be specified on the
    command line, or BOTH in the config file.  For more information run:
    """
    print sys.argv[0] + " --help\n"
    sys.exit(1)
    
  # Message is required, so argparse is already going to validate it exists
  returnval['message'] = args.message
  
  #I am doing essentially the same thing twice.  This needs cleaned up FIXME
  if args.devid is not None:
    if dev_is_valid(args.devid,returnval['user'],returnval['token']):
      returnval['device'] = args.devid
    else:
      print "Error: Device " + str(args.devid) + " is invalid"
      sys.exit(1)
  if 'device' in returnval:
    #We got a device from config, let's validate it
    if not dev_is_valid(returnval['device'],returnval['user'],returnval['token']):
      print "Error: Device " + str(returnval['device']) + " is invalid"
      sys.exit(1)
      
  # It feels like there may be a better way to loop through this next stuff
  if args.sound is not None:
    returnval['sound'] = args.sound
    
  if args.priority is not None:
    returnval['priority'] = args.priority
    
  if args.title is not None:
    returnval['title'] = args.title
  
  if args.url is not None:
    returnval['url'] = args.url
  
  if args.epochval is not None:
    returnval['timestamp'] = args.epochval
  
  return returnval

http = httplib2.Http()
# This is where we actually make the call to send the message
response, content = http.request(defaults['msgUrl'], 'POST', 
                                 urllib.urlencode(build_params()),
                                 headers={'Content-Type': 
                                          'application/x-www-form-urlencoded'}
)
