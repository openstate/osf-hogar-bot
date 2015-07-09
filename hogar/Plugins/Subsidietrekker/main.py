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

    return ['sub']


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

    logger.info(u'Got subsidie trekker command : %s' % (message,))

    output = u''
    base_url = 'http://www.subsidietrekker.nl/allesubsidies/api.php?draw=2&columns%%5B0%%5D%%5Bdata%%5D=0&columns%%5B0%%5D%%5Bname%%5D=Ministerie&columns%%5B0%%5D%%5Bsearchable%%5D=false&columns%%5B0%%5D%%5Borderable%%5D=true&columns%%5B0%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B0%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&columns%%5B1%%5D%%5Bdata%%5D=1&columns%%5B1%%5D%%5Bname%%5D=Regeling&columns%%5B1%%5D%%5Bsearchable%%5D=false&columns%%5B1%%5D%%5Borderable%%5D=true&columns%%5B1%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B1%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&columns%%5B2%%5D%%5Bdata%%5D=2&columns%%5B2%%5D%%5Bname%%5D=Ontvanger&columns%%5B2%%5D%%5Bsearchable%%5D=true&columns%%5B2%%5D%%5Borderable%%5D=true&columns%%5B2%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B2%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&columns%%5B3%%5D%%5Bdata%%5D=3&columns%%5B3%%5D%%5Bname%%5D=Beleid&columns%%5B3%%5D%%5Bsearchable%%5D=false&columns%%5B3%%5D%%5Borderable%%5D=true&columns%%5B3%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B3%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&columns%%5B4%%5D%%5Bdata%%5D=4&columns%%5B4%%5D%%5Bname%%5D=Realisatie&columns%%5B4%%5D%%5Bsearchable%%5D=false&columns%%5B4%%5D%%5Borderable%%5D=true&columns%%5B4%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B4%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&columns%%5B5%%5D%%5Bdata%%5D=5&columns%%5B5%%5D%%5Bname%%5D=Jaar&columns%%5B5%%5D%%5Bsearchable%%5D=false&columns%%5B5%%5D%%5Borderable%%5D=true&columns%%5B5%%5D%%5Bsearch%%5D%%5Bvalue%%5D=&columns%%5B5%%5D%%5Bsearch%%5D%%5Bregex%%5D=false&order%%5B0%%5D%%5Bcolumn%%5D=0&order%%5B0%%5D%%5Bdir%%5D=asc&start=0&length=200&search%%5Bvalue%%5D=%s&search%%5Bregex%%5D=false&_=1436438498008'
    url = u''
    params = {}

    # Get the message contents
    text = message['text']

    results = []

    # Remove a mention. This could be the case
    # if the bot was mentioned in a chat room
    if text.lower().startswith('sub '):
        text = text[4:]
        url = base_url % (text,)

        try:
            results = requests.get(url).json()
        except Exception as e:
            results = []

    if len(results) <= 0:
        return 'No subsidies were found.'

    total = sum([float(r[4]) for r in results['data']])

    output = u'%s subsidies found for a total of %s ' % (
        results['recordsFiltered'], total,)

    return output
