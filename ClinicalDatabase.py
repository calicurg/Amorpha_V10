import LightLinter as LL
#import win32com.client as win32
import DataLoad
import os
import tkFileDialog as TFD
#import Refsi
import SourceFileReader2017 as SFR
import CC
#import igraph as csar


DataLoad.ParamsDI['dna'] = os.getcwd() ##'C:\\Il\\DiaData' ##ClinicalOverview

LL.Create__root('Clinical Database')

TK = LL.TK
TKDI = LL.TKDI
Accs = {0:[], ## semblocks
        1:[] ## rl
        }

AttrDI = {}

FRAMES = {}
Domains = {}
CS = {} ## k = slot, v = {}, k = attr, value - slot or slot_list
CurSentSet = {0:[]}
SeinxxDI = {}


VsLI = []

RefEsDI = {}

RefsiDI = {}
RefsiOl = []

GrDI = {0:''}

LtDI = {0:''}

def GraphLines():

    LL.TKDI['cv'][0].delete('GR')
    
    ecounter = 0
    for pair, inci in RefEsDI.items():
        
        vinx0 =  pair[0]
        vinx1 =  pair[1]
        weight_factor = 1
        line_weight = weight_factor * inci

        LT = LtDI[0]
        start = LT[vinx0]
        finish = LT[vinx1]
        
        x0, y0 = start[0], start[1]
        x1, y1 = finish[0], finish[1]
        lind = LL.TKDI['cv'][0].create_line(x0, y0, x1, y1,\

                        fill = 'green',\
#                        width = 2,\
                                      
        #### hiding the line width: 22.05.2017 for Anton Artur.
                        width = line_weight,\
                        arrow = LL.TK.LAST,\
                        #arrowshape = (13, 17, 7), \
                        tags = 'li_'+str(ecounter)
                              )
#        print 'lind = ', lind
        ecounter += 1 

#    LL.TKDI['cv'][0].addtag_all('gr')
        

def GraphLabels():
    
    
    lt = LtDI[0]
    for vinx in range(len(lt)):
        pair = lt[vinx]
        si = RefsiOl[vinx][1]
        LL.TKDI['cv'][0].create_text(pair[0], pair[1], \
                              text = si,\
                              fill = 'yellow',\
                              font = 'Courier 8',\
                                 #     state=LINTER.TK.HIDDEN,\
                                      tags = 'la_'+str(vinx))

    LL.TKDI['cv'][0].addtag_all('GR')
    center = LtDI[0].centroid()
    x, y = center[0], center[1]

    zoom_factor = 10
    LL.TKDI['cv'][0].scale('GR', x, y, zoom_factor, zoom_factor)
    
    


def LT():

    gr = GrDI[0]
    lt = gr.layout_fruchterman_reingold()
    LT = csar.Layout(lt)
    LT.center([250, 200])
#    LT.scale(5)
#    print LT.coords
    LtDI[0] = LT

    

    

def GR():

    GrDI[0] = csar.Graph()
    
    amt_vs = len(RefsiOl)
    GrDI[0].add_vertices(amt_vs)
    GrDI[0].delete_vertices(0)
    
    EsLI = RefEsDI.keys()
    GrDI[0].add_edges(EsLI)

    print GrDI[0].summary()
    
    
    


def Es():

    RefEsDI.clear()
    
    sz = LL.TKDI['lx']['frs'].size()
    for y in range(sz):
        line = LL.TKDI['lx']['frs'].get(y)
        lx_sl = line.split('__')
        inci = int(lx_sl[0])
        fr = lx_sl[1]

        sl = fr.split()
        for x in range(len(sl) - 1):
            z = x + 1
            source = sl[x]
            target = sl[z]

            ref_source = RefsiDI[source]['pos']
            ref_target = RefsiDI[target]['pos']

            edge = (ref_source, ref_target)
            if edge in RefEsDI:
                RefEsDI[edge] += inci
            else:
                RefEsDI[edge] = inci
                
                
    print 'Edges: done'            
            
    

def Vs():

    RefsiDI.clear()

    if len(VsLI) > 0:
        for y in range(len(VsLI)):
            VsLI.pop(0)
            
    if len(RefsiOl) > 0:
        for y in range(len(RefsiOl)):
            RefsiOl.pop(0)
            
    
    sz = LL.TKDI['lx']['frs'].size()
    for y in range(sz):
        line = LL.TKDI['lx']['frs'].get(y)
        lx_sl = line.split('__')
        inci = int(lx_sl[0])
        fr = lx_sl[1]

        sl = fr.split()
        for si in sl:
            if si in RefsiDI:
                RefsiDI[si]['inci'] += inci
            else:
                RefsiDI[si] = {'inci':inci}
                
    for k, v in RefsiDI.items():
        ol = [v, k]
        RefsiOl.append(ol)
        
    RefsiOl.sort()
    RefsiOl.reverse()

    for x in range(len(RefsiOl)):
        ol = RefsiOl[x]
        si = ol[1]
        RefsiDI[si]['pos'] = x
        
    print 'Vertices: done'        
        
    
def BuildGraph():

    Vs()
    Es()
    GR()
    LT()
    GraphLines()
    GraphLabels()
        


def ExportFragments():

    fna = LL.TKDI['en']['refsi'].get()
    fna += '.txt'
    fi = open(fna, 'w')
    print 'frs size:', LL.TKDI['lx']['frs'].size()
    for cs in range(LL.TKDI['lx']['frs'].size()):
        line = LL.TKDI['lx']['frs'].get(cs)
        line += '\n' 
        fi.write(line)

    fi.close()
                    

