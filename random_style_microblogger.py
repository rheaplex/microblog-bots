#!/usr/bin/env python

# random_style_microblogger.py - Post random style descriptions.
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

from utilities import call_one_of, choose, maybe, maybe_choose
import microblog_bot

################################################################################
# Style description
################################################################################

def attitude ():
    return maybe_choose("competent", "critical", "deconstructionist", 
                        "incompetent", "ironic", "nostalgic", "parodic",
                        "revivalist")

def movement ():
    return choose("abstract ", "abstract expressionist", "academic", 
                  "art brut", "art deco", "art nouveau", "arte povera",
                  "arts and crafts", 
                  "Bloomsbury Group", "baroque", "Bauhaus",
                  "celtic", "classical", "colour field", "computer art",
                  "conceptualist", "constuctivist", "contemporary art",
                  "cubist", 
                  "Dada", "De Stijl", "digital art",
                  "expressionist", 
                  "fauvist", "figurative", "folk art", "Fluxus",
                  "futurist", 
                  "generative art", "geometric abstract", "glitch art",
                  "gothic", "graffiti", "grunge",
                  "hard-edge painting", "hypermoderist", "hyperrealist",
                  "impressionist", "institutional critique",
                  "international style", "installation art",
                  "jugendstil", "junk art",
                  "kitsch",
                  "land art", "lettrist", "lowbrow",
                  "magical realist", "mannerist", "minimalist",
                  "modernist",
                  "naive art", "neoclassical", "neoconceptualist",
                  "neo-Dada", "neo-expressionist", "neo-geo",
                  "neoplasticist", "neo-primitivist", "net.art",
                  "net art", "neue sachlichkeit", "new media",
                  "op art", "orphic", "outsider art",
                  "performance art", "photorealist", "pixel art",
                  "plein air", "pointilist", "pop-art",
                  "post-impressionist", "post-minimalist",
                  "postmodern", "postmodernist",
                  "post-painterly abstraction", "Pre-Raphaelite",
                  "primitivist", "process art", "psychedelic",
                  "readymade", "realist", "renaissance", "rococo", 
                  "romanesque", "romantic",
                  "situationist", "social realist", "socialist realist",
                  "space art", "spraycan art", "street art",
                  "stuckist", "suprematist", "surrealist", "symbolist",
                  "vorticist",
                  "yBA")

def artists ():
    return "%s-style" % choose("Art & Language", "Albers", "Francis Bacon", "Barbara Kruger", "Boccioni", "Bosch", "Bridget Riley", "Broodthaers", "Caravaggio", "Cezanne", "Chapman Brothers", "Chris Ashley", "Cindy Sherman", "Claes Oldenburg", "Constable", "Courbet", "Dali", "Danica Phelps", "de Kooning", "Degas", "Diego Riviera", "Donatello", "Duchamp", "Fuseli", "Hirst", "Fiona Rae", "Giacometti", "Gilbert & George", "Goya", "Hockney", "Hogarth", "Holzer", "H.R. Geiger", "Jasper Johns", "John Singer Sargent", "Joy Garnett", "Joseph Kosuth", "Julian Opie", "Kahlo", "Kandinsky", "Klimt", "Koons", "Lawrence Weiner", "Leonardo Da Vinci", "Magritte", "Malevich", "Manet", "MANIK", "Matisse", "Michaelangelo", "Modigliani", "Monet", "Murakami", "O\'Keefe", "Pollock", "Picasso", "Rachel Whiteread", "Raphael", "Rembrandt", "Renoir", "Rodin", "Rosetti", "Rothko", "Roy Lichtenstein", "Rubins", "Rhea Myers", "Seurat", "Sherrie Levine"  "Sol LeWitt", "Titian", "Tom Moody", "Tracey Emin", "Turner", "Van Gogh", "Vermeer", "Warhol")

def style (): 
    return choose("action painting", "appropriation", "assemblage", 
"automatic drawing", "bricolage", "carving", "cast bronze", "cast steel", "casting", "collage", "cut-up technique", "decollage", "decoupage", "detournement", "etching", "refusal to signify", "frottage", "generative art", "graffitti", "installation", "land art", "lightshows", "lightboxes", "marble carving", "monoprint", "mosaic", "new media", "nomination", "origami", "painting", "performance", "photography", "photomontage", "polychrome steel", "readymades", "relief", "sculpture", "screenprint", "site-specific art", "slide projection", "stone carving", "video", "video projection", "wall drawing", "wall painting", "wallpaper", "welded steel", "wood carving", "woodcut")

def random_style ():
    "A possible (albeit often improbable) artistic style"
    return ("%s %s %s" % (attitude(),
                          call_one_of(movement, artists), 
                          style()))

################################################################################
# The bot
################################################################################

class RandomStyleMicroblogger(microblog_bot.MicroblogBot):
    """A microblog bot that posts random style descriptions"""

    def generate_update(self):
        """Generate a random style description to post"""
        return "%s." % random_style().capitalize()

################################################################################
# Main flow of execution
################################################################################

if __name__ == "__main__":
    microblog_bot.run_once(RandomStyleMicroblogger)
