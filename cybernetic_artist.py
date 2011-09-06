#!/usr/bin/env python

# random_colour_microblogger.py - Post random colour descriptions.
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

import random

import microblog_bot
from aesthetic import generate_description

################################################################################
# The bot
################################################################################

class CyberneticArtistMicroblogger(microblog_bot.MicroblogBot):
    """A microblog bot that posts random aesthetic descriptions"""

    def generate_update(self):
        """Generate a random aesthetic description to post"""
        return generate_description()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(CyberneticArtistMicroblogger)