##def CentralPassage():
##
##    line = LL.TKDI['en']['refsi'].get()
##    si = line.split('__')[1]
##    si = si.strip()
##
##    ##CC.primer = si #.encode('utf-8')
####    CC.TargetDI[0] = si #.encode('utf-8')
####    CC.rl = Accs[1]
####    CC.Cc(25, 45)
##
##    LL.TKDI['lx']['frs'].delete(0, TK.END)
##    left_value = int(LL.TKDI['en']['left'].get())
##    right_value = int(LL.TKDI['en']['right'].get())
##    FrOl = CC.CentralPassage(left_value, right_value)
##    print 'len(FrOl)', len(FrOl)
##    for fl in FrOl:
##        lxline = str(fl[0])+'__'+fl[1]
##        LL.TKDI['lx']['frs'].insert(TK.END, lxline)
##    
    

def RightPassage():
    
    line = LL.TKDI['en']['refsi'].get()
    si = line.split('__')[1]
    si = si.strip()

    CC.primer = si #.encode('utf-8')
    CC.rl = Accs[1]
    CC.Cc(25, 45)

    LL.TKDI['lx']['frs'].delete(0, TK.END)
    
    depth = int(LL.TKDI['en']['right'].get())
    FrOl = CC.RightPassage(depth)
    print 'len(FrOl)', len(FrOl)
    for fl in FrOl:
        lxline = str(fl[0])+'__'+fl[1]
        LL.TKDI['lx']['frs'].insert(TK.END, lxline)
                 

def LeftPassage():

    line = LL.TKDI['en']['refsi'].get()
    si = line.split('__')[1]
    si = si.strip()

    CC.primer = si #.encode('utf-8')
    CC.rl = Accs[1]
    CC.Cc(25, 45)

    LL.TKDI['lx']['frs'].delete(0, TK.END)
    depth = int(LL.TKDI['en']['left'].get())
    FrOl = CC.LeftPassage(depth)
    print 'len(FrOl)', len(FrOl)
    for fl in FrOl:
        lxline = str(fl[0])+'__'+fl[1]
        LL.TKDI['lx']['frs'].insert(TK.END, lxline)
                 

def GetSeinxx(si):

    SeinxxDI[si] = []
    
    for seinx in range(len(Accs[1])):
        ls = Accs[1][seinx]
        ls = ls.lower()
        sl = ls.split()
        if si in sl:
            if sl.count(si) == 1:
                pos = sl.index(si)
                ol = [seinx, pos]
                SeinxxDI[si].append(ol)
                
            elif sl.count(si) > 1:
                inxi = sl.count(si) 
                for x in range(inxi):
                    pos = sl.index(si)
                    ol = [seinx, pos]
                    SeinxxDI[si].append(ol)
                    sl = sl[(pos+1):]
                    
                    
def CentralPassage():

    FrsDI = {}
    FrOl = []

    line = LL.TKDI['en']['refsi'].get()
    si = line.split('__')[1]
    si = si.strip()

    LL.TKDI['lx']['frs'].delete(0, TK.END)
    left_value = int(LL.TKDI['en']['left'].get())
    right_value = int(LL.TKDI['en']['right'].get())
    print 'left_value', left_value
    print 'right_value', right_value
##    FrOl = CC.CentralPassage(left_value, right_value)
##    print 'len(FrOl)', len(FrOl)
##    for fl in FrOl:
##        lxline = str(fl[0])+'__'+fl[1]
##        LL.TKDI['lx']['frs'].insert(TK.END, lxline)


    CC.TargetDI[0] = si
    CC.rl = Accs[1]

    if si not in SeinxxDI:
        GetSeinxx(si)

    seinx_pos_array = SeinxxDI[si]
    for ol in seinx_pos_array:
        seinx, pos = ol[0], ol[1]

        left_border = pos - left_value ## left_value is negative
        if left_border < 0:
            left_border = 0
            
        right_border = pos + right_value
        ls = Accs[1][seinx]
        ls = ls.lower()
        sl = ls.split()
        len_sent = len(sl)
        if len_sent < right_border:
            right_border = len_sent

        sl_fr = sl[left_border:right_border]

        array = []
        for single in sl_fr:
            if single in SFR.PCR.ALL_SEPARATORS:
                continue
            array.append(single)


        if right_value > 0 and si not in array:
            continue
        fr = ' '.join(array)
        fr = fr.strip()
        if fr == si:
            continue
        if fr in FrsDI:
            FrsDI[fr] += 1
        else:
            FrsDI[fr] = 1

    print 'FrsDI filled'

    for k, v in FrsDI.items():
        ol = [v, k]
        FrOl.append(ol)

    FrOl.sort()
    FrOl.reverse()

    for ol in FrOl:
        lx__line = str(ol[0])+'__'+ol[1]
        LL.TKDI['lx']['frs'].insert(TK.END, lx__line)
        
    
            
            
        
        
    
        
        
def RefsiCC():

    line = LL.TKDI['en']['refsi'].get()
    si = line.split('__')[1]
    si = si.strip()

    CC.TargetDI[0] = si
    CC.rl = Accs[1]
    CC.Cc(25, 45)
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    for ls in CC.Accs[0]:
        ls += '\n'
        LL.TKDI['tx'][0].insert(TK.END,  ls)
    

def ShowCC():

    line = LL.TKDI['en']['frs'].get()
    si = line.split('__')[1]
    si = si.strip()

    CC.TargetDI[0] = si
    CC.rl = Accs[1]
    CC.Cc(25, 45)
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    for ls in CC.Accs[0]:
        ls += '\n'
        LL.TKDI['tx'][0].insert(TK.END,  ls)
    
