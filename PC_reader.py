
syn_dir = 'C:\\Il\\syntax'
fn = 'mono_preposition.txt'
fna = syn_dir + '\\'+fn 
fi = open(fna, 'r')
rl = fi.readlines()
fi.close()

fn = 'mono_conjunctions.txt'
fna = syn_dir + '\\'+fn 
fi = open(fna, 'r')
rl_2 = fi.readlines()
fi.close()


fn = 'modal_verbs.txt'
fna = syn_dir + '\\'+fn 
fi = open(fna, 'r')
rl_3 = fi.readlines()
fi.close()

##fn = 'ru_seps.txt'
##fna = syn_dir + '\\'+fn 
##fi = open(fna, 'r')
##rl_4 = fi.readlines()
##fi.close()
##

prepositions = [line.strip() for line in rl]
conjunctions = [line.strip() for line in rl_2]
modal_verbs = [line.strip() for line in rl_3]
#ru_seps = [line.strip().decode('cp1251').encode('utf-8') for line in rl_4]
points = [',', ';', ':', '(', ')', '[', ']', '/', '\\']
articles = ['a', 'the']

un_sl = prepositions\
        +conjunctions\
        +points\
        +articles
        


Pre_con_points = prepositions+conjunctions+points
##print sl
##print '=================================='
##print sl_2
##
##s1 = set(sl)
##s2 = set(sl_2)
##s3 = set(sl_3)
##
##PC = s1.union(s2, s3)
PC = set(un_sl)
seplist = list(PC)
seplist.sort()
ALL_SEPARATORS = seplist
print 'Total ', len(ALL_SEPARATORS), ' separators'
print 'Separators reading is done'
print ''
print '==================================================='
##for sep in ALL_SEPARATORS:
##    print sep
