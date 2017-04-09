#!/usr/bin/python

"""
This file is part of pyadm300 (https://github.com/ThreeSixes/pyadm300).

pyadm300 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyadm300 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyadm300.  If not, see <http://www.gnu.org/licenses/>. 
"""


import adm300parse
from pprint import pprint

# Pull in the parser library.
adm300 = adm300parse.adm300parse()

# Test sentences.
sentences = [
    "01a232+1 143-1 209+1 R..L.I00U3aA4401 600-1 71]",
    "02a230+1 155-1 235+1 R..L.I00U3rA4402 100+2 6A]",
    "03a230+1 168-1 232+1 R..L.I00U3jA4403 49620 6A]",
    "04a230+1 181-1 238+1 R..L.I00U3uA4404 00000 71]",
    "05a229+1 193-1 218+1 R..L.I00U3aA4407 00000 6E]",
    "06a228+1 205-1 216+1 R..L.I00U3lA4408 00000 6C]",
    "07a227+1 217-1 202+1 R..L.I00U3XA4409 00000 51]",
    "08a225+1 229-1 242+1 R..L.I00U3s5440: 00000 09]",
    "09a225+1 241-1 221+1 R..L.I00U3gA4401 600-1 72]",
    "10a177+1 251-1 129+1 R..L.I00U2hA0002 100+2 7B]",
    "11a010-1 251-1 040-1 R..L.I00U01A1513 49620 3A]",
    "12a013-1 251-1 000-1 R..L.I00U00A2514 00000 32]",
    "13a009-1 251-1 000-1 R..L.I00U00A3537 00000 38]",
    "14a007-1 251-1 000-1 R..L.I00U00A3518 00000 3C]",
    "15a009-1 251-1 039-1 R..L.I00U01A4579 00000 38]",
    "16a010-1 251-1 039-1 R..L.I00U01A455: 00000 32]",
    "17a010-1 251-1 000-1 R..L.I00U00A4531 600-1 2F]",
    "18a010-1 251-1 039-1 ...L.I00U01A4512 100+2 54]",
    "19a012-1 251-1 039-1 ...L.I00U01A55F3 49620 31]",
    "20a014-1 251-1 000-1 ...L.I00U00A55D4 00000 3A]",
    "21a441-1 252-1 343+0 ...L.I00U19A2227 00000 42]",
    "22a120+1 259-1 159+0 R..L.I00U0VA0008 00000 58]",
    "23a116+0 260-1 223+0 R..L.I00U0pA0009 00000 7E]",
    "24a112+1 266-1 885+0 ...L.I00U28A000: 00000 49]",
    "25a928+0 271-1 102+1 R..L.I00U2NA2421 600-1 56]",
    "26a951+0 277-1 105+1 R..L.I00U2OA3442 100+2 5D]",
    "27a978+0 283-1 103+1 R..L.I00U2MA3423 49620 4E]",
    "28a972+0 288-1 985+0 R..L.I00U2MA4484 00000 44]",
    "29a974+0 294-1 115+1 R..L.I00U2ZA4467 00000 54]",
    "30a977+0 299-1 880+0 R..L.I00U2BA4448 00000 43]",
    "31a973+0 304-1 107+1 R..L.I00U2PA4429 00000 51]",
    "32a982+0 310-1 101+1 R..L.I00U2KA440: 00000 45]",
    "33a987+0 316-1 107+1 R..L.I00U2RA4401 600-1 49]",
    "34a994+0 322-1 935+0 ...L.I00U2DA4402 100+2 28]",
    "35a989+0 327-1 946+0 R..L.I00U2FA4403 49620 4A]",
    "36a980+0 332-1 927+0 R..L.I00U2FA4404 00000 4D]",
    "37a981+0 338-1 108+1 R..L.I00U2VA4407 00000 50]",
    "38a984+0 343-1 105+1 R..L.I00U2QA4408 00000 53]",
    "39a987+0 349-1 918+0 R..L.I00U2DA4409 00000 4A]",
    "40a981+0 354-1 990+0 R..L.I00U2HA440: 00000 41]",
    "41a984+0 360-1 957+0 R..L.I00U2EA4401 600-1 55]",
    "42a986+0 365-1 879+0 R..L.I00U27A4402 100+2 2F]",
    "43a982+0 370-1 103+1 R..L.I00U2QA4403 49620 5D]",
    "44a974+0 375-1 874+0 R..L.I00U2AA4404 00000 40]",
    "45a980+0 382-1 123+1 R..L.I00U2gA4407 00000 6D]"
]

# Process each sentence.
for sentence in sentences:
    pprint(adm300.parseSentence(sentence))