#    CC.PrintAll()    
    

    

def RelevantSents():

    SeOl = []
    line = LL.TKDI['en']['refsi'].get()
    si = line.split('__')[1]
    for seinx, v in Refsi.SE.items():
        ss = v['ss']
        if si in ss:
            pos = ss.index(si)
            ol = [pos, seinx]
            SeOl.append(ol)

    SeOl.sort()
    CurSentSet[0] =  SeOl
    LL.TKDI['lx']['ls'].delete(0, TK.END)
    for oline in SeOl:
        seinx = oline[1]
        lxline = Refsi.SE[seinx]['ls'] ##str(seinx)+'__'+
        LL.TKDI['lx']['ls'].insert(TK.END, lxline)
        
            
            
        
def ReadRefsiFromFile():

    fna =     LL.TKDI['en']['attr_path'].get()
    fi = open(fna, 'r')
    rl = fi.readlines()
    fi.close()

    array = [ls.strip() for ls in rl]
    LL.Fill__lx(array, 'refsi')


def GetRefsi():

##    Refsi.rl = Accs[1]
##    Refsi.FillRefsi()
##    fna = 'c:\Il\DATABASE\Entry__Cl_Ov_exemestane.txt'
##    fi = open(fna, 'r')
##    rl = fi.readlines()
    SFR.Accs[0] = Accs[1]
    SFR.Start()
    
    LL.TKDI['lx']['refsi'].delete(0, TK.END)
    
    for ol in SFR.OL: ##Refsi.Ol:
        lxline = str(ol[0])+'__'+ol[1]
        LL.TKDI['lx']['refsi'].insert(TK.END, lxline)
        
#    Refsi.PrintoutOl()
    
    

def ShowAllSemblocks():

    LL.Fill__lx(Accs[0], 'semblock')       
    


def LimitSemblocksToAttrDI():

    array = AttrDI.keys()
    array.sort()
    LL.Fill__lx(array, 'semblock')       
    
    

def SelectFile():

    fna = TFD.askopenfilename()
    LL.TKDI['en']['attr_path'].delete(0, TK.END)
    LL.TKDI['en']['attr_path'].insert(0, fna)

def Read_word_file():

    fna = LL.TKDI['en']['attr_path'].get()
    WD = win32.Dispatch('Word.Application')
    Doc = WD.Documents.Open(fna)

    limit = Doc.Sentences.Count
    Accs[1] = []
    for y in range(1, limit):
        
        tx = Doc.Sentences(y).Text
        #print tx
        Accs[1].append(tx)
   

    LL.Fill__lx(Accs[1], 'ls')    
        
    

def Read_text_file():

    fna =     LL.TKDI['en']['attr_path'].get()
    fi = open(fna, 'r')
    rl = fi.readlines()
    fi.close()

    arr = []
    LxArray = []
    Accs[1] = []
    for ls in rl:
        ls = ls.strip()
        if len(ls) > 1:
            if '. ' in ls:            
                sl = ls.split('. ')
                for sent in sl:
                    if len(sent) > 1: 
                        arr.append(sent)            
            else:
                arr.append(ls)            


    for el in enumerate(arr):
        inx = el[0]
        ls = el[1]
        ls = ls.strip()
        if len(ls) > 1:
            line = str(inx)+'__'+ls
## 26/05/2017           Accs[1].append(line)
            Accs[1].append(ls)
            LxArray.append(line)
             
    

    LL.Fill__lx(LxArray, 'ls')    
    
    

##### Text input   ================================
def Set_second_drug():

    si = LL.TKDI['en']['attr_slots'].get()
    LL.TKDI['en']['second_drug'].delete(0, TK.END)
    LL.TKDI['en']['second_drug'].insert(0, si)


def Set_first_drug():

    si = LL.TKDI['en']['attr_slots'].get()
    LL.TKDI['en']['first_drug'].delete(0, TK.END)
    LL.TKDI['en']['first_drug'].insert(0, si)

##    LL.Add__entry('first_drug', 5, 2, 1, 20, 'Arial 14')
##    LL.Add__entry('second_drug', 5, 3, 1, 20, 'Arial 14')

def Set__current__study__attrslot():

    si = LL.TKDI['en']['attr_slots'].get()
    LL.TKDI['en']['current_study'].delete(0, TK.END)
    LL.TKDI['en']['current_study'].insert(0, si)

def Set__current__study__slot():

    si = LL.TKDI['en']['slots'].get()
    LL.TKDI['en']['current_study'].delete(0, TK.END)
    LL.TKDI['en']['current_study'].insert(0, si)
    
    

def Delete__semblock():

    cs = int(LL.TKDI['lx']['semblock'].curselection()[0])
    si = LL.TKDI['lx']['semblock'].get(cs)
    
    LL.TKDI['lx']['semblock'].delete(cs)
    Accs[0].remove(si)
    
    
    
def Rename__slot():

    semblock = LL.TKDI['en']['semblock'].get()
    ren_slot = LL.TKDI['en']['slots'].get()
    cs = int(LL.TKDI['lx']['slots'].curselection()[0])
    old_slot = LL.TKDI['lx']['slots'].get(cs)
    CS[ren_slot] = {}
    for k, v in CS[old_slot].items():
        CS[ren_slot][k] = v
        
    CS.pop(old_slot)
    LL.TKDI['lx']['slots'].delete(cs)
    LL.TKDI['lx']['slots'].insert(0,ren_slot)
    FRAMES[semblock].append(ren_slot)
    

def Clone__cs():

    slot = LL.TKDI['en']['slots'].get()    
    new_slot = slot+'_copy'
    
    CS[new_slot] = {}
    for k, v in CS[slot].items():
        CS[new_slot][k] = v

    LL.TKDI['lx']['slots'].insert(0, new_slot)         

    

