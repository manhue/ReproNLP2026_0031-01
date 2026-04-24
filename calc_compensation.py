from math import ceil
def round_up(n, factor=100):
    return ceil(n * factor) / factor

# Please read about the procedure in the Google Doc
# - https://docs.google.com/document/d/1duHj4jDRrggOZ2bOV_ERyijlytrKjMvp7-HnzT7GoUg/edit?usp=sharing

# Values within Section A must be in the same currency as each other
# Values within Section B must be in the same currency as each other
# The currency of Section A need not match that of Section B

'''Begin Section A:  All values here must be in the same currency'''
min_wage_your_lab = 21.70 # CHF -> used the value from Basel as per https://www.ch.ch/de/arbeit/mindestlohne-und-medianlohn/#mindestlohne-in-der-schweiz
min_wage_your_participant = 21.70 # CHF -> used the value from Basel as per https://www.ch.ch/de/arbeit/mindestlohne-und-medianlohn/#mindestlohne-in-der-schweiz
uk_living_wage = 13.53  # CHF
'''End Section A'''

'''Begin Section B:  All values here must be in the same currency'''
original_study_wage = 1 # USD
original_study_min_wage = 1 # USD
'''End Section B'''

# Take the higher of your labs minimum wage, and the minimum wage where participants are
min_wage = max(min_wage_your_lab, min_wage_your_participant) # => 21.7

# Calculate the multiplier and wage based on
if not original_study_min_wage:
  # To avoid div by zero error, will set multiplier to 1.0
  # - for when original_study_min_wage is not known
  original_study_min_wage = original_study_wage
multiplier = (original_study_wage / original_study_min_wage) # => 1
wage = min_wage * multiplier # => 21.7

# Take the highest of these three wages
# - min_wage is in case multipler is less than 1.0
reproduction_wage = max(wage, min_wage, uk_living_wage) # => 21.7

reproduction_wage = round_up(reproduction_wage) # => 21.7 CHF =

print(f'The reproduction wage is {reproduction_wage}')




# source: https://docs.google.com/document/d/1oXXH52ew3MpOEDqMQ-oLRKf15ULZzUU8IZKBgMOilYs/edit?tab=t.0, 3.1 point 5
# everything in CHF, conversions done with https://www.oanda.com/currency-converter/en/?from=GBP&to=CHF
# min_wage_your_lab = 0 #:  the minimum wage in the country/region where your lab is based.
# min_wage_your_participant = 21.7 #  the minimum wage in the country/region where your participants are based, converted to the same currency as min_wage_your_lab.  For crowdsource work (such as Mechanical Turk) set this to 0.
# original_study_wage = 0 #:  what participants were paid in the original study.
# original_study_min_wage = 0 # the minimum wage where the original study was carried out, at the time when it was conducted.  (original_study_* variables should both be in the same currency as each other, but need not be converted to the same currency as used by your lab).
# uk_living_wage = 13.53 #:  set to the equivalent in your currency of £12.60 GBP, this is the ReproHum project global minimum.
# #Calculate the reproduction_wage by following the below steps:
# min_wage = max(min_wage_your_lab,min_wage_your_participant)
# if original_study_min_wage is None:
#     original_study_min_wage = original_study_wage
# multiplier = (original_study_wage / original_study_min_wage)
# wage = min_wage * multiplier
# reproduction_wage = max(wage, min_wage, uk_living_wage)
# print(reproduction_wage)
