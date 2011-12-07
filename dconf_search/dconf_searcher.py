import tinydconf as dconf
import argparse
import sys
import re

"""
    Provides search funcionality for dconf
"""

class Match(object):
    """Represents a match found while searching on dconf"""
    KEY, VALUE = range(2)
    
    def __init__(self, search, type, path=None, value=None):
        self.match = search
        self.type = type
        self.value = value
        self.path = path

def dconf_search(path, search_value, look_keys=False, look_values=False,
                 icase=True):
    """Searches dconf returning a list of Match """
    results = []
    search_value = str(search_value)
    flags = icase and re.IGNORECASE
    if path[-1] == '/': 
        found = re.search('(.*)(' + search_value + ')(.*)', path, flags)
        if found:
            results.append(Match(found, Match.KEY))
        for i in dconf.list(path):
            results += dconf_search(path + i, search_value, look_keys,
                                  look_values, icase)
    else:
        if look_keys:
            found = re.search('(.*)(' + search_value + ')(.*)', path, flags)
            if found:
                results.append(Match(found, Match.KEY))
        if look_values:
            value = dconf.read(path)
            found = re.search('(.*)(' + search_value + ')(.*)',
                                unicode(value), flags)
            if found:
                results.append(Match(found, Match.VALUE, path, value))
    return results

def format(prefix, core, sufix, crop, color):
    """Format output cropping if crop is set"""
    if color:
        txtgrn = '\x1b[32m'
        txtrst = '\x1b[0m'
    else:
        txtgrn = ''
        txtrst = ''
    if len(prefix + core + sufix) <= 50 or not crop:
        return prefix + txtgrn + core + txtrst + sufix
    left = 50
    left -= len(core)
    each = left / 4
    if len(prefix) >= each * 2:
        prefix = prefix[:each] + ' ... ' + prefix[-each:]
    if len(sufix) >= each * 2:
        sufix = sufix[:each] + ' ... ' + sufix[-each:]
    return prefix + txtgrn + core + txtrst + sufix

def beautify(results, crop_key=True, color=True):
    """Makes the results look good : D"""
    if color:
        txtgrn = '\x1b[32m'
        txtred = '\x1b[31m'
        txtrst = '\x1b[0m'
    else:
        txtgrn = ''
        txtred = ''
        txtrst = ''
    pretty_results = []
    for i in results:
        if i.type == Match.VALUE:
            pretty_results.append(i.path + txtred + ':' + txtrst +
                                  format(i.match.group(1), i.match.group(2),
                                         i.match.group(3), crop_key, color))
        else:
            pretty_results.append(i.match.group(1) + txtgrn + i.match.group(2) +
                                  txtrst + i.match.group(3))
    return pretty_results

def search():
    parser = argparse.ArgumentParser(description='''
                                        Script made to search entries on dconf
                                        since the dconf only provide read/list.
                                     ''')
    parser.add_argument('search', metavar='SEARCH', type=str,
                        help='Pattern to search for')
    parser.add_argument('-p', '--path', dest='path', type=str, 
                        help="Dconf path to begin search. Default is '/'",
                        default='/')
    parser.add_argument('-k', '--keys', dest='keys', action='store_true',
                        help='Search for keys also')
    parser.add_argument('--values', dest='values', action='store_true',
                        help='Search for value of keys also')
    parser.add_argument('-i', '--icase', dest='icase', action='store_true',
                        help='Makes the search case insensitive')
    parser.add_argument('-c', '--crop', dest='crop', action='store_true',
                        help='Crop results if it\'s too long')
    parser.add_argument('-n', '--no-color', dest='color', action='store_false',
                        help='No colourful output')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    results = dconf_search(args.path, args.search, args.keys, args.values,
                            args.icase)
    for i in beautify(results, args.crop, args.color):
        sys.stderr.write(i+'\n')
        print i.encode('utf-8')