def Assign__domain():

    semblock = LL.TKDI['en']['attrs'].get()
    domain = LL.TKDI['en']['counterpart'].get()
    Domains[semblock] = domain

    print 'Assign__domain:', semblock, 'is', domain

def Assign__value():

    pass
    ok = 0
    attr = LL.TKDI['en']['attrs'].get()
    slot = LL.TKDI['en']['slots'].get()
    value = LL.TKDI['en']['attr_slots'].get()
    
        
    if len(attr) < 1:
        ok = 1
        print 'please, select attr'
        
    if len(slot) < 1:
        ok = 1
        print 'please, select slot'
        
    if len(value) < 1:
        ok = 1
        print 'please, select value'
        
    if ok == 0:
        if slot in CS:
            CS[slot][attr] = value
        else:
            CS[slot] = {attr:value}

        line = attr+'__'+value            
        LL.TKDI['lx']['cs'].insert(0, line)
##        print 'CS:', CS
        

def ReadText():

    DataLoad.ParamsDI['dna'] = 'c:/Il/Amorpha/FromCrawler/PsAr'
    rl = DataLoad.ReadTextfile('Risk.txt')

    arr = []
    for ls in rl:
        ls = ls.strip()
        if len(ls) > 1: 
            arr.append(ls)            


    for el in enumerate(arr):
        inx = el[0]
        ls = el[1]
        ls = ls.strip()
        if len(ls) > 1:
            line = str(inx)+'__'+ls
            Accs[1].append(line)            
    
 #   DataLoad.ParamsDI['dna'] = 'C:\\Il\\ClinicalOverview'

    LL.Fill__lx(Accs[1], 'ls')    
    


#### Data

def LoadDomains():

    DataLoad.LoadDI('Domains.li')
    try: 
        for k, v in DataLoad.AI['Domains'].items():
            Domains[k] = v
    except:
        print 'Domains was not loaded!'
    
def LoadCS():

    DataLoad.LoadDI('CS.li')
    try: 
        for k, v in DataLoad.AI['CS'].items():
            CS[k] = v
    except:
        pass

def LoadFRAMES():

    try:

        DataLoad.LoadDI('FRAMES.li')
        for k, v in DataLoad.AI['FRAMES'].items():
            FRAMES[k] = v
    
    except:
        print 'FRAMES were not loaded!'

def LoadAttrDI():

    DataLoad.LoadDI('AttrDI.li')
    for k, v in DataLoad.AI['AttrDI'].items():
        AttrDI[k] = v
        

def Adjust__counterparts():

    array = DataLoad.AL['semblocks']
    array.sort()
    LL.Fill__lx(array, 'counterpart')

    
def LoadSemblocks():

    try:
        DataLoad.LoadLI('semblocks.li')
        LL.Fill__lx(DataLoad.AL['semblocks'],  'semblock')
        Accs[0] = DataLoad.AL['semblocks']

        Adjust__counterparts()
    except:
        print 'Semblocks were not loaded!'

def DumpDomains():
    
    DataLoad.AI['Domains'] = Domains
    DataLoad.DumpDI('Domains')
    

def DumpCS():
    
    DataLoad.AI['CS'] = CS
    DataLoad.DumpDI('CS')

def DumpFRAMES():

    DataLoad.AI['FRAMES'] = FRAMES
    DataLoad.DumpDI('FRAMES')
    
def DumpAttrDI():
    DataLoad.AI['AttrDI'] = AttrDI
    DataLoad.DumpDI('AttrDI')

def DumpSemblocks():
    DataLoad.AL['semblocks'] = Accs[0]
    DataLoad.DumpLI('semblocks')

def AllDumps():

    DumpSemblocks()
    DumpAttrDI()
    DumpFRAMES()
    DumpCS()
    DumpDomains()

    

#########     Semantics

def Insert__attr__slot():

    ok = 0
    semblock = LL.TKDI['en']['attrs'].get()
    
    if len(semblock) < 1:
        ok = 1
        print 'please, write the attr'
    
    slot = LL.TKDI['en']['attr_slots'].get()
    slot = slot.lower()
    if len(slot) < 1:
        ok = 1
        print 'please, write attr slot'

    if ok == 0:
        if semblock in FRAMES:
            if slot not in FRAMES[semblock]:
                FRAMES[semblock].append(slot)
                LL.TKDI['lx']['attr_slots'].insert(0, slot)
        else:            
            FRAMES[semblock] = [slot]
            LL.TKDI['lx']['attr_slots'].insert(0, slot)
            
      

def Insert__slot():

    ok = 0
    semblock = LL.TKDI['en']['semblock'].get()
    attr = LL.TKDI['en']['attrs'].get()
    
    if len(semblock) < 1:
        ok = 1
        print 'please, write the semblock'
    
    slot = LL.TKDI['en']['slots'].get()
    slot = slot.lower()
    if len(slot) < 1:
        ok = 1
        print 'please, write the slot'

    if ok == 0:
        if semblock in FRAMES:
            if slot not in FRAMES[semblock]:
                FRAMES[semblock].append(slot)
        else:            
            FRAMES[semblock] = [slot]
            
        LL.TKDI['lx']['slots'].insert(0, slot)


