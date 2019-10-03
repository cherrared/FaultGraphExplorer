from z3 import *
import six
def compte(m, liste):
 t=0
 for e in liste:
  if m[e]== False: t=t+1
 return(t)
def comp (s,m):
 b=0
 for e in s:
  if str(s[e])== str(m) :
    b=b+1
 return b 
def SMTAlgo(ObsT, ObsF, ObsN, extend, stop): 
 DCE1C,Appsprout1,DCbono1C,Appbono1,Apphomestead,ClusterEventE1,Csprout1homestead,Cbono1sprout1,Register21,Chomesteadcass,Register11,clusterCsprout1,Appcass =Bools('DCE1C Appsprout1 DCbono1C Appbono1 Apphomestead ClusterEventE1 Csprout1homestead Cbono1sprout1 Register21 Chomesteadcass Register11 clusterCsprout1 Appcass')
 s=Solver()
 s.add(Csprout1homestead==And(Appsprout1,Apphomestead,ClusterEventE1,clusterCsprout1))
 s.add(Cbono1sprout1==And(DCE1C,Appsprout1,DCbono1C,Appbono1,ClusterEventE1,clusterCsprout1))
 s.add(Register21==And(Appcass,Apphomestead,Chomesteadcass))
 s.add(Chomesteadcass==And(Appcass,Apphomestead))
 s.add(Register11==And(Appsprout1,Appcass,Appbono1,Apphomestead,Csprout1homestead,Cbono1sprout1,Chomesteadcass))
 s.add(Cbono1sprout1== False)
 s.add(Register11== False)
 s.add(Register21== True)
 s.add(DCbono1C== True)
 s.add(Appbono1== True)
 liste=[]
 valT={}
 valSF={}
 num_pred={}
 liste.append(DCE1C)
 valT[DCE1C]=1
 valSF[DCE1C]=1
 num_pred[DCE1C]=0
 liste.append(Appsprout1)
 valT[Appsprout1]=1
 valSF[Appsprout1]=0
 num_pred[Appsprout1]=0
 liste.append(Apphomestead)
 valT[Apphomestead]=1
 valSF[Apphomestead]=0
 num_pred[Apphomestead]=0
 liste.append(ClusterEventE1)
 valT[ClusterEventE1]=0
 valSF[ClusterEventE1]=0
 num_pred[ClusterEventE1]=0
 liste.append(Csprout1homestead)
 valT[Csprout1homestead]=1
 valSF[Csprout1homestead]=0
 num_pred[Csprout1homestead]=4
 liste.append(Chomesteadcass)
 valT[Chomesteadcass]=1
 valSF[Chomesteadcass]=0
 num_pred[Chomesteadcass]=2
 liste.append(clusterCsprout1)
 valT[clusterCsprout1]=0
 valSF[clusterCsprout1]=0
 num_pred[clusterCsprout1]=0
 liste.append(Appcass)
 valT[Appcass]=1
 valSF[Appcass]=0
 num_pred[Appcass]=0
 fi = open("Solutions.txt", "w")
 Sauve={}
 Sauve2={}
 save=[]
 t=[]
 i=1
 s.check() 
 c=compte(s.model(),liste)
 Sauve[0]= (c,s.model())
 Sauve2[0]= s.model()
 while s.check() == sat:
  j=0
  while j < len(liste):
   if ((s.check() == sat) and (comp(Sauve2, s.model())==0)): 
     c=compte(s.model(),liste)
     Sauve[i]= (c,s.model())
     Sauve2[i]= s.model()
     i=i+1
   if (s.check()== sat): save= s.model()
   if (save[liste[j]] == False):
    s.add(And(liste[j] == True))
   j=j+1
 k=0 
 while k<i-1:
   t.append(Sauve[k]) 
   k=k+1
 k=0
 t.sort(key=lambda x:x[0])
 while k<i-1:
   fi.write(str(k)+":"+str(t[k])+ " \n ")
   k=k+1
 for e in liste:
   if t[0][1][e] == False :
     if valT[e] == 1 :
        print("Please check the value of: ", e) 
        a=input() 
        if a == 'False':
           if valSF[e]== 1: 
            if num_pred[e]== 0: 
             print(e, "  is the root cause")
             stop= True
             ObsF.append(str(e))
            else:
             print(e, "  Possible root cause? Yes/No")
             answer= input()
             if answer=="Yes": 
               print(e, "  is the root cause")
               stop= True
               ObsF.append(str(e))
             else:  ObsF.append(str(e)) 
           elif valSF[e]==2: 
            if num_pred[e]== 0: 
             print(e, "  is the root cause")
             stop=True
             ObsF.append(str(e))
            else:
             print(e, "  Possible root cause with auto_recovery node? Yes/No")
             answer= input()
             if answer=="Yes": 
               print(e, "  is the root cause , check the auto recovery node")
               stop=True
               ObsF.append(str(e))
           else:  ObsF.append(str(e)) 
        elif a == 'True': 
           ObsT.append(str(e)) 
           extend= False 
        elif a == 'None':  
             ObsN.append(str(e)) 
             extend= False 
     elif valT[e] == 0:  
       ObsN.append(str(e)) 
       extend= False 
 return(ObsT, ObsF, ObsN, liste, extend, stop)