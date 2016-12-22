import sys  ##used to obtain the command line parameters
            ##check www.tutorialspoint.com/python/python_command_line_arguments.htm for documentation

##  Throughout this code I dont rename any of the fields of data, preferring to use list indecies for speed. Below is a description of what each list item is:
##  item[0] = Hostname
##  item[1] = IP Address
##  item[2] = Patched?
##  item[3] = OS version
##  item[4] = Notes

def main():
    if len(sys.argv) > 2 or len(sys.argv) < 2: ##check if too many args
        print("Incorrect number of arguments, please only pass in the filename of the file to read.")
    else:
        filename = sys.argv[1] ##assign the 2nd command line parameter for filename to filename
        data = removeDuplicates(parseFile(filename)) ##obtain 'data' from file
        data = getUpdateables(data) ##remove unwanted data
        printDataList(data) ##print final dataset

        
def parseFile(filename):
    '''
    try to open the given file, then parse into a list of lists, flagging 'duplicates'
    return list of lists
    '''
    fileContents = []
######open the file
    try:
        f = open(filename)
    except Exception as e: ##various file errors
        print(e)
        sys.exit()

###### read and close the file
    for line in f:
        contents = str.split(line,",") ##convert comma separated string into list of the string split by a comma
        for i in range(len(contents)):
            contents[i] = contents[i].strip()##to remove blank spaces from the strings so that same strings can be found    
        ##Here I would check for and remove headers, but that is not needed as tests on OS Version and Patched? lower down remove it anyway
        if len(contents) > 1:##check that line is not 'blank'
            for item in fileContents:
                if item[0].lower() == contents[0].lower() or item[1].lower() == contents[1].lower(): ##check whether the current item is a duplicate of another in the list (not case sensitive)
                    item.append("dup") ##just append something onto the end of the item that needs to be deleted at the end (since valid data will only ever have 5 fields this allows for a simple <6 check later).
                    contents.append("dup") ##same as above
                    break
            fileContents.append(contents)
    f.close()##no need to keep the file open
    return(fileContents)

def removeDuplicates(data):
    '''
    iterate through list to remove data containing duplicate flags
    return list of lists
    '''
    dataList = []
    for item in data:
        if len(item) < 6: ##valid files only have 5 fields - ones that have been marked as duplicates above have >=6 fields
            dataList.append(item)
    return(dataList)

def getUpdateables(data):
    '''
    iterate through list to remove data that does not fit the brief by comparing items to correct values
    return list of lists
    '''
    dataList = []
    for item in data:
        try:
            float(item[3]) ##if the version cannot be turned into a float then ignore this bit of data as the version 'number' will not be 'higher than 12'
        except:
            continue
        if (item[2].lower() == "no")and(float(item[3]) >= 12.0): ##check that router has not been updated and that OS Version is 12 or above
            dataList.append(item)
    return(dataList)

def printDataList(dataList):
    '''
    iterate through list of data and print out each data in the correct format
    '''
    for data in dataList:
        comment = ""
        if len(data[4]) > 1: ##if there is no comment then 'comment' is left as an empty string so nothing prints out
            comment = "[%s]" % data[4].strip('\n') ##the .strip\n just removes the newline char from the end of the list
        print("%s (%s), OS version %s %s" % (data[0],data[1],str(data[3]),comment)) ##make and print the string with briefed syntax

if __name__ == "__main__": ##runs main()
    main()
