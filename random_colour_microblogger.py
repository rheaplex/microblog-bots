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
from utilities import call_one_of, concatenate_string, maybe, choose

################################################################################
# Colour description
################################################################################

def hue ():
    return choose("red", "orange", "yellow", "green", "blue", 
                          "purple")

def saturation ():
    return choose("very pale", "pale", "greyish",
                          "moderately saturated", "strongish", 
                          "strong", "vivid")

def brightness ():
    return choose("very dark", "dark", "medium", "light", 
                          "very light")

def in_between_hue ():
    return choose("orangish red", "reddish orange", 
                          "yellowish orange", "orangeish yellow", 
                          "greenish yellow", "yellowish green", 
                          "bluish green", "greenish blue", 
                          "purplish blue", "bluish purple", 
                          "reddish purple", "purplish red")

def hsv ():
    return "%s %s %s" % (brightness(), saturation(),
                         call_one_of(hue, in_between_hue))
    
def combined_hsv ():
    return choose("white", "black", "grey")

def gloss ():
    return choose("very matt", "matt", "silk", "silky", "glossy",
                          "very glossy")

def highlight_colour ():
    return choose("plastic", "metallic")

def polish ():
    return choose("very polished", "polished", "rough",
                          "very rough")

def transparency ():
    return choose("transparent", "nearly transparent",
                          "semi-transparent", "nearly opaque", "opaque")

def glow ():
    return choose("very faintly glowing", "faintly glowing",
                          "glowing", "brightly glowing", 
                          "very brightly glowing")

def random_colour ():
    # combined-hsv needs to be much lower probability
    if random.random() < 0.95:
        hsv_to_use = hsv
    else:
        hsv_to_use = combined_hsv
    return concatenate_string(maybe(glow, 0.05),
                              maybe(transparency, 0.05),
                              maybe(polish, 0.05),
                              maybe(highlight_colour, 0.05),
                              maybe(gloss, 0.05),
                              hsv_to_use())

################################################################################
# The bot
################################################################################

class RandomColourMicroblogger(microblog_bot.MicroblogBot):
    """A microblog bot that posts random colour descriptions"""

    def generate_update(self):
        """Generate a random colour description to post"""
        return random_colour()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(RandomColourMicroblogger)
