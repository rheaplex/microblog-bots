#!/usr/bin/env python

# cybernetic_critic.py - Post aesthetic critiques.
# Copyright (C) 2011, 2015 Rhea Myers rhea@myers.studio
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

import datetime
import pickle

import microblog_bot
from aesthetic import critique_artwork, describe_aesthetic, \
    make_aesthetic, update_aesthetic

################################################################################
# The bot
################################################################################

class CyberneticCriticMicroblogger(microblog_bot.MicroblogFollowerBot):
    """A microblog bot that posts aesthetic critiques"""

    CURRENT_DAY = 'current_day'
    AESTHETIC = 'critical_aesthetic'

    def db_set_aesthetic(self):
        """Serialize the aesthetic to the database"""
        self.db_set(CyberneticCriticMicroblogger.AESTHETIC,
                    pickle.dumps(self.aesthetic, 0))

    def generate_comment(self, message):
        """Generate an aesthetic critique to post"""
        return critique_artwork(message['text'], self.aesthetic,
                                "http://identi.ca/notice/%s" % message['id'])

    def post_aesthetic(self):
        """Post updates describing the current aesthetic"""
        good, bad = describe_aesthetic(self.aesthetic)
        desc = ' '.join((good, bad))
        if len(desc) <= 140:
            self.api.PostUpdate(desc)
        else:
            if len(good) > 140:
                good = "%s..." % good[:137]
            self.api.PostUpdate(good)
            if len(bad) > 140:
                bad = "%s..." % bad[:137]
            self.api.PostUpdate(bad)

    def load_aesthetic(self):
        """Load the aesthetic from the db, or create a new one on first run"""
        # Get the aesthetic from the DB
        self.aesthetic = self.db_get(CyberneticCriticMicroblogger.AESTHETIC)
        if self.aesthetic:
            self.aesthetic = pickle.loads(self.aesthetic)
        else:
            self.aesthetic = make_aesthetic()
            self.db_set_aesthetic()

    def load_previous_time(self):
        """Load the previous run time from the database"""
        self.previous = self.db_get(CyberneticCriticMicroblogger.CURRENT_DAY)
        if self.previous:
            self.previous = pickle.loads(self.previous)
        else:
            self.previous = datetime.date(1970, 1, 1)

    def update_aesthetic(self):
        """Update the aesthetic"""
        now = datetime.date.today()
        # This will update the aesthetic on first run. This is wasteful but ok
        if now > self.previous:
            self.db_set(CyberneticCriticMicroblogger.CURRENT_DAY,
                        pickle.dumps(now, 0))
            update_aesthetic(self.aesthetic)
            self.db_set_aesthetic()
            self.post_aesthetic()

    def update_state(self):
        """Update the aesthetic"""
        self.load_previous_time()
        self.load_aesthetic()
        self.update_aesthetic()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(CyberneticCriticMicroblogger)
