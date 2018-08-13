# -*- coding: utf-8 -*-
"""
Test document for the open street map project
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
# from uszipcode import ZipcodeSearchEngine

osm_file = "map.osm.xml"

## create instance:
#search = ZipcodeSearchEngine()
## search by zipcode
#zipcode = search.by_zipcode("85051")
#print('\nzipcode')
#print(zipcode)
## search by city:
#result = search.by_city_and_state(city="Phoenix", state="AZ")
#print('\nZipcode')
#print(result[0].Zipcode)

# "Compile a regular expression pattern into a regular expression object,
# which can be used for matching using match() and search() methods"
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set) #keeps track of all the unusual street types
postcode_types = defaultdict(set) #keeps track of all the unusual postcode types

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Lane", 
            "Northwest"]

# UPDATE THIS VARIABLE 
mapping = { "Ave": "Avenue",
            "Ave,": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "LN.": "Lane",
            "NW": "Northwest",
            "St": "Street",
            "St,": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            }

# define the street type
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    # if the 'name' has a street type (ie isn't a single word street name):
    if m:
        # if the match found is in the mapping keys:
        if m.group() in mapping.keys():
            # you want to replace 'm.group()' in name (as it is the street type)
            street_type = m.group()
            if street_type not in expected:
                street_types[street_type].add(street_name)
        
#aduit the postcodes
def audit_postcode_type(postcode_types, postcode):
    n = re.match(r'^\d{5}$', postcode)
    # if the 'postcode' exists
    if n:
        return postcode
    else:
        postcode_types[postcode].add(postcode)
        
    #postcode_types[postcode].add(postcode)
    #return postcode_types

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print ("%s: %d") % (k, v) 
        
#========== Audit the attributes.  See what's in the data =====================
# street type attribute
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

# postal code attribute
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osm_file):
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag in ["way", "node"]:
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v']) 
                if is_postcode(tag):
                    audit_postcode_type(postcode_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))
    pprint.pprint(dict(postcode_types))
    
    return street_types, postcode_types
    
#def auditpost():
#    for event, elem in ET.iterparse(osm_file, events=("start",)):
#        if elem.tag in ["way", "node"]:
#            for tag in elem.iter("tag"):
#                if is_postcode(tag):
#                    audit_postcode_type(postcode_types, tag.attrib['v'])    
#    pprint.pprint(dict(postcode_types))
    #print_sorted_dict(street_types) 

#==============================================================================

#============== Fix the unusual data pieces / CLEAN IT ========================
    
def update_street_name(name, mapping):
            
    name = name.replace('  ', ' ')
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        # you can only fix what is in the mapping dictionary
        if street_type in mapping.keys():
            # as street_type is a key in 'mapping' 
            # it must have a value mapping[street_type]
            # just substitute one for the other
            name = re.sub(street_type, mapping[street_type], name)
    # this function will return either the cleaned street_name or the original
    # i.e. street_name is only cleaned if:
    #  1. It has a street type, 2. its type is a key in the mapping dictionary  
    return name
        
    # if m.group() in mapping.keys():
        # add code here

def test():
    # the 'st_types' dictionary is created
    st_types = audit(osm_file)

    for street_types, ways in st_types.items():
        for name in ways:
            better_name = update_street_name(name, mapping)
            # print the street names in the 'way' nodes
            print (name, "=>", better_name)

# test()

# test cases to test postcode update
# test_zip = ['AZ 85004', '85032-5837','850822']
# clean postcode after performing the audit
def update_postcode(postcode):
   # new regular expression pattern
   search = re.match(r'^\D*(\d{5}).*', postcode)
   # select the group that is captured
   clean_postcode = search.group(1)
   
   return clean_postcode

#for item in test_zip:
#   cleaned = update_postcode(item)
#   print (cleaned)

if __name__ == '__main__':
    audit(osm_file)
       
