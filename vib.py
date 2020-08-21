import numpy as np
import copy as cp


asite2 = [1,1,1,1,0,0]
a_site = [1,1,1,1,0,0]
n_orb = len(a_site)


aindex = []
eindex = []
for i in range(0,n_orb):
    if a_site[i] == 1:
        aindex.append(i)
    elif a_site[i] == 0:
        eindex.append(i)
        

print(aindex)
print(eindex)

for j in aindex:
    for k in aindex:
        for l in eindex:
            for m in eindex: 
                if j < k and l < m :
                    asite2[j], asite2[l] = asite2[l], asite2[j]
                    asite2[k], asite2[m] = asite2[m], asite2[k]
                        
                    print(a_site,asite2)
                    
                    ###Fermionic anti-symmetry
		    sym = 0                                         
                    for i in range(min(j,l)+1, max(j,l)):             
                        if asite2[i] == 1:                          
                            sym += 1                                
                                                                    
                    Sphase1 = (-1)**sym                             
                                                                    
                    sym = 0                                         
                    for i in range(min(k,m)+1, max(k,m)):             
                        if asite2[i] == 1:                          
                            sym += 1                                
                    
		    Sphase2 = (-1)**sym                             
                                                                    
                    print(Sphase1*Sphase2)                          
                                                                    
                    asite2 = cp.deepcopy(a_site) #imp 

"""
for j in aindex:
    for k in eindex:
        asite2[j], asite2[k] = asite2[k], asite2[j]
            
        print(a_site,asite2)
        
        ###Fermionic anti-symmetry
        sym = 0
        for i in range(min(k,j)+1,max(k,j)):
            if a_site[i] == 1:
                sym += 1 
        
	Sphase1 = (-1)**sym
        
	asite2 = cp.deepcopy(a_site) #imp
"""
