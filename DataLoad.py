import pickle as PI

AI = {}
FRAMES = {}

ParamsDI = {'dna':''}
LoadList = [
            ]


def ReadTextfile(fn):

    fna = ParamsDI['dna'] +'\\'+fn
    Name = fn.split('.')[0]
    fi = open(fna, 'r')
    rl = fi.readlines()
    fi.close()
    print Name, 'load: done'

    return rl
 

def LoadAllDI():

    if len(LoadList) == 0:
        print 'LoadList is empty!'
    else:
        for fna in LoadList:
            LoadDI(fna)
        

def LoadDI(fn):

    try:
        fna = ParamsDI['dna']+'\\'+fn
        fi = open(fna, 'rb')
        Name = fn.split('.')[0]
        AI[Name] = PI.load(fi)
        fi.close()
        print 'load', fn, ': done'
    except:
        print fn, 'NOT loaded!!!'


def DumpDI(fn):

    try:
        fna = ParamsDI['dna']+'\\'+fn+'.li'
        fi = open(fna, 'wb')
        
        PI.dump(AI[fn], fi)
        fi.close()
        
        print 'dump', fn, ': done'
    except:
        print fn, 'NOT dumped!!!'

