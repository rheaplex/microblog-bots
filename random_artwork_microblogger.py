#!/usr/bin/env python

# random_artwork_microblogger.py - Post random artwork descriptions.
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
# Artwork description
################################################################################

def attitude ():
  return maybe_choose("incompetent", "ironic", "parodic", "revivalist")

def movement ():
    return choose("abstract ", "abstract expressionist", "academic", "art brut",
                  "art deco", "art nouveau", "arte povera", "arts and crafts",
                  "Bloomsbury Group", "baroque", "Bauhaus",
                  "celtic", "classical", "colour field", "computer art",
                  "conceptualist", "constuctivist", "contemporary art",
                  "cubist",
                  "Dada", "De Stijl", "digital art",
                  "expressionist", "fauvist", "figurative", "folk art", 
                  "Fluxus", "futurist",
                  "generative art", "geometric abstract", "glitch art",
                  "gothic", "graffiti", "grunge",
                  "hard-edge painting", "hypermoderist", "hyperrealist",
                  "impressionist", "institutional critique",
                  "international style", "installation art",
                  "jugendstil", "junk art",
                  "kitsch",
                  "land art", "lettrist", "lowbrow",
                  "magical realist", "mannerist", "minimalist", "modernist",
                  "naive art", "neoclassical", "neoconceptualist", "neo-Dada",
                  "neo-expressionist", "neo-geo", "neoplasticist",
                  "neo-primitivist", "net.art", "net art", "neue sachlichkeit",
                  "new media",
                  "op art", "orphic", "outsider art",
                  "performance art", "photorealist", "pixel art", "plein air",
                  "pointilist", "pop-art", "post-impressionist",
                  "post-minimalist", "postmodern", "postmodernist",
                  "post-painterly abstraction", "Pre-Raphaelite",
                  "primitivist", "process art", "psychedelic",
                  "readymade", "realist", "renaissance", "rococo", "romanesque",
                  "romantic",
                  "situationist", "social realist", "socialist realist",
                  "space art",
                  "spraycan art", "street art", "stuckist", "suprematist",
                  "surrealist", "symbolist",
                  "vorticist", "yBA")

def artists ():
    return "%s-style" % choose("Art & Language", "Albers", "Francis Bacon", "Barbara Kruger", "Boccioni", "Bosch", "Bridget Riley", "Broodthaers", "Caravaggio", "Cezanne", "Chapman Brothers", "Chris Ashley", "Cindy Sherman", "Claes Oldenburg", "Constable", "Courbet", "Dali", "Danica Phelps", "de Kooning", "Degas", "Diego Riviera", "Donatello", "Duchamp", "Fuseli", "Hirst", "Fiona Rae", "Giacometti", "Gilbert & George", "Goya", "Hockney", "Hogarth", "Holzer", "H.R. Geiger", "Jasper Johns", "John Singer Sargent", "Joy Garnett", "Joseph Kosuth", "Julian Opie", "Kahlo", "Kandinsky", "Klimt", "Koons", "Lawrence Weiner", "Leonardo Da Vinci", "Magritte", "Malevich", "Manet", "MANIK", "Matisse", "Michaelangelo", "Modigliani", "Monet", "Murakami", "O'Keefe", "Pollock", "Picasso", "Rachel Whiteread", "Raphael", "Rembrandt", "Renoir", "Rodin", "Rosetti", "Rothko", "Roy Lichtenstein", "Rubins", "Rhea Myers", "Seurat", "Sherrie Levine"  "Sol LeWitt", "Titian", "Tom Moody", "Tracey Emin", "Turner", "Van Gogh", "Vermeer", "Warhol")

def style ():
    return choose("action painting", "appropriation", "assemblage", "automatic drawing", "bricolage", "carving", "cast bronze sculpture", "cast steel sculpture", "cast", "collage", "cut-up technique", "decollage", "decoupage", "detournement", "etching", "refusal to signify", "frottage", "generative artwork", "graffitti", "installation", "lightshow", "lightbox", "marble carving", "monoprint", "mosaic", "new media artwork", "painting", "performance", "photograph", "photomontage", "polychrome steel sculpture", "readymade", "relief", "sculpture", "screenprint", "site-specific artwork", "slide projection", "stone carving", "video", "video projection", "wall drawing", "wall painting", "welded steel sculpture", "wood carving", "woodcut")

def genre ():
    return choose("abstract", "allegorical", "anti-clerical", "caricature", "cityscape", "equestrian", "erotica", "genre", "historical", "interior", "landscape", "marine", "memento mori", "military", "nude", "pastoral", "portrait", "propaganda", "protest", "still life", "studio")

def ideology ():
    return maybe_choose("academic", "anarchist", "critical", "conservative", "environmantalist", "liberal", "libertarian", "marxist", "modernist", "nationalist", "neoliberal", "postmodernist", "progressive", "radical", "religious")

def expressing ():
  return "expressing %s" % \
      choose("anger", "alienation", "amusement", "anxiety",
             "bravery", "coldness",
             "compassion", "dejection", "depression", "desire",
             "disgust", "excitement", "expectation", "fear",
             "grief", "happiness", "hope",
             "joy", "love", "lust", "melancholy", "nostalgia",
             "pain", "pleasure", "pride", "sentimentality",
             "shock", "surprise", "sympathy", "tenderness",
             "warmth")

def critiquing ():
    return "critiquing %s" % choose("academia", "aesthetics", "art", "capital", "class", "culture", "gender", "identity", "ideology", "mass media", "nationality", "philosophy", "politics", "popular culture", "race", "relationships", "science", "society", "technology", "theology")

#depicting, alluding to, mourning, praising, reacting against, paying homage to

def mood ():
    return maybe_choose("calm", "dour", "energetic", "gloomy",
                        "angry", "alienating" # -ed or -ing?
                        "amusing", "anxious", "brave",
                        "calm", "carefree", "cold",
                        "compassionate", "dejected", "depressing", "desirous",
                        "disgusting", "dour", "exciting", "expectant", 
                        "fearful",
                        "happy", "hopeful",
                        "joyful", "loving", "lustful", "melancholy", 
                        "nostalgic",
                        "proud", "sentimental",
                        "shocking", "surprising", "sympathetic", "tender",
                        "warm")

def random_artwork ():
    "A possible (albeit often improbable) artwork",
    # This use of maybe-choose is wasteful
    description = concatenate_string(mood(), attitude(), ideology(),
                                     maybe_choose(movement(), artists()),
                                     genre(), style(),
                                     maybe_choose(expressing(), critiquing()))
    return "%s %s" % (singular(description), description)

################################################################################
# The bot
################################################################################

class RandomArtworkMicroblogger(microblog_bot.MicroblogBot):
    """A microblog bot that posts random artwork descriptions""",

    def generate_update(self):
        """Generate a random artwork description to post""",
        return "%s." % random_artwork().capitalize()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(RandomArtworkMicroblogger)