########    ### default parameters
        if slot not in CS:
            CS[slot] = {}
        all_attrs = AttrDI[semblock]
       # print all_attrs
        if 'STUDY' in all_attrs:
            si = LL.TKDI['en']['current_study'].get()
            if len(si) > 1:
                
                CS[slot]['STUDY'] = si

                line = 'STUDY__'+si            
                LL.TKDI['lx']['cs'].insert(0, line)

        if 'Frist__drug' in all_attrs:
            si = LL.TKDI['en']['first_drug'].get()
            if len(si) > 1:
               
                CS[slot]['Frist__drug'] = si

                line = 'Frist__drug__'+si            
                LL.TKDI['lx']['cs'].insert(0, line)
                
        if 'Second__drug' in all_attrs:
            si = LL.TKDI['en']['second_drug'].get()
            if len(si) > 1:
                
                CS[slot]['Second__drug'] = si

                line = 'Second__drug__'+si            
                LL.TKDI['lx']['cs'].insert(0, line)

       
    
def Insert__attr():

    ok = 0
    semblock = LL.TKDI['en']['semblock'].get()
    attr = LL.TKDI['en']['attrs'].get()
    
    if len(semblock) < 1:
        ok = 1
        print 'please, write the semblock'
        
    if len(attr) < 1:
        ok = 1
        print 'please, write the attr'
        
    if ok == 0:
        if semblock in AttrDI:
            if attr in AttrDI[semblock]:
                print 'attribute exists!'
            else:                
                AttrDI[semblock].append(attr)
        else:
            AttrDI[semblock] = [attr]
            
        LL.TKDI['lx']['attrs'].insert(0, attr)
        

def Insert__semblock():

    si = LL.TKDI['en']['semblock'].get()
    si = si.strip()
    if len(si) < 1:
        print 'please, write the semblock'
    else:
        Accs[0].append(si)
        LL.TKDI['lx']['semblock'].insert(0, si)
        DataLoad.AL['semblocks'] = Accs[0]

        Adjust__counterparts()



def Counterframe__to__attr():

    ok = 0
    semblock = LL.TKDI['en']['semblock'].get()
    attr = LL.TKDI['en']['counterpart'].get()
    
    if len(semblock) < 1:
        ok = 1
        print 'please, write the semblock'
        
    if len(attr) < 1:
        ok = 1
        print 'please, write the attr'
        
    if ok == 0:
        if semblock in AttrDI:
            if attr not in AttrDI[semblock]:
                AttrDI[semblock].append(attr)
                LL.TKDI['lx']['attrs'].insert(0, attr)
        else:
            AttrDI[semblock] = [attr]            
            LL.TKDI['lx']['attrs'].insert(0, attr)
 
    
        
        


#####  Linter ======================

def Add__canvas():

    LL.TKDI['cv'] = {0:LL.TK.Canvas(LL.TKDI['fr']['cv'])}
    LL.TKDI['cv'][0].grid(row = 1, column = 1)
    LL.TKDI['cv'][0]['bg'] = 'black'
    LL.TKDI['cv'][0]['width'] = 500
    LL.TKDI['cv'][0]['height'] = 400
    
    

    

    
        

def Add__frames():

##       LL.Add__one__frame('00', 'root', 1, 1)
##    #LL.Add__one__frame(1, 'root', 1,0)
##    LL.TKDI['nb'] = {0:LL.ttk.Notebook(LL.TKDI['fr']['00'])}    
##    LL.TKDI['nb'][0].grid(row = 1, column = 1)
##
##    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['zero'], text = 'Disassembly')
##    LL.Add__one__frame(0, 'zero', 1, 1)
##
##    LL.TKDI['fr'][3] = LL.TK.Frame(LL.TKDI['nb'][0])
##    LL.TKDI['nb'][0].add(LL.TKDI['fr'][3], text = 'Blocks')
##    LL.Add__lx('blocks', 3, 1, 1, 10, 10, 'Arial 12') ## all Olly-defined blocks
##    LL.Add__lx('block_content', 3, 1, 2, 50, 10, 'Courier 12')## the content
##    LL.TKDI['lx']['blocks'].bind('<KeyRelease>', reflect__block)
##    LL.TKDI['lx']['blocks'].bind('<ButtonRelease>', reflect__block)
##
##    
    LL.Add__one__frame('0', 'root', 1, 1)
    LL.Add__one__frame('00', '0', 1, 1) ## path --> Notebook
##       LL.Add__one__frame('00', 'root', 1, 1)
    LL.TKDI['nb'] = {0:LL.ttk.Notebook(LL.TKDI['fr']['00'])}    
    LL.TKDI['nb'][0].grid(row = 1, column = 1)    
##    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])
    LL.TKDI['fr']['zero'] = LL.TK.Frame(LL.TKDI['nb'][0])    
    LL.TKDI['nb'][0].add(LL.TKDI['fr']['zero'], text = 'Concordance')

    LL.TKDI['fr']['one'] = LL.TK.Frame(LL.TKDI['nb'][0])    
#    LL.TKDI['nb'][0].add(LL.TKDI['fr']['one'], text = 'Graph')

##    LL.TKDI['fr']['two'] = LL.TK.Frame(LL.TKDI['nb'][0])    
##    LL.TKDI['nb'][0].add(LL.TKDI['fr']['two'], text = 'Semblocks')


    LL.Add__one__frame(0, 'zero', 0, 1) ## path
##    LL.Add__one__frame(1, 'two', 1, 1) ## semblocks
##    LL.Add__one__frame(2, 'two',  2, 1) ## buttons
    LL.Add__one__frame(3, 'zero', 3, 1) ## Tx
    LL.Add__one__frame('cv', 'one', 1, 1) ## Graph Canvas
    




    
    LL.Add__one__frame(8, '0', 2, 1) ## left, right
    LL.Add__one__frame(7, '0', 0, 1) ## scales
    LL.Add__one__frame(4, 'root', 1, 0) ## ls
    ## slot attrs table LL.Add__one__frame(5, 0, 3, 1) ## slot attrs table

