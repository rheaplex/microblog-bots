import random

def maybe (fun, probability=0.5, default=None):
    "Call fun with args if random(0..1) is less than probability."
    if random.random() < probability:
        result = fun()
    else:
        result = default
    return result

def choose (*choices):
    "Choose one of the choices"
    return random.choice(choices)

def choose_deep (choices):
    "Choose one item from a list of lists."
    return random.choice(random.choice(choices))

def maybe_choose (*choices):
    "Choose one, or return None, with a fifty-fifty chance"
    if random.random() < 0.5:
        result = choose(*choices)
    else:
        result = None
    return result

def plus_or_minus_one ():
    "Choose either one or minus one."
    return random.choice((1.0, -1.0))

def pluralise (string, plurality):
    "Make a word plural if necessary."
    if plurality == "A":
        result = string
    else:
        result = "%ss" % string
    return result

def concatenate_string(*strings):
    "Concatenate a list of strings, stripping empty or blank strings"
    strings = [string for string in strings if string and string.strip()]
    return ' '.join(strings)

def call_one_of(*funs):
    """Return the result of calling one of the functions"""
    return random.choice(funs)()

def singular (string):
    """Return the singular for the string"""
    string = string.strip()
    if string == "":
        singular = ""
    elif string[0] in "aeiou" :
        # "hi" ignored deliberately because it's silly
        singular = "an"
    else:
        singular ="a"
    return singular
