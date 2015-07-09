# The MIT License (MIT)
#
# Copyright (c) 2015 Leon Jacobs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

''' This provides commands for the politwoops bot '''

import requests

from hogar.static import values as static_values

from hogar.Models.Base import db
from hogar.Models.Logger import Logger

import logging
logger = logging.getLogger(__name__)


def applicable_types():

    '''
        Applicable Types

        Returns the type of messages this plugin is for.
        See: hogar.static.values

        --
        @return list
    '''

    #return ['text']
    return static_values.possible_message_types


def commands():

    '''
        Commands

        In the case of text plugins, returns the commands
        that this plugin should trigger for. For other
        message types, a empty list should be returned.

        If your plugin applies to any command (in the
        case of text messages), simply supply the a
        wildcard in the list ie. ['*']

        --
        @return list
    '''

    return ['dt']


def should_reply():

    '''
        Should Reply

        Specifies wether a reply should be sent to the original
        sender of the message that triggered this plugin.

        --
        @return bool
    '''

    return True


def reply_type():

    '''
        Reply Type

        Specifies the type of reply that should be sent to the
        sender. This is an optional function. See hogar.static.values
        for available types.

        --
        @return str
    '''

    return 'text'


def run(message):

    '''
        Run

        Run the custom plugin specific code. A returned
        string is the message that will be sent back
        to the user.

        --
        @param  message:dict    The message sent by the user

        @return str
    '''

    logger.info(u'Got politwoops command : %s' % (message,))

    output = u''
    base_url = 'http://www.politwoops.com/'
    url = u''
    params = {}

    # Get the message contents
    text = message['text']

    # Remove a mention. This could be the case
    # if the bot was mentioned in a chat room
    if text.lower().startswith('dt @'):
        text = text[4:]
        url = u'%suser/%s.json' % (base_url, text,)
    else:
        url = u'%ssearch.json' % (base_url,)
        params = {'q': text[3:]}

    try:
        result = requests.get(url, params=params).json()
    except Exception as e:
        result = None

    if result is None:
        return 'Nothing was found.'

    try:
        tweet = result[0]
    except IndexError as e:
        tweet = None

    if tweet is None:
        return 'Nothing was found.'

    link = u'%stweet/%s' % (base_url, tweet['id'],)
    output = u'%s: %s -- %s' % (
        tweet['user_name'], tweet['content'], link,)

    return output
