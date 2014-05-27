# Extracts NSF award data from all XML files in the current directory and appends them to a single dataframe which is then pickled to disk

# Command line argument - 1 indicates the presence of a previously pickled dataframe on disk, 0 indicates its absence (for the first run)

# Data sourced from - http://www.nsf.gov/awardsearch/download.jsp
# Written by Utkarsh Jaiswal on May 18 2014

from bs4 import BeautifulSoup
from numpy import hstack, matrix
import pandas as pd
import os
from sys import argv, setrecursionlimit, getrecursionlimit
 
def xml2df(files, fLen, picklePath):
    master_list = [[]]
    df = pd.DataFrame(columns=('html', 'body', 'roottag', 'award', 'awardtitle', 'awardeffectivedate', 'awardexpirationdate', 'awardamount',
    'awardinstrument', 'awardinstrument-value', 'organization', 'organization-code', 'organization-directorate', 'organization-directorate-longname', 'organization-division',
    'organization-division-longname', 'programofficer', 'programofficer-signblockname', 'abstractnarration', 'minamdletterdate', 'maxamdletterdate', 'arraamount', 'awardid',
    'investigator-1', 'investigator-firstname-1', 'investigator-lastname-1', 'investigator-emailaddress-1', 'investigator-startdate-1', 'investigator-enddate-1', 'investigator-rolecode-1',
    'investigator-2', 'investigator-firstname-2', 'investigator-lastname-2', 'investigator-emailaddress-2', 'investigator-startdate-2', 'investigator-enddate-2', 'investigator-rolecode-2',
    'investigator-3', 'investigator-firstname-3', 'investigator-lastname-3', 'investigator-emailaddress-3', 'investigator-startdate-3', 'investigator-enddate-3', 'investigator-rolecode-3',
    'investigator-4', 'investigator-firstname-4', 'investigator-lastname-4', 'investigator-emailaddress-4', 'investigator-startdate-4', 'investigator-enddate-4', 'investigator-rolecode-4',
    'investigator-5', 'investigator-firstname-5', 'investigator-lastname-5', 'investigator-emailaddress-5', 'investigator-startdate-5', 'investigator-enddate-5', 'investigator-rolecode-5',
    'institution-1', 'institution-name-1', 'institution-cityname-1', 'institution-zipcode-1', 'institution-phonenumber-1', 'institution-streetaddress-1', 'institution-countryname-1', 'institution-statename-1', 'institution-statecode-1',
    'institution-2', 'institution-name-2', 'institution-cityname-2', 'institution-zipcode-2', 'institution-phonenumber-2', 'institution-streetaddress-2', 'institution-countryname-2', 'institution-statename-2', 'institution-statecode-2',
    'institution-3', 'institution-name-3', 'institution-cityname-3', 'institution-zipcode-3', 'institution-phonenumber-3', 'institution-streetaddress-3', 'institution-countryname-3', 'institution-statename-3', 'institution-statecode-3',
    'institution-4', 'institution-name-4', 'institution-cityname-4', 'institution-zipcode-4', 'institution-phonenumber-4', 'institution-streetaddress-4', 'institution-countryname-4', 'institution-statename-4', 'institution-statecode-4',
    'institution-5', 'institution-name-5', 'institution-cityname-5', 'institution-zipcode-5', 'institution-phonenumber-5', 'institution-streetaddress-5', 'institution-countryname-5', 'institution-statename-5', 'institution-statecode-5',
    'foainformation-1', 'foainformation-code-1', 'foainformation-name-1',
    'foainformation-2', 'foainformation-code-2', 'foainformation-name-2',
    'foainformation-3', 'foainformation-code-3', 'foainformation-name-3',
    'foainformation-4', 'foainformation-code-4', 'foainformation-name-4',
    'foainformation-5', 'foainformation-code-5', 'foainformation-name-5',
    'programelement-1', 'programelement-code-1', 'programelement-text-1',
    'programelement-2', 'programelement-code-2', 'programelement-text-2',
    'programelement-3', 'programelement-code-3', 'programelement-text-3',
    'programelement-4', 'programelement-code-4', 'programelement-text-4',
    'programelement-5', 'programelement-code-5', 'programelement-text-5',
    'programelement-6', 'programelement-code-6', 'programelement-text-6',
    'programelement-7', 'programelement-code-7', 'programelement-text-7',
    'programelement-8', 'programelement-code-8', 'programelement-text-8',
    'programelement-9', 'programelement-code-9', 'programelement-text-9',
    'programreference-1', 'programreference-code-1', 'programreference-text-1',
    'programreference-2', 'programreference-code-2', 'programreference-text-2',
    'programreference-3', 'programreference-code-3', 'programreference-text-3',
    'programreference-4', 'programreference-code-4', 'programreference-text-4',
    'programreference-5', 'programreference-code-5', 'programreference-text-5',
    'programreference-6', 'programreference-code-6', 'programreference-text-6',
    'programreference-7', 'programreference-code-7', 'programreference-text-7',
    'programreference-8', 'programreference-code-8', 'programreference-text-8',
    'programreference-9', 'programreference-code-9', 'programreference-text-9'))
    
    errorLog = open('errorLog.txt', 'a')

    fileIdx = 1
    for f in files:
        #print "Processing", f, "- file", fileIdx, "of", fLen
        fileIdx += 1
        inFile = open(f, 'r')
        soup = BeautifulSoup(inFile)
     
        name_list=[]
        text_list=[]
        attr_list=[]
     
        def recurs(soup):
            try:
                for j in soup.contents:
                    try:
                        #print j.name
                        if j.name!=None:
                            name_list.append(j.name)
                    except:
                        pass
                    try:
                        #print j.text
                        if j.name!=None:
                            #print j.string
                            text_list.append(j.string)
                    except:
                        pass
                    try:
                        #print j.attrs
                        if j.name!=None:
                            attr_list.append(j.attrs)
                    except:
                        pass
                    recurs(j)
            except:
                pass
     
        recurs(soup)
        inFile.close()
        #print name_list
        #print text_list
        #print attr_list # always null according to schema - http://www.nsf.gov/awardsearch/resources/Award.xsd

        # For the following section, refer http://www.nsf.gov/awardsearch/resources/Award.xsd
        # Per the schema, investigator, institution, foainformation, programelement and programreference can occur an unbounded number of times (maxOccurs = "unbounded")
        # Pad out each of these elements to the maximum number of instances allowed in our dataframe definition

        indices = [i for i, x in enumerate(name_list) if x == "investigator"]
        #print "investigator", indices
        if 5 - len(indices) > 0 and len(indices) != 0: # padding required if number of investigators is less than the max allowed
            firstIdx = indices[-1]
            colCount = offset = 7 # each occurrence of investigator accounts for 7 columns (see dataframe above)
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 7
        elif 5 - len(indices) > 0: # what if there are zero instances of investigator?
            firstIdx = name_list.index('awardid')
            colCount = 7
            offset = 1
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 7
        
        indices = [i for i, x in enumerate(name_list) if x == "institution"]
        #print "institution", indices
        if 5 - len(indices) > 0 and len(indices) != 0: # padding required if number of institutions is less than the max allowed
            firstIdx = indices[-1]
            colCount = offset = 9 # each occurrence of institution accounts for 9 columns (see dataframe above)
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 9
        elif 5 - len(indices) > 0: # what if there are zero instances of institution?
            firstIdx = name_list.index('awardid')
            colCount = 9
            offset = 36 # first insertion will occur at index(awardid) +35 (5x7 from padded 'investigator') +1
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 9

        indices = [i for i, x in enumerate(name_list) if x == "foainformation"]
        #print "foainformation", indices
        if 5 - len(indices) > 0 and len(indices) != 0: # padding required if number of foainformations is less than the max allowed
            firstIdx = indices[-1]
            colCount = offset = 3 # each occurrence of foainformation accounts for 3 columns (see dataframe above)
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3
        elif 5 - len(indices) > 0: # what if there are zero instances of foainformation?
            firstIdx = name_list.index('awardid')
            colCount = 3
            offset = 81 # first insertion will occur at index(awardid) +35 (5x7 from padded 'investigator') +45 (5x9 from padded 'institution') +1
            for i in range(5 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3

        indices = [i for i, x in enumerate(name_list) if x == "programelement"]
        #print "programelement", indices
        if 9 - len(indices) > 0 and len(indices) != 0: # padding required if number of programelements is less than the max allowed
            firstIdx = indices[-1]
            colCount = offset = 3 # each occurrence of programelement accounts for 3 columns (see dataframe above)
            for i in range(9 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3
        elif 9 - len(indices) > 0: # what if there are zero instances of programelement?
            firstIdx = name_list.index('awardid')
            colCount = 3
            offset = 96 # first insertion will occur at index(awardid) +35 (5x7 from padded 'investigator') +45 (5x9 'institution') +15 (5x3 'foainformation') +1
            for i in range(9 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3

        indices = [i for i, x in enumerate(name_list) if x == "programreference"]
        #print "programreference", indices
        if 9 - len(indices) > 0 and len(indices) != 0: # padding required if number of programreferences is less than the max allowed
            firstIdx = indices[-1]
            colCount = offset = 3 # each occurrence of programreference accounts for 3 columns (see dataframe above)
            for i in range(9 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3
        elif 9 - len(indices) > 0: # what if there are zero instances of programreference?
            firstIdx = name_list.index('awardid')
            colCount = 3
            offset = 123 # first insertion will occur at index(awardid) +35 (5x7 from padded 'investigator') +45 (5x9 'institution') +15 (5x3 'foainformation') +27 (9x3 'programelement') +1
            for i in range(9 - len(indices)):
                for j in range(colCount):
                    text_list.insert(firstIdx+offset, None)
                offset += 3
    
        #print "Length of name_list is", len(name_list), "and the length of text_list is", len(text_list)
        if len(text_list) != 172: # something's wrong, most likely a case of ProgramElement containing Code but not Text
            errorLog.write(picklePath + ' ' + f + '\n') # write the name of the troublesome XML file to the error log along with the .msg that contains it
        else:
            master_list.append(text_list) # all good, append to master_list
        
    errorLog.close()
    master_list = master_list[1:]
    for i in range(len(master_list)):
        df.loc[i] = master_list[i]
    df.to_msgpack(picklePath) # highly space efficient, also experimental (requires pandas 0.13 or later). Read with pd.read_msgpack('picklePath')

if __name__ == "__main__":
    setrecursionlimit(getrecursionlimit()*12)
    #print "Reading XML files, this may take a while..."
    files = [f for f in os.listdir('.') if (os.path.isfile(f) and f.endswith('.xml'))] # produce a list of all XML files in the current directory
    #print "Calculating total number of files..."
    fLen = len(files)
    xml2df(files, fLen, str(argv[1]))
