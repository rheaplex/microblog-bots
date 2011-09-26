#!/usr/bin/env python

# cybernetic_collector.py - Buy masterpieces.
# Copyright (C) 2011  Rhea Myers rhea@myers.studio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################################
# Imports
################################################################################

import re

import microblog_bot

################################################################################
# The bot
################################################################################

class CyberneticCollectorMicroblogger(microblog_bot.MicroblogFollowerBot):
    """A microblog bot that buys masterpieces"""

    def should_comment(self, message):
        # Don't call super.should_comment(), as we're commenting on a message
        # with an in_reply_to_user_id
        return message.text.find("is a masterpiece") != -1
    
    def generate_comment(self, message):
        """Generate an aesthetic critique to post"""
        url = re.search("(http://[^ ]+)", message.text).group(1)
        return "I just bought %s" % url

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(CyberneticCollectorMicroblogger)
