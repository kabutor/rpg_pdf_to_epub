import fitz
import io
from collections import Counter
import sys, getopt

DEBUG = False 

def count_adjust(blocks):
    """
    Count the number of ocurrences from the horizontal coordinate, pick the two most common
    Adjust all the text to those two columns to the one on the left of where text is
    """
    adjust_h = []
    tmp_list = []
    #get number of occurrences
    for w in blocks:
        adjust_h.append(int(w[0])) 
    
    occur = Counter(adjust_h)
    #adjust values to a margin
    margin = 15 
    rows = occur.most_common(2)
    #have to do this for the two columns (a and b)
    row_a = rows[0][0]
    row_b = rows[1][0]
    # row_a is the leftist one
    if (row_a > row_b):
        row_c = row_a
        row_a = row_b
        row_b = row_c
    if DEBUG:
        print("Row_A %i Row_B %i" % (row_a,row_b))
    for w in blocks:
        # must be greater and different and between the margin
        if (int(w[0]) >= row_b):
            if (int(w[0]) == row_b):
                tmp_list.append( (row_b, w[1],w[2],w[3], "\n" + w[4] + "\n",w[5],w[6]))
            else:
                #seven values
                tmp_list.append( (row_b, w[1],w[2],w[3], "<p></p>\n<i>" + w[4] + "</i><p></p>\n",w[5],w[6]))
        elif(int(w[0]) >= row_a):
            if (int(w[0]) == row_a):
                tmp_list.append( (row_a, w[1],w[2],w[3], "\n" + w[4] + "\n",w[5],w[6]))
            else:
                #seven values
                tmp_list.append( (row_a, w[1],w[2],w[3], "<p></p>\n<i>" + w[4] + "</i><p></p>\n",w[5],w[6]))
        else:
            tmp_list.append(w)
    return tmp_list

def sort_text(words):
    """
    Word items are sorted for reading sequence left to right,
    top to bottom.
    """
    block_sorted = sorted(words, key=lambda w: (int(w[0]), int(w[1])) )  # sort by horizontal coordinate
    block_text = ""
    for w in block_sorted:  # fill the line dictionary
        if DEBUG:
            print ("Linea %i / %i : %s" % (w[0], w[1],w[4]) )
        # remove (for now) the images and if len less than 2
        if (not('<image' in w[4][0:20]) and (len(w[4]) > 2)):
            block_text+=(w[4]+'\n')
        
    return block_text 


argumentList = sys.argv[1:]
# Options
options = "hfo:f:"
file_output = "output.txt"
file_mode = "w+" # change this to release
file_input = "c.pdf"
try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--Help"):
            print ("Displaying Help")
        if currentArgument in ("-f"):
            print ("Enable force mode")
            file_mode = "w+"
        if currentArgument in ("-o"):
            print (("output file to %s") % (currentValue))
            file_output = currentValue
        if currentArgument in ("-f"):
            print (("input file to %s") % (currentValue))
            file_input = currentValue
        # TODO: Add else sys.exit(2)
except getrptrerror as err:
    # output error, and return with an error code
    print (str(err))

doc = fitz.open(file_input)
doc_pages = doc.page_count
f = open(file_output,file_mode)

# Title for PANDOC
f.write ('% ' + file_input + '\n')
f.write ('% ' + file_output+ '\n')
doc_pages= 4
for i in range(0,doc_pages):
    page = doc[i]
    texto = page.get_text("blocks")
    texto = count_adjust(texto)
    leer = sort_text(texto)
    f.write(leer)
    ##input("next")

f.close()

doc.close()
