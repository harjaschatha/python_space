import os
import pickle
cwd=os.getcwd()
def clean(i):
    s=i.strip('III').strip('II').strip('I')
    s=s.replace('YEAR','').replace('HONOURS','').replace('-SEC A','').replace('-SEC B','')
    s=s.replace(' ','').lower().replace('b.sc.','').replace('b.a.','')
    if 'prog.' in s:
        s=s.replace('prog.','B.Sc.Programme with ')
    return s
f=file(os.path.join(cwd,'paper_list'),'r')
d=pickle.load(f)
f.close()
nd={}
used=[]
for i in d:
    if clean(i) not in used:
        used.append(clean(i))
        nd[clean(i)]={}
        cnt=i.strip()[:5].count('I')
        nd[clean(i)][cnt]=d[i]
    else:
        cnt=i.strip()[:5].count('I')
        nd[clean(i)][cnt]=d[i]
f=file('paper_list_clean','w')
pickle.dump(nd,f)
f.close()

