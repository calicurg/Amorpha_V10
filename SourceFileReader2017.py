import Tkinter as TK
import sys
import PC_reader as PCR

all_seps = PCR.ALL_SEPARATORS

#fd = 'c:\\Corpus_Analysis\\DATABASE'
fd = 'c:\\Il\\DATABASE'
#fd = 'C:\\Il\\DataExtraction\\AmorphaPresentation'
######### refsi

RefsiArray = []
OL = []
#rl_1 = []
Refsi = {}
points = [';', ':', '(', ')', ',', '[', ']']
#rl = []
ol = {}
SE = {}
Accs = {0:[], 1:[], 2:[]}


def CleanRefsi():
    
    if len(Refsi) > 0:
        Refsi.clear()
        
    if len(OL) > 0:
        for y in range(len(OL)):
            OL.pop(0)
            
    print 'CleanOL: done'


def Preapre__refsi__array():

    
    for oline in OL:
        si = oline[1]
     #   if si not in all_seps:            
        line = str(oline[0]) +'__'+oline[1]
        RefsiArray.append(line)
    
    

def Fill__Refsi():

    CleanRefsi()

    for k, v in SE.items():
        seinx = k
        ss = v['ss']
        for y in range(len(ss)):
            pos = y
            single = ss[y]
            seinx_line = []
            single = single.lower()

            if single in all_seps:
                continue

            ## put refsi    
            if single in Refsi.keys():
                Refsi[single]['inci'] += 1
                if single not in all_seps:
                    seinx_line = [pos, seinx]
                 ##   Refsi[single]['seinxx'].append(seinx_line)

            else:
                Refsi[single] = {}
                Refsi[single]['inci'] = 1

                ## assign seinx    
                if single not in all_seps:
                    seinx_line = [pos, seinx]
####                    Refsi[single]['seinxx'] = []
####                    Refsi[single]['seinxx'].append(seinx_line)
                else:
                    Refsi[single]['seinxx'] = []
                    
    print 'Refsi filled'

    ########   OL  =======================
    for k, v in Refsi.items():
        si = k
        inci = v['inci']
        
#        seinxx = v['seinxx']
        oline = [inci, si]
        OL.append(oline)

    OL.sort()
    OL.reverse()
    
    print 'Fill_OL() : done'






#######    fn = selected_file
fn = '315__sunitinib.txt'
#fn = 'st_ans.txt'
#fn = 'qw.txt'
#fn = 'All__aspirin__clopidogrel.txt'
#fn = '0_Antiplatelet_resistance.txt'
#fn = 'content.txt'
#fn = 'Entry__Cl_Summary_0666_1.txt'


#fn = 'python__content.txt'
#fn = 'All__content.txt'

#fn = 'DSUR__1.txt'
#fn = 'DSUR__2.txt'
#fn = 'DSUR_#1_DCVAC.txt'
#fn = 'Entry__Cl_Summary_0666_1.txt'
#fn = 'XELJANZ.txt'
#fn = 'Entry__Cl_Ov_exemestane.txt'
#fn = 'Entry__Cl_Ov_Rabeprazole.txt'
#fn = 'DHT__all.txt'
#fn = 'Vilda__all.txt'

#fn = 'Entry__SPC_Truvada.txt'
#fn = 'Entry__Cl_Ov_Clopidogrel.txt'
#fn = 'Entry__Cl_Summary_Anagrelide.txt'
#fn = 'Entry__Cl_Ov_opioids.txt'

#fn = '066606_02_li_text.txt'
#fn = 'GT335_4_fr_wo_tables.txt'
#fn = 'Notes.txt'
#fn = 'orlistat_2_fr.txt'
#fn = selected_file
#fn = 'Entry__Cl_Summary_Anagrelide.txt'

#fn = 'Maria_A_Blasco.txt'
#fn = 'Manchester_United.txt'
#fn = 'Pailperidone_01.txt'
#print 'selected file : ', fn

def ReadTargetFile():
    
    fna = fd+'\\'+fn

    fi = open(fna, 'r')
##    rl_1 = fi.readlines()
    Accs[0] = fi.readlines()
    fi.close()

    print 'Accs[0] raw lines filled'

##fn = '03.txt'
##fna = fd+'\\'+fn
##fi = open(fna, 'r')
##rl_3 = fi.readlines()
##fi.close()
##print 'file 3 : ', len(rl_3), 'se'



def Delete_empty_lines():

    Accs[1] = []
    empty_counter = 0
    for line in Accs[0]:
        st = line.strip()
        if st != '':
            Accs[1].append(st)
        else:
            empty_counter +=1
    print 'Total ', empty_counter, 'empty lines'
    print 'Delete_empty_lines : done'

#Delete_empty_lines()    
#print 'Total : ', len(rl), ' se'


def Replace_points():
    #rl = rllist
    for lindex in range(len(Accs[1])):
        line = Accs[1][lindex]
        
        line = line.strip()
        line = line.lower()
        if line.endswith('.'):
            line = line[:-1]
        for point in points:
            repl_point = ' '+point+' '
            if point in line:
                line = line.replace(point, repl_point)
                line = line.replace('\t', ' ')
                line = line.replace('  ', ' ')
                line = line.replace('  ', ' ')
                line = line.replace('  ', ' ')
        Accs[1][lindex] = line
    print 'point replacement is done'
    
#Replace_points()

def Create_sent_list():
    ol.clear()
    ss = [line.split() for line in Accs[1]]
    print 'ss was created'

    for sindex in range(len(ss)):
        sent = ss[sindex]
        ol[sindex] = sent
    print 'ol was created' 
#Create_sent_list()

def Fill_SE():

    SE.clear()
    for lindex in ol.keys():
        ss = ol[lindex]
        ls = ' '.join(ss)
        ## >>  for Russian version of Semantic_ sorter
        ls = ls.strip()
        try:
            ls = ls.decode('utf-8').lower().encode('utf-8')
        except:
            ls = ls.lower()
            
        ss = ls.split()
        ## <<  for Russian version of Semantic_ sorter
        
        SE[lindex] = {}
        SE[lindex]['ls'] = ls
        SE[lindex]['ss'] = ss
        #print lindex, ls
    print 'Fill_SE : done'

#Fill_SE()


def Excecute_all():
    #Display_selection()
    Replace_points()
    Create_sent_list()
    Fill_SE()


def Start():

    Delete_empty_lines()    
    print 'Total : ', len(Accs[1]), ' sents'
    Replace_points()
    Create_sent_list()
    Fill_SE()
    Fill__Refsi()
##    Preapre__refsi__array()


#Start()    
#root = TK.Tk()

#Excecute_all()    
##    print s
##for line in rl:
##    print line
