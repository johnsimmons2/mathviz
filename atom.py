# Atom made of electrons orbiting a nucleus. 
# Atoms can interact based on "proximity" (irl, euclidean distance, p-adic distance, etc)
# An atom can have kintetic and potential energy.
# An atom, based on its charge can attract or repell other atoms, or bond with them.
# I will need to implement beta decay, fission, fusion, and bonding.
# Molecules should be composed of any amount of atoms, one or more,
#   molecules should not be array/list based and instead have a "DNA" to describe them.
# Molecules can interact in chemical processes like in real life to form new molecule.


# I want to see if given high density, high energy, insane conditions (computer version of big bang),
#   can I produce the same atoms that develop into water, organic compounds, crystals, etc.
# Basically, are life and its components intrinsically interesting 
#   or is it just an emergent phenomena of necessary/likely entropic processes.


# Main Experiment:
# 1. Can we create a "chemical" simulation
#   a. Dimensionless: atoms do not need to literally 'touch' eachother.
#   b. What is inherent in evolution given enormous time
# 2. What aspects of evolution can be observed or analyzed here?
# 3. Can we form lipids and self-catalyzing similar properties?

class Atom:
    def __init__(self):
        self.charge = 0
        self.electrons = 0
        self.neutrons = 0
        self.protons = 0