def Add__entries():

    LL.Add__entry('attr_path', 0, 1, 1, 30, 'Arial 8')

    LL.Add__button('SelectFile', 0,1,3, 6, '...')
    LL.TKDI['bu']['SelectFile']['command'] = SelectFile

    LL.Add__button('ReadTextFile', 0,1,4, 15, 'Read Text')
    LL.TKDI['bu']['ReadTextFile']['command'] = Read_text_file
    

##    LL.Add__button('ReadWordFile', 0,1,5, 15, 'Read Word')
##    LL.TKDI['bu']['ReadWordFile']['command'] = Read_word_file


def reflect__semblock(event):
        
    lxname = 'semblock'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)

    semblock = si
    if semblock in AttrDI:
        array = AttrDI[semblock]
        array.sort()
    else:
        array = []
    LL.Fill__lx(array, 'attrs')
    LL.TKDI['en']['attrs'].delete(0, TK.END)

    if semblock in FRAMES:
        array = FRAMES[semblock]
        array.sort()
    else:
        array = []
    LL.Fill__lx(array, 'slots')
    

def reflect__ls(event):

    lxname = 'ls'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)

    if  '__' in si:
        ls = si.split('__')[1]
    else:
        ls = si
    LL.TKDI['tx'][0].delete('1.0', TK.END)
    LL.TKDI['tx'][0].insert('1.0', ls)

            
def reflect__attr(event):
        
    lxname = 'attrs'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)

    semblock = si

    if semblock in Domains:
        semblock = Domains[semblock]
    
    if semblock in FRAMES:
        array = FRAMES[semblock]
        array.sort()
    else:
        array = []
    LL.Fill__lx(array, 'attr_slots')

        

def reflect__slot(event):

    lxname = 'slots'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)

    slot = si
    LL.TKDI['lx']['cs'].delete(0, TK.END)
    arr = []
    if slot in CS:
        for k, v in CS[slot].items():
            line = k +'__'+v
            arr.append(line)
    arr.sort()
    for ls in arr:
        LL.TKDI['lx']['cs'].insert(TK.END, ls)
            
        
def reflect__attr__slot(event):

    lxname = 'attr_slots'
    cs = int(LL.TKDI['lx'][lxname].curselection()[0])
    si = LL.TKDI['lx'][lxname].get(cs)
    LL.TKDI['en'][lxname].delete(0, TK.END)
    LL.TKDI['en'][lxname].insert(0, si)

    slot = si
    LL.TKDI['lx']['cs'].delete(0, TK.END)  
    if slot in CS:
        for k, v in CS[slot].items():
            line = k +'__'+v
            LL.TKDI['lx']['cs'].insert(TK.END, line)

def reflect__refsi(event):

    LL.reflect__lx__in__entry('refsi')
    
    RefsiCC()

def reflect__scale(event):

    left__value = LL.TKDI['sc'][0].get()
    stand_left = -1*left__value
    LL.TKDI['en']['left'].delete(0, TK.END)
    LL.TKDI['en']['left'].insert(0, stand_left)

    right__value = LL.TKDI['sc'][1].get()
    LL.TKDI['en']['right'].delete(0, TK.END)
    LL.TKDI['en']['right'].insert(0, right__value)

    CentralPassage()
    
    
def Add__lxx():
    
####    LL.Add__lx('semblock', 1, 1, 1, 15, 3, 'Arial 10')
####    LL.TKDI['lx']['semblock'].bind('<KeyRelease>', reflect__semblock)
####    LL.TKDI['lx']['semblock'].bind('<ButtonRelease>', reflect__semblock)
####
####    LL.Add__lx('attrs', 1, 1, 2, 15, 3, 'Arial 10')
####    LL.TKDI['lx']['attrs'].bind('<KeyRelease>', reflect__attr)
####    LL.TKDI['lx']['attrs'].bind('<ButtonRelease>', reflect__attr)
####
####    LL.Add__lx('slots', 1, 1, 3, 15, 3, 'Arial 10')
####    LL.TKDI['lx']['slots'].bind('<KeyRelease>', reflect__slot)
####    LL.TKDI['lx']['slots'].bind('<ButtonRelease>', reflect__slot)
####
####
####    LL.Add__lx('attr_slots', 1, 1, 4, 15, 3, 'Arial 10')
##    LL.TKDI['lx']['attr_slots'].bind('<KeyRelease>', reflect__attr__slot)
##    LL.TKDI['lx']['attr_slots'].bind('<ButtonRelease>', reflect__attr__slot)



##    LL.Add__lx('cs', 1, 1, 5, 25, 3, 'Arial 10')#14')

    ## slot attrs table    
####    LL.Add__one__frame(5, 1, 3, 4) ## slot attrs table
####    for z in range(6):
####        LL.TKDI['en'][(0, z)] = TK.Entry(LL.TKDI['fr'][5])
####        LL.TKDI['en'][(0, z)].grid(row = z, column = 1)
####        LL.TKDI['en'][(0, z)]['font'] = 'Arial 14'
####        
####        LL.TKDI['en'][(1, z)] = TK.Entry(LL.TKDI['fr'][5])
####        LL.TKDI['en'][(1, z)].grid(row = z, column = 2)
####        LL.TKDI['en'][(1, z)]['font'] = 'Arial 14'
          

    
### 26/05/2017    LL.Add__lx('counterpart', 3, 1, 1, 15, 5, 'Arial 10')#14')

