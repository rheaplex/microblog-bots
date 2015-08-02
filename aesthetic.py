# aesthetic.py - Generate and evaluate aesthetic descriptions.
# Copyright (C) 2011 Rhea Myers rhea@myers.studio
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

from utilities import choose, choose_deep, concatenate_string, \
    call_one_of, maybe, pluralise, plus_or_minus_one

##############################################################################
## Quantity
##############################################################################

def amount ():
    "Generate a quantity description."
    return choose("A", "A pair of", "Some", "Many")

##############################################################################
## Colour
##############################################################################

MONOCHROMES = ("black", "grey", "white")
HUES = ("red", "orange", "yellow", "green", "blue", "purple")
COLOURS = ("magenta", "cyan", "brown", "pink", "turquoise", "mauve")
METALS = ("gold", "silver", "bronze", "platinum", "copper", "rust-coloured")
FABRICS = ("khaki", "cotton-coloured", "denim blue", "suede-coloured")
NATURALS = ("sky blue", "leaf green", "sea green", "sunset red")
ARTIFICIALS = ("neon blue", "sunset yellow", "shocking pink", "non-repro blue",
               "blue-screen blue", "green-screen green")
PALETTES = (MONOCHROMES, HUES, COLOURS, METALS, FABRICS, NATURALS, ARTIFICIALS)
TONE = ("pale", "", "rich", "bright", "", "dark")

def colour ():
    "Choose a flat colour from a palette"
    return choose_deep(PALETTES)

def colour_description ():
    "Generate a colour description."
    return concatenate_string(random.choice(TONE), colour())

##############################################################################
## Texture
##############################################################################

def texture ():
    "Choose a texture."
    return choose("halftoned", "crosshatched", "scumbled", "glazed",
                  "sketchy", "smooth")

##############################################################################
## Appearance
##############################################################################

def appearance ():
    "Generate the appearance of a figure."
    return concatenate_string(maybe(texture), colour_description())

##############################################################################
## Shape
##############################################################################

GEOMETRIC = ("circle", "triangle", "square", "pentagon", "hexagon", "octagon")
FORM = ("organic shape", "spiky shape", "irregular shape")
ABSTRACT_SHAPES = (GEOMETRIC, FORM)
ABSTRACT_SHAPE_TREATMENT = ("", "", "outlined")
BUILDING = ("house", "skyscraper")
TRANSPORT = ("car", "aeroplane", "ship")
ANIMAL = ("bird", "cat", "dog", "horse")
GENERIC_SHAPES = (BUILDING, TRANSPORT, ANIMAL)
GENERIC_SHAPE_TREATMENT = ("", "", "", "silhouetted", "outlined", "abstracted")

def shape_size ():
    "Generate a size for the shape."
    choose("", "", "tiny", "small", "large", "massive")

def shape_form (plural):
    "Generate a shape form description."
    if random.random() > 0.5:
        form = concatenate_string(random.choice(ABSTRACT_SHAPE_TREATMENT),
                                  pluralise(choose_deep(ABSTRACT_SHAPES),
                                            plural))
    else:
        form = concatenate_string(random.choice(GENERIC_SHAPE_TREATMENT),
                                  pluralise(choose_deep(GENERIC_SHAPES),
                                            plural))
    return form

def shape ():
    if random.random() > 0.5:
        shape = choose_deep(ABSTRACT_SHAPES)
    else:
        shape = choose_deep(GENERIC_SHAPES)
    return shape

def shape_description (plural):
    "Generate a shape description."
    return concatenate_string(shape_size(), appearance(), shape_form(plural))

##############################################################################
## Ground
##############################################################################

def ground ():
    "Generate a simple ground description."
    return appearance()

##############################################################################
## Descriptions
##############################################################################

def generate_description ():
    "Describe a single (set of) figure(s) on a single ground."
    plural = amount()
    return concatenate_string(plural, shape_description(plural), "on a",
                              ground(), "ground.")

##############################################################################
## Aesthetics
##############################################################################

MIN_PROPERTIES = 4
MAX_PROPERTIES = 12
MAX_PROPERTIES_TO_DELETE = 2
MAX_PROPERTIES_TO_MUTATE = 2
MAX_PROPERTIES_TO_ADD =2

def aesthetic_opinions (aesthetic):
    "Sort the properties into likes and dislikes."
    likes = []
    dislikes = []
    for key in aesthetic.keys():
        if aesthetic[key] >= 0.0:
            likes.append(key)
        else:
            dislikes.append(key)
    return likes, dislikes

def describe_aesthetic (aesthetic):
    "Describe the current likes and dislikes."
    likes, dislikes = aesthetic_opinions(aesthetic)
    if likes:
        likes_string = 'I like %s' % ', '.join(likes)
    else:
        likes_string = ''
    if dislikes:
        dislikes_string = 'I dislike %s' % ', '.join(dislikes)
    else:
        dislikes_string = ''
    return likes_string, dislikes_string

def make_property ():
    "Choose a new property."
    return call_one_of(shape, colour, texture)

def make_properties (count):
    "Choose n properties."
    return [make_property() for i in xrange(0, count)]

def add_properties (properties):
    "Add zero or more properties."
    new_props = make_properties(min(max(MIN_PROPERTIES,
                                        random.randint(MAX_PROPERTIES_TO_ADD))
                                    (- MAX_PROPERTIES, len(properties))))
    return properties + new_props

