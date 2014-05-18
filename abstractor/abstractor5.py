# Extracts NSF award data from all XML files in the current directory and appends them to a single dataframe which is then written to a CSV file on disk
# Data sourced from - http://www.nsf.gov/awardsearch/download.jsp
# Written by Utkarsh Jaiswal on May 18 2014

from bs4 import BeautifulSoup
from numpy import hstack, matrix
import pandas as pd
import os
 
def xml2df(files, fLen):
    df = pd.DataFrame()
    fileIdx = 1
    for f in files:
        print "Processing", f, "- file", fileIdx, "of", fLen
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
        # We thus append suffixes to each such occurrence to avoid confusing pandas while appending to the existing dataframe
        # We also append parent element names since beautifulsoup flattens the XML hierarchy

        # suffix indices to multiple instances of 'investigator'
        if 'investigator' in name_list:
            firstIdx = name_list.index('investigator')
            if 'institution' in name_list:
                lastIdx = name_list.index('institution')
            elif 'foainformation' in name_list:
                lastIdx = name_list.index('foainformation')
            elif 'programelement' in name_list:
                lastIdx = name_list.index('programelement')
            elif 'programreference' in name_list:
                lastIdx = name_list.index('programreference')
            else:
                lastIdx = len(name_list)
            idx = 1
            for i in range(firstIdx, lastIdx, 7):
                name_list[i+1] = name_list[i] + '-' + name_list[i+1] + '-' + str(idx)
                name_list[i+2] = name_list[i] + '-' + name_list[i+2] + '-' + str(idx)
                name_list[i+3] = name_list[i] + '-' + name_list[i+3] + '-' + str(idx)
                name_list[i+4] = name_list[i] + '-' + name_list[i+4] + '-' + str(idx)
                name_list[i+5] = name_list[i] + '-' + name_list[i+5] + '-' + str(idx)
                name_list[i+6] = name_list[i] + '-' + name_list[i+6] + '-' + str(idx)
                name_list[i] = name_list[i] + '-' + str(idx)
                idx += 1

        # suffix indices to multiple instances of institution
        if 'institution' in name_list:
            firstIdx = name_list.index('institution')
            if 'foainformation' in name_list:
                lastIdx = name_list.index('foainformation')
            elif 'programelement' in name_list:
                lastIdx = name_list.index('programelement')
            elif 'programreference' in name_list:
                lastIdx = name_list.index('programreference')
            else:
                lastIdx = len(name_list)
            idx = 1
            for i in range(firstIdx, lastIdx, 9):
                name_list[i+1] = name_list[i] + '-' + name_list[i+1] + '-' + str(idx)
                name_list[i+2] = name_list[i] + '-' + name_list[i+2] + '-' + str(idx)
                name_list[i+3] = name_list[i] + '-' + name_list[i+3] + '-' + str(idx)
                name_list[i+4] = name_list[i] + '-' + name_list[i+4] + '-' + str(idx)
                name_list[i+5] = name_list[i] + '-' + name_list[i+5] + '-' + str(idx)
                name_list[i+6] = name_list[i] + '-' + name_list[i+6] + '-' + str(idx)
                name_list[i+7] = name_list[i] + '-' + name_list[i+7] + '-' + str(idx)
                name_list[i+8] = name_list[i] + '-' + name_list[i+8] + '-' + str(idx)
                name_list[i] = name_list[i] + '-' + str(idx)
                idx += 1

        # suffix indices to multiple instances of foainformation
        if 'foainformation' in name_list:
            firstIdx = name_list.index('foainformation')
            if 'programelement' in name_list:
                lastIdx = name_list.index('programelement')
            elif 'programreference' in name_list:
                lastIdx = name_list.index('programreference')
            else:
                lastIdx = len(name_list)
            idx = 1
            for i in range(firstIdx, lastIdx, 3):
                name_list[i+1] = name_list[i] + '-' + name_list[i+1] + '-' + str(idx)
                name_list[i+2] = name_list[i] + '-' + name_list[i+2] + '-' + str(idx)
                name_list[i] = name_list[i] + '-' + str(idx)
                idx += 1

        # suffix indices to multiple instances of programelement
        if 'programelement' in name_list:
            firstIdx = name_list.index('programelement')
            if 'programreference' in name_list:
                lastIdx = name_list.index('programreference')
            else:
                lastIdx = len(name_list)
            idx = 1
            for i in range(firstIdx, lastIdx, 3):
                name_list[i+1] = name_list[i] + '-' + name_list[i+1] + '-' + str(idx)
                name_list[i+2] = name_list[i] + '-' + name_list[i+2] + '-' + str(idx)
                name_list[i] = name_list[i] + '-' + str(idx)
                idx += 1

        # suffix indices to multiple instances of programreference
        if 'programreference' in name_list:
            firstIdx = name_list.index('programreference')
            lastIdx = len(name_list)
            idx = 1
            for i in range(firstIdx, lastIdx, 3):
                name_list[i+1] = name_list[i] + '-' + name_list[i+1] + '-' + str(idx)
                name_list[i+2] = name_list[i] + '-' + name_list[i+2] + '-' + str(idx)
                name_list[i] = name_list[i] + '-' + str(idx)
                idx += 1

        # The other elements appear only once and can be deduplicated without suffixing indices

        if 'value' in name_list:
            firstIdx = name_list.index('value')
            name_list[firstIdx] = 'awardinstrument-value'

        if 'code' in name_list:
            firstIdx = name_list.index('code')
            name_list[firstIdx] = 'organization-code'

        if 'directorate' in name_list:
            firstIdx = name_list.index('directorate')
            name_list[firstIdx] = 'organization-directorate'

        if 'longname' in name_list:
            firstIdx = name_list.index('longname')
            name_list[firstIdx] = 'organization-directorate-longname'

        if 'division' in name_list:
            firstIdx = name_list.index('division')
            name_list[firstIdx] = 'organization-division'

        if 'longname' in name_list:
            firstIdx = name_list.index('longname')
            name_list[firstIdx] = 'organization-division-longname'

        if 'signblockname' in name_list:
            firstIdx = name_list.index('signblockname')
            name_list[firstIdx] = 'programofficer-signblockname'

        s1 = pd.Series(text_list, index = name_list, name = f)
        df = df.append(s1, ignore_index=True)

    # Write dataframe to disk as CSV
    df.to_csv('df.csv', sep=',', encoding='utf-8')

if __name__ == "__main__":
    print "Reading XML files, this may take a while..."
    files = [f for f in os.listdir('.') if (os.path.isfile(f) and f.endswith('.xml'))] # produce a list of all XML files in the current directory
    print "Calculating total number of files..."
    fLen = len(files)
    xml2df(files, fLen)
