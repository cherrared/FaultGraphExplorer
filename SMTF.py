from z3 import *
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
 Appbono1,Apphomestead,Appsprout1,Register21,Chomesteadcass,Appcass,ClusterEventE1,Register11,clusterCsprout1,DCbono1C,Cbono1sprout1,Csprout1homestead,DCE1C =Bools('Appbono1 Apphomestead Appsprout1 Register21 Chomesteadcass Appcass ClusterEventE1 Register11 clusterCsprout1 DCbono1C Cbono1sprout1 Csprout1homestead DCE1C')
 s=Solver()
 s.add(Register21==And(Apphomestead,Chomesteadcass,Appcass))
 s.add(Chomesteadcass==And(Apphomestead,Appcass))
 s.add(Register11==And(Appbono1,Apphomestead,Appsprout1,Chomesteadcass,Appcass,Csprout1homestead,Cbono1sprout1))
 s.add(Cbono1sprout1==And(Appbono1,Appsprout1,ClusterEventE1,clusterCsprout1,DCbono1C,DCE1C))
 s.add(Csprout1homestead==And(Apphomestead,Appsprout1,ClusterEventE1,clusterCsprout1))
 s.add(Cbono1sprout1== False)
 s.add(Register11== False)
 s.add(Register21== True)
 liste=[]
 valT={}
 valSF={}
 num_pred={}
 liste.append(Appbono1)
 valT[Appbono1]=1
 valSF[Appbono1]=0
 num_pred[Appbono1]=0
 liste.append(Apphomestead)
 valT[Apphomestead]=1
 valSF[Apphomestead]=0
 num_pred[Apphomestead]=0
 liste.append(Appsprout1)
 valT[Appsprout1]=1
 valSF[Appsprout1]=0
 num_pred[Appsprout1]=0
 liste.append(Chomesteadcass)
 valT[Chomesteadcass]=1
 valSF[Chomesteadcass]=0
 num_pred[Chomesteadcass]=2
 liste.append(Appcass)
 valT[Appcass]=1
 valSF[Appcass]=0
 num_pred[Appcass]=0
 liste.append(ClusterEventE1)
 valT[ClusterEventE1]=0
 valSF[ClusterEventE1]=0
 num_pred[ClusterEventE1]=0
 liste.append(clusterCsprout1)
 valT[clusterCsprout1]=0
 valSF[clusterCsprout1]=0
 num_pred[clusterCsprout1]=0
 liste.append(DCbono1C)
 valT[DCbono1C]=1
 valSF[DCbono1C]=1
 num_pred[DCbono1C]=0
 liste.append(Csprout1homestead)
 valT[Csprout1homestead]=1
 valSF[Csprout1homestead]=0
 num_pred[Csprout1homestead]=4
 liste.append(DCE1C)
 valT[DCE1C]=1
 valSF[DCE1C]=1
 num_pred[DCE1C]=0
 fi = open("Solutions.txt", "w")
 Sauve={}
 Sauve2={}
 save=[]
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
 t=sorted(Sauve.itervalues())
 i=0
 while i<len(t):
   Sauve[i]=t[i] 
   fi.write(str(i)+":"+str(t[i])+ " \n ")
   i=i+1
 for e in liste:
   if t[0][1][e] == False :
     if valT[e] == 1 :
        print("Please check the value of: ", e) 
        a=input() 
        if a== False:
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
        elif a== True: 
           ObsT.append(str(e)) 
           extend= False 
        elif a== None:  
             ObsN.append(str(e)) 
             extend= False 
     elif valT[e] == 0:  
       ObsN.append(str(e)) 
       extend= False 
 return(ObsT, ObsF, ObsN, liste, extend, stop)