def delete_properties (properties):
    "Delete 0+ properties, don't reduce properties below +min_properties+."
    end = max(len(properties) - random.randint(MAX_PROPERTIES_TO_MUTATE),
              MIN_PROPERTIES)
    return properties[0:end]

def update_properties (properties):
    "Add some properties, delete some properties"
    return add_properties(delete_properties(properties))

def describe_properties (properties):
    "List the properties in a comma-delimited string"
    return ', '.join(properties)

def evaluate_properties (properties1, properties2):
    "Find how many properties match"
    return len(intersection(set(properties1), set(properties2)))

def set_aesthetic_property (aesthetic, prop):
    "Set (intialize) valenced property."
    aesthetic[prop] = plus_or_minus_one()

def set_aesthetic_properties (aesthetic, props):
    "Set (initialize) valenced properties."
    for prop in props:
        set_aesthetic_property(aesthetic, prop)

def make_aesthetic ():
    "Generate an initial set of properties."
    properties = make_properties(random.randint(MIN_PROPERTIES, MAX_PROPERTIES))
    aesthetic = {}
    set_aesthetic_properties(aesthetic, properties)
    return aesthetic

def delete_aesthetic_properties (aesthetic):
    "Delete 0+ properties, don't reduce properties below MIN_PROPERTIES."
    delete_count = random.randint(0, MAX_PROPERTIES_TO_DELETE)
    delete_props = random.sample(aesthetic.keys(), delete_count)
    for prop in delete_props:
        del aesthetic[prop]

def add_aesthetic_properties (aesthetic):
  "Add zero or more properties."
  add_count = min(max(MIN_PROPERTIES,
                      random.randint(0, MAX_PROPERTIES_TO_ADD)),
                  (MAX_PROPERTIES - len(aesthetic)))
  for i in xrange(0, add_count):
      prop = make_property()
      if not prop in aesthetic:
          set_aesthetic_property(aesthetic, prop)

def mutate_aesthetic_properties (aesthetic):
    "Mutate zero or more properties."
    mutate_count = random.randint(1, MAX_PROPERTIES_TO_MUTATE)
    for prop in random.sample(aesthetic.keys(), mutate_count):
        aesthetic[prop] = -(aesthetic[prop])

def update_aesthetic (aesthetic):
    "Update the aesthetic."
    delete_aesthetic_properties(aesthetic)
    mutate_aesthetic_properties(aesthetic)
    add_aesthetic_properties(aesthetic)

##############################################################################
## Critique
##############################################################################

## How to handle ambiguities? yellow vs sunset yellow?
## Sort keys by length
## Find longest first
## Remove from string
## But what if that creates bogus sequences? Break into substrings?
## Just always hypenate multi-word sequences?

def positive_aesthetic_value (description, aesthetic):
    "Sum the positive value of the work under the aesthetic"
    clean_artwork = description.lower()
    pos_total = 0.0
    for key, value in aesthetic.items():
        if clean_artwork.find(key) != -1:
            if value > 0.0:
                pos_total += value
    return pos_total

def negative_aesthetic_value (description, aesthetic):
    "Sum the negative value of the work under the aesthetic"
    clean_artwork = description.lower()
    neg_total = 0.0
    for key, value in aesthetic.items():
        if clean_artwork.find(key) != -1:
            if value < 0.0:
                # Yes, subtract. It's a positive value
                neg_total -= value
    return neg_total

def total_aesthetic_values (description, aesthetic):
    "Sum the values of the work under the aesthetic"
    clean_artwork = description.lower()
    pos_total = 0.0
    neg_total = 0.0
    for key, val in aesthetic.items():
        if clean_artwork.find(key) != -1:
            if val > 0.0:
                pos_total += val
            if val < 0.0:
                # Yes, subtract. Both values are positive
                neg_total -= val
    return pos_total, neg_total

def describe_aesthetic_value (positive, negative):
    "Describe the value of the work allowing for pos & neg points."
    if (positive >= 2) and (negative == 0):
        result = "a masterpiece"
    elif (negative >= 2) and (positive == 0):
        result = "a failure"
    elif positive > negative:
        result = "good"
    elif negative > positive:
        result = "bad"
    elif (negative == positive) and (negative >= 2):
        result = "extremely mixed"
    elif negative == positive == 1:
        result = "mixed"
    else:
        result = "uninteresting"
    return result

def critique_artwork (description, aesthetic, identifier):
    "Verbally critique the artwork."
    positive, negative = total_aesthetic_values(description, aesthetic)
    throat_clearing = choose("I think that", "In my opinion,",
                             "I would say that", "Aesthetically speaking,")
    return "%s %s is %s." % (throat_clearing,
                             identifier,
                             describe_aesthetic_value(positive, negative))

##############################################################################
## Similarity, strength of resemblance
##############################################################################

def euclidean_aesthetic_similarity (aesthetic_list, aesthetic_hash):
    "Get the normalized euclidean distance between two aesthetics"
    total = 0.0
    for key in aesthetic_list:
        aesthetic_weight = aesthetic_hash.get(key, 0.0)
        total += math.pow(aesthetic_weight, 2)
    return 1.0 / (1.0 + math.sqrt(total))