### 12/07/2017   
    LL.Add__lx('frs',   4, 1, 1, 25, 7, 'Arial 16')
    
    LL.Add__lx('refsi', 4, 5, 1, 20, 5, 'Arial 16')
    LL.TKDI['lx']['refsi'].bind('<KeyRelease>', reflect__refsi)
    LL.TKDI['lx']['refsi'].bind('<ButtonRelease>', reflect__refsi)

    
    LL.Add__lx('ls',    4, 10, 1, 20, 4, 'Arial 16')
    LL.TKDI['lx']['ls'].bind('<KeyRelease>', reflect__ls)
    LL.TKDI['lx']['ls'].bind('<ButtonRelease>', reflect__ls)




##    LL.Add__one__frame(5, 4, 3, 5) ## slot attrs table
##    LL.Add__entry('current_study', 5, 1, 1, 7, 'Arial 10')
##    LL.Add__entry('first_drug',    5, 2, 1, 7, 'Arial 10')
##    LL.Add__entry('second_drug',   5, 3, 1, 7, 'Arial 10')
    LL.Add__entry('left',          8, 1, 1, 7, 'Arial 10')
    LL.TKDI['en']['left'].insert(0, 1)
    LL.Add__entry('right',         8, 1, 4, 7, 'Arial 10')     
    LL.TKDI['en']['right'].insert(0, 1)

    
    LL.TKDI['sc'][0] = TK.Scale(LL.TKDI['fr'][7])
    LL.TKDI['sc'][0].grid(row = 1, column = 0)
    LL.TKDI['sc'][0]['length'] = 270
    LL.TKDI['sc'][0]['from'] = -7
    LL.TKDI['sc'][0]['to'] = 0
    LL.TKDI['sc'][0].set(0) 
    LL.TKDI['sc'][0]['orient'] = TK.HORIZONTAL
    LL.TKDI['sc'][0]['tickinterval'] = 1
    LL.TKDI['sc'][0].bind('<KeyRelease>', reflect__scale)
    LL.TKDI['sc'][0].bind('<ButtonRelease>', reflect__scale)
    
    
    LL.TKDI['sc'][1] = TK.Scale(LL.TKDI['fr'][7])
    LL.TKDI['sc'][1].grid(row = 1, column = 1)
    LL.TKDI['sc'][1]['length'] = 270
    LL.TKDI['sc'][1]['from'] = 0
    LL.TKDI['sc'][1]['to'] = 7
    LL.TKDI['sc'][1]['orient'] = TK.HORIZONTAL
    LL.TKDI['sc'][1]['tickinterval'] = 1
    LL.TKDI['sc'][1].bind('<KeyRelease>', reflect__scale)
    LL.TKDI['sc'][1].bind('<ButtonRelease>', reflect__scale)
    



def Add__txx():

    LL.TKDI['tx'][0] = TK.Text(LL.TKDI['fr'][3])
    LL.TKDI['tx'][0].grid(row = 3, column = 2)
    LL.TKDI['tx'][0]['width'] = 70
    LL.TKDI['tx'][0]['height'] = 12#15
    LL.TKDI['tx'][0]['font'] = 'Courier 16 bold'
##    LL.TKDI['tx'][0]['fg'] = 'blue'
   
    
    

def Add__buttons():

    pass

####    LL.TKDI['bu'][0] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][0].grid(row = 1, column = 1)
####    LL.TKDI['bu'][0]['text'] = 'Insert semblock'    
####    LL.TKDI['bu'][0]['command'] = Insert__semblock
####
####    LL.TKDI['bu'][1] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][1].grid(row = 1, column = 2)
####    LL.TKDI['bu'][1]['text'] = 'Insert attribute'    
####    LL.TKDI['bu'][1]['command'] = Insert__attr
####
####    LL.TKDI['bu'][2] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][2].grid(row = 1, column = 3)
####    LL.TKDI['bu'][2]['text'] = 'Insert slot'    
####    LL.TKDI['bu'][2]['command'] = Insert__slot
####
####    LL.TKDI['bu'][3] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][3].grid(row = 1, column = 4)
####    LL.TKDI['bu'][3]['text'] = 'Insert__attr__slot'    
####    LL.TKDI['bu'][3]['command'] = Insert__attr__slot
####    LL.TKDI['bu'][3]['bd'] = 7
####    LL.TKDI['bu'][3]['relief'] = TK.RAISED
####
####
####    LL.TKDI['bu'][4] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][4].grid(row = 1, column = 5)
####    LL.TKDI['bu'][4]['text'] = 'Counterframe ==>> attr'    
####    LL.TKDI['bu'][4]['command'] = Counterframe__to__attr
####    LL.TKDI['bu'][4]['bd'] = 7
####    LL.TKDI['bu'][4]['relief'] = TK.RAISED
####
####    LL.TKDI['bu'][5] = LL.TK.Button(LL.TKDI['fr'][2])
####    LL.TKDI['bu'][5].grid(row = 1, column = 6)
####    LL.TKDI['bu'][5]['text'] = 'Assign  value'    
####    LL.TKDI['bu'][5]['command'] = Assign__value
####    LL.TKDI['bu'][5]['bd'] = 7
####    LL.TKDI['bu'][5]['relief'] = TK.RAISED

    

def Go__to__ls():

    line = LL.TKDI['en']['ls'].get()
    if line.isdigit() == True:
        seinx = int(line)
        LL.TKDI['lx']['ls'].see(seinx)
        LL.TKDI['lx']['ls'].selection_set(seinx)
        
    
        
    
def Create__menu():

    LL.Create__menu()
####    TKDI['me'][0] = TK.Menu(TKDI['fr']['root'])
####    TKDI['me'][1] = TK.Menu(TKDI['me'][0])

    LL.TKDI['me'][1].add_command(label = 'Go to sentence', command = Go__to__ls)
