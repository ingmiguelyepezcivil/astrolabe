# bright_stars_process.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2010-2022 Dominic Ford <dcf21-www@dcford.org.uk>
#
# This code is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# You should have received a copy of the GNU General Public License along with
# this file; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

# ----------------------------------------------------------------------------

"""
This script takes the Yale Bright Star Catalogue, and formats it into a python list. It also adds the names of objects.
"""

import re


def fetch_bright_star_list():
    """
    Read the Yale Bright Star Catalogue from disk, and return it as a list of stars.

    :return:
        Dictionary
    """
    # Astronomical unit, in metres
    AU = 1.49598e11

    # Light year, in metres
    LYR = 9.4605284e15

    # Build a dictionary of stars, indexed by HD number
    stars = {}

    # Convert three-letter abbreviations of Greek letters into UTF-8
    greek_alphabet = {'Alp': '\u03b1', 'Bet': '\u03b2', 'Gam': '\u03b3', 'Del': '\u03b4', 'Eps': '\u03b5',
                      'Zet': '\u03b6', 'Eta': '\u03b7', 'The': '\u03b8', 'Iot': '\u03b9', 'Kap': '\u03ba',
                      'Lam': '\u03bb', 'Mu': '\u03bc', 'Nu': '\u03bd', 'Xi': '\u03be', 'Omi': '\u03bf',
                      'Pi': '\u03c0', 'Rho': '\u03c1', 'Sig': '\u03c3', 'Tau': '\u03c4', 'Ups': '\u03c5',
                      'Phi': '\u03c6', 'Chi': '\u03c7', 'Psi': '\u03c8', 'Ome': '\u03c9'}

    # Superscript numbers which we may place after Greek letters to form the Flamsteed designations of stars
    star_suffices = {'1': '\u00B9', '2': '\u00B2', '3': '\u00B3'}

    # Look up the common names of bright stars
    star_names = {}
    for line in open("raw_data/bright_star_names.dat"):
        if (len(line) < 5) or (line[0] == '#'):
            continue
        # Catalog is indexed by the HR number of each star in the first column
        bs_num = int(line[0:4])

        # The second column is the name of the star, with underscores in the place of spaces
        name = line[5:]
        star_names[bs_num] = re.sub(' ', '_', name.strip())

    # Loop through the Yale Bright Star Catalog, line by line
    bs_num = 0
    for line in open("raw_data/bright_star_catalog.dat"):
        # Ignore blank lines and comment lines
        if (len(line) < 100) or (line[0] == '#'):
            continue

        # Counter used too calculated the bright star number -- i.e. the HR number -- of each star
        bs_num += 1
        try:
            # Read the Henry Draper (i.e. HD) number for this star
            hd = int(line[25:31])

            # Read the right ascension of this star (J2000)
            ra_hrs = float(line[75:77])
            ra_min = float(line[77:79])
            ra_sec = float(line[79:82])

            # Read the declination of this star (J2000)
            dec_neg = (line[83] == '-')
            dec_deg = float(line[84:86])
            dec_min = float(line[86:88])
            dec_sec = float(line[88:90])

            # Read the V magnitude of this star
            mag = float(line[102:107])
        except ValueError:
            continue

        # Look up the Bayer number of this star, if one exists
        star_num = -1
        try:
            star_num = int(line[4:7])
        except ValueError:
            pass

        # Render a unicode string containing the name, Flamsteed designation, and Bayer designation for this star
        name_bayer = name_bayer_full = name_english = name_flamsteed_full = "-"

        # Look up the Greek letter (Flamsteed designation) of this star
        greek = line[7:10].strip()

        # Look up the abbreviation of the constellation this star is in
        const = line[11:14].strip()

        # Some stars have a suffix after the Flamsteed designation, e.g. alpha-1, alpha-2, etc.
        greek_letter_suffix = line[10]
        if greek in greek_alphabet:
            name_bayer = greek_alphabet[greek]
            if greek_letter_suffix in star_suffices:
                name_bayer += star_suffices[greek_letter_suffix]
            name_bayer_full = '{}-{}'.format(name_bayer, const)
        if star_num > 0:
            name_flamsteed_full = '{}-{}'.format(star_num, const)

        # See if this is a star with a name
        if bs_num in star_names:
            name_english = star_names[bs_num]

        # Turn RA and Dec from sexagesimal units into decimal
        ra = (ra_hrs + ra_min / 60 + ra_sec / 3600) / 24 * 360
        dec = (dec_deg + dec_min / 60 + dec_sec / 3600)
        if dec_neg:
            dec = -dec

        # Build a dictionary is stars, indexed by HD number
        stars[hd] = [ra, dec, mag, name_bayer, name_bayer_full, name_english, name_flamsteed_full]

    hd_numbers = list(stars.keys())
    hd_numbers.sort()

    return {
        'stars': stars,
        'hd_numbers': hd_numbers
    }
