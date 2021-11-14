#fi = open('BCL__abstracts.txt', 'r')
#fi = open('Liu-461-6.txt', 'r')
#fna = 'all__titles_47.txt'
#fna = 'ConversionTitles.txt'
#fna = 'AllAbstractsTestConversion.txt'
#fna = 'AllAbstracts.txt'
#fi = open(fna, 'r')
#rl = fi.readlines()
##line = fi.read()
#fi.close()
#
##amt = line.count('PFS')
#print amt
#print len(rl)
Accs = {0:[],
       1:[]
       }

#primer  = 'sensitization'
#primer = 'test conversion'
#primer = 'response'
#primer = 'duration'
TargetDI = {0:''}
rl = []

SeinxxDI = {}


def CentralPassage(left_value, right_value):

    FrOl = []
    FrDI = {}
    primer = TargetDI[0]
    for ls in Accs[0]:
        sl = ls.split()
        if primer not in sl:
            continue
        sinx = sl.index(primer)
        slfr = sl[(sinx-left_value):(sinx+right_value)]
        fr = ' '.join(slfr)
        if fr in FrDI:
            FrDI[fr] += 1
        else:
            FrDI[fr] = 1
            
    for fr, inci in FrDI.items():
        oline = [inci, fr]
        FrOl.append(oline)

    FrOl.sort()
    FrOl.reverse()

    
    return FrOl


def RightPassage(depth):

    FrOl = []
    
    primer = TargetDI[0]
    for ls in Accs[0]:
        sl = ls.split()
        if primer not in sl:
            continue
        sinx = sl.index(primer)
        slfr = sl[sinx:(sinx+depth)]
        fr = ' '.join(slfr)
        if fr in FrDI:
            FrDI[fr] += 1
        else:
            FrDI[fr] = 1
            
    for fr, inci in FrDI.items():
        oline = [inci, fr]
        FrOl.append(oline)

    FrOl.sort()
    FrOl.reverse()

    for ol in FrOl:
        print ol

def LeftPassage(depth):

    FrOl = []
    
    primer = TargetDI[0]
    for ls in Accs[0]:
        sl = ls.split()
        if primer not in sl:
            continue
        sinx = sl.index(primer)
        slfr = sl[(sinx-depth):(sinx+1)]
        fr = ' '.join(slfr)
        if fr in FrDI:
            FrDI[fr] += 1
        else:
            FrDI[fr] = 1
            
    for fr, inci in FrDI.items():
        oline = [inci, fr]
        FrOl.append(oline)

    FrOl.sort()
    FrOl.reverse()

    for ol in FrOl:
        print ol
        
    

def Cc(l, r):
    primer = TargetDI[0]
    print 'primer', primer
    
    Accs[0] = []
    for ls in rl:
        ls = ls.lower()
        #print ls
        #sl = ls.split()
        if primer in ls:
            pos = ls.find(primer)
            if pos > 0:
                ance = ls[(pos-l):(pos+r)]
                #ance = ls[pos:(pos+r)]
                #ance = ance.strip()
                if len(ance.strip()) > len(primer):
                   ## print len(ance), ance
                    Accs[0].append(ance)

    print 'Cc: len(Accs[0])', len(Accs[0])

def PrintRealValues():

#    lfilter  = 'duration of response'
    lfilter = 'response duration'
    for ls in Accs[0]:
#        if 'month' in ls:
#        if 'rituximab' in ls:
        if lfilter in ls:        
            print ls
            
def PrintAll():

    for ls in Accs[0]:
##        if 'month' in ls:
        print ls

        

     
#target = 'free survival '
def Start():
##    target = 'survival'
##    target = 'sensitization'
##    target = 'conversion'
    target = 'contacts'
##    Cc(target, 25, 75)
    Cc(25, 35)
##    print len(Accs[0])
##    PrintRealValues()
##    PrintAll()
##    LeftPassage(1)
##    RightPassage(3)
    PrintRealValues()

#Start()









    