##    LL.TKDI['me'][1].add_command(label = 'Accept_block_content', command = Accept_block_content)

   ## LL.TKDI['me'][1]['text'] = 'Semantics'    
    LL.TKDI['me'][2] = TK.Menu(TKDI['me'][0])
    LL.TKDI['me'][2].add_command(label = 'Dump all', command = AllDumps)
    LL.TKDI['me'][2].add_command(label = 'Export Fragments', command = ExportFragments)

    

##    LL.TKDI['me'][3] = TK.Menu(TKDI['me'][0])
##    LL.TKDI['me'][3].add_command(label = 'Insert__semblock', command = Insert__semblock)
##    LL.TKDI['me'][3].add_command(label = 'Delete__semblock', command = Delete__semblock)
##    LL.TKDI['me'][3].add_command(label = 'LimitSemblocksToAttrDI', command = LimitSemblocksToAttrDI)
##    LL.TKDI['me'][3].add_command(label = 'ShowAllSemblocks', command = ShowAllSemblocks)    
##    
##
####    LL.TKDI['me'][3].add_separator()
##
##
##    LL.TKDI['me'][4] = TK.Menu(TKDI['me'][0])
##    LL.TKDI['me'][4].add_command(label = 'Insert__attr', command = Insert__attr)
##    LL.TKDI['me'][4].add_command(label = 'Counterframe ==>> attr', command = Counterframe__to__attr)
##    LL.TKDI['me'][4].add_command(label = 'Assign__domain', command = Assign__domain)
##    
##    LL.TKDI['me'][5] = TK.Menu(TKDI['me'][0])
##    LL.TKDI['me'][5].add_command(label = 'Insert__slot', command = Insert__slot)
##    LL.TKDI['me'][5].add_command(label = 'Clone__slot', command = Clone__cs)
##    LL.TKDI['me'][5].add_command(label = 'Rename__slot', command = Rename__slot)
##
##    
##    LL.TKDI['me'][5].add_command(label = 'Set current study (from slot)', command = Set__current__study__slot)
##    LL.TKDI['me'][5].add_command(label = 'Set current study (from attr_slot)', command = Set__current__study__attrslot)
##    LL.TKDI['me'][5].add_separator()
##    LL.TKDI['me'][5].add_command(label = 'Set_first_drug', command = Set_first_drug)
##    LL.TKDI['me'][5].add_command(label = 'Set_second_drug', command = Set_second_drug)
##    
##    
##
##    LL.TKDI['me'][7] = TK.Menu(TKDI['me'][0])
##    LL.TKDI['me'][7].add_command(label = 'Assign value', command = Assign__value)

    LL.TKDI['me'][8] = TK.Menu(TKDI['me'][0])
    LL.TKDI['me'][8].add_command(label = 'GetRefsi', command = GetRefsi)
    LL.TKDI['me'][8].add_command(label = 'ReadRefsiFromFile', command = ReadRefsiFromFile)  
    LL.TKDI['me'][8].add_command(label = 'RelevantSents', command = RelevantSents)
    LL.TKDI['me'][8].add_command(label = 'ShowCC', command = ShowCC)
##    LL.TKDI['me'][8].add_separator()
##    LL.TKDI['me'][8].add_command(label = 'BuildGraph', command = BuildGraph)

    
##    LL.TKDI['me'][8].add_command(label = 'LeftPassage', command = LeftPassage)
##    LL.TKDI['me'][8].add_command(label = 'RightPassage', command = RightPassage)
##    LL.TKDI['me'][8].add_command(label = 'CentralPassage', command = CentralPassage)    
    

    
    
##############################################################


##############################################################
    LL.TKDI['me'][0].add_cascade(label = 'Data', menu = TKDI['me'][2])
##    LL.TKDI['me'][0].add_cascade(label = 'Semblocks', menu = TKDI['me'][3])
##    LL.TKDI['me'][0].add_cascade(label = 'Attributes', menu = TKDI['me'][4])
##    LL.TKDI['me'][0].add_cascade(label = 'Slots', menu = TKDI['me'][5])
##    LL.TKDI['me'][0].add_cascade(label = 'Structure', menu = TKDI['me'][7])
    LL.TKDI['me'][0].add_cascade(label = 'Reference singles', menu = TKDI['me'][8])
    

def Create__forms():
    Add__frames()
    
    Add__entries()
    Add__lxx()
    Add__buttons()
    Add__txx()
    Add__canvas()
    Create__menu()



def StartLoads():

    pass

##    LoadSemblocks()
##    LoadAttrDI()
##    LoadFRAMES()
##    LoadCS()
##    LoadDomains()
 ##   fna = 'c:\\Il\\DATABASE\\Entry__Cl_Ov_exemestane.txt'
 ##   fna = 'C:\Il\Amorpha\CrohnDisease\AllCrohnArticles.txt'
   ## fna = ###'C:/Il/DATABASE/IB/099044_Aleglitazar_IB_Version_9_1_en.txt'
  ##  LL.TKDI['en']['attr_path'].insert(0, fna)
  ##  Read_text_file()

  ##  fna = 'C:/Il/Amorpha/CrohnDisease/FromUbuntu/TotalRefsi.txt'
  ##  LL.TKDI['en']['attr_path'].delete(0, LL.TK.END)
   ## LL.TKDI['en']['attr_path'].insert(0, fna)
    #GetRefsi()
    
#    ReadText()
                    

def Start():

    Create__forms()
    StartLoads()

    LL.TKDI['fr']['root'].mainloop()

Start()

