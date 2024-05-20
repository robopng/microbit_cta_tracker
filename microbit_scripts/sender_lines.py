"""
Definitions of all the stops on each of the CTA 'L' lines.
Each name listed in this file shadows the name given in official CTA data.
For use only in conjunction with sender_main.py; see that file for more.
"""

# assuming tower 18 entry point
LOOP = [
    "CLARK/LAKE",
    "STATE/LAKE",
    "WASHINGTON/WABASH",
    "ADAMS/WABASH",
    "HAROLD WASHINGTON LIBRARY-STATE/VAN BUREN",
    "LASALLE/VAN BUREN",
    "QUINCY/WELLS",
    "WASHINGTON/WELLS"
]
BROWN = [
    "KIMBALL",
    "KEDZIE",
    "FRANCISCO",
    "ROCKWELL",
    "WESTERN",
    "DAMEN",
    "MONTROSE",
    "IRVING PARK",
    "ADDISON",
    "PAULINA",
    "SOUTHPORT",
    "BELMONT",
    "WELLINGTON",
    "DIVERSEY",
    "FULLERTON",
    "ARMITAGE",
    "SEDGWICK",
    "CHICAGO",
    "MERCHANDISE MART",
] + LOOP[::-1]  # brown line traverses opposite
PURPLE = [
    "LINDEN",
    "CENTRAL",
    "NOYES",
    "DAVIS",
    "DEMPSTER",
    "MAIN",
    "SOUTH BOULEVARD",
    "HOWARD",
    "WILSON",
] + BROWN[BROWN.index("BELMONT"):BROWN.index("MERCHANDISE MART")] + LOOP  # shared tracks
RED = [
    "HOWARD",
    "JARVIS",
    "MORSE",
    "LOYOLA",
    "GRANVILLE",
    "THORNDALE",
    "BRYN MAWR",
    # "BERWYN",
    "ARGYLE",
    # "LAWRENCE",
    "WILSON",
    "SHERIDAN",
    "ADDISON",
    "BELMONT",
    "FULLERTON",
    "NORTH/CLYBOURN",
    "CLARK/DIVISION",
    "CHICAGO",
    "GRAND",
    "LAKE",
    "MONROE",
    "JACKSON",
    "HARRISON",
    "ROOSEVELT",
    "CERMAK-CHINATOWN",
    "SOX-35TH",
    "47TH",
    "GARFIELD",
    "69TH",
    "79TH",
    "87TH",
    "95TH"
]
BLUE = [
    "O'HARE",
    "ROSEMONT",
    "CUMBERLAND",
    "HARLEM",
    "JEFFERSON PARK",
    "MONTROSE",
    "IRVING PARK",
    "ADDISON",
    "BELMONT",
    "LOGAN SQUARE",
    "CALIFORNIA",
    "WESTERN",
    "DAMEN",
    "DIVISION",
    "CHICAGO",
    "GRAND",
    "WASHINGTON",
    "MONROE",
    "JACKSON",
    "LASALLE",
    "CLINTON",
    "UIC-HALSTED",
    "RACINE",
    "ILLINOIS MEDICAL DISTRICT",
    "WESTERN",
    "KEDZIE-HOMAN",
    "PULASKI",
    "CICERO",
    "AUSTIN",
    "OAK PARK",
    "HARLEM",
    "FOREST PARK"
]
ORANGE = [
    "MIDWAY",
    "KEDZIE",
    "WESTERN",
    "35TH/ARCHER",
    "ASHLAND",
    "HALSTED",
    "ROOSEVELT"
] + LOOP[4:] + LOOP[0:4]  # tower 12 entry point
GREEN = [
    "HARLEM / LAKE",
    "OAK PARK",
    "RIDGELAND",
    "AUSTIN",
    "CENTRAL",
    "LARAMIE",
    "CICERO",
    "PULASKI",
    "CONSERVATORY",
    "KEDZIE",
    "CALIFORNIA",
    "ASHLAND",
    "MORGAN",
    "CLINTON",
] + LOOP[:4] + [  # green line only swings through
    "ROOSEVELT",
    "CERMAK",
    "35TH-BRONZEVILLE-IIT",
    "INDIANA"
    "43RD",
    "45TH",
    "51ST",
    "GARFIELD",
    "HALSTED",
    "ASHLAND/63RD",
    # cottage grove branch
    "KING DRIVE",
    "COTTAGE GROVE"
]
PINK = [
    "54TH/CERMAK",
    "CICERO",
    "KOSTNER",
    "PULASKI",
    "CENTRAL PARK",
    "KEDZIE",
    "CALIFORNIA",
    "WESTERN",
    "DAMEN",
    "18TH",
    "POLK",
    "ASHLAND",
    "MORGAN",
    "CLINTON"
] + LOOP
YELLOW = [
    "DEMPSTER-SKOKIE",
    "OAKTON-SKOKIE",
    "HOWARD"
]
LINES = {
    "BROWN": BROWN,
    "PURPLE": PURPLE,
    "RED": RED,
    "BLUE": BLUE,
    "ORANGE": ORANGE,
    "GREEN": GREEN,
    "PINK": PINK,
    "YELLOW": YELLOW,
}
