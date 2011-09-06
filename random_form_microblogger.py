#!/usr/bin/env python

# random_form_microblogger.py - Post random form descriptions.
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

from utilities import call_one_of, choose, concatenate_string, maybe, \
    maybe_choose, singular
import microblog_bot

################################################################################
# Form description
################################################################################

def scale ():
    "The 3d dimensions of the form"
  # Just have one as more tend to get confusing
    return maybe_choose("massive", "large", "small", "tiny",
                        "fat", "narrow", "slim", "thin", "wide",
                        "shallow", "deep",
                        "tall", "short", "low", "stretched")

def style ():
  "The artistic, design or industrial style of the object",
  return choose("abstract", "art deco", "art brut", "art nouveau",
                "biomechanical", "classical", "conceptual", "cuboidal", 
                "cubist", "curvilinear", "cybernetic", "devotional", "erotic",
                "expressionist", "freeform", "futuristic", "gothic",
                "grunge", "iconic", "impressionist", "international style",
                "kitsch", "mechanistic", "mechanical", "minimalist", "neo-geo",
                "neoclassical", "neoconceptual", "new media", "organic",
                "pop-art", "post-atomic", "post-impressionist", "postmodern",
                "readymade", "rectilinear", "renaissance", "retro-futuristic",
                "robotic", "romanesque", "romantic", "socialist realist",
                "spiky", "streamlined", "surreal", "symbolist", "vernacular")

def qualities ():
    "The object's textural or physical properties"
    return maybe_choose("blurry", "bumpy", "cracked", "crosshatched", "fibrous",
                        "fluorescent", "fractal",
                        "furry", "glazed", "glassy",
                        "halftoned", "iridescent", "jagged", "lumpy",
                        "metallic",
                        "pixellated", "ragged", "rough",
                        "scumbled", "sketchy", "smeary", "smoky", "smooth",
                        "torn",
                        "transparent", "vague", "wooden", "wobbly")

def feel ():
    "The objects emotional or tactile feel"
    return maybe_choose("angry", "alienating", "amusing", "anxious", "brave",
                        "calm", "carefree", "cold",
                        "compassionate", "dejected", "depressing", "desirous",
                        "disgusting", "exciting", "expectant", "fearful",
                        "grieving", "happy", "harsh", "hopeful",
                        "joyful", "loving", "lustful", "melancholy",
                        "nostalgic",
                        "painful", "pleasurable", "proud", "sentimental",
                        "shocking", "surprising", "sympathetic", "tender",
                        "warm")

# Colour(s),  n from cybernetic, optional?

def medium ():
    "The substance of the object"
    return maybe_choose("assemblage", "chocolate", "canvas", "cardboard",
                        "carved", "ceramic",
                        "clay", "collage", "crackle glazed", "fabric", "fat",
                        "felt", "foam rubber",
                        "glass", "glazed", "hessian", "holographic", "ice",
                        "impasto", "marble", "modelling clay", "neon",
                        "painted", "paper", "polished steel",
                        "polychrome steel", "plastic", "relief",
                        "spraycan stencil", "textile ", "wax", "wicker", "wire",
                        "wireframe",
                        "welded steel", "wooden", "woven")

def shape ():
    """The object's shape or form"""
    return choose("anthropomorphic", "architectural", "blobby", "blocky",
                  "conical", "crazy", "cuboidal", "cylindrical", "fractal",
                  "geometrical", "gnarled", "organic",
                  "ovoidal", "flat", "rectilinear", "toroidal", "tubular",
                  "streamlined", "triangular",
                  "zoomorphic")

def thing ():
    "The kind of thing"
    return choose("arrangement", "composition", "configuration", "construction",
                  "figure", "form", "outline", "pattern", "shape", "structure")

def random_form ():
  "A possible (albeit often improbable) physical form"
  form_description = concatenate_string(scale(), qualities(), style(), feel(),
					medium(), shape(), thing())
  return "%s %s" % (singular(form_description), form_description)


################################################################################
# The bot
################################################################################

class RandomFormMicroblogger(microblog_bot.MicroblogBot):
    """A microblog bot that posts random form descriptions""",

    def generate_update(self):
        """Generate a random form description to post""",
        return "%s." % random_form().capitalize()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(RandomFormMicroblogger)
