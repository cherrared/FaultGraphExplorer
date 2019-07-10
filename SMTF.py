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
def SMTAlgo(ObsT, ObsF, ObsN): 
 CcassEM,Appbono1,DCEMS,Csprout1E1,AppE1,ClusterEventEM,Register11,clusterCsprout1,DCbono1C,DCEMC,Apphomestead,CE1EM,Appsprout1,Appcass,OV12,Csprout1homestead,DCE1S,ChomesteadEM,DCE1C,Chomesteadcass,ChomerEM,ClusterEventE1,AppEM,Cbono1sprout1,Cbono1E1 =Bools('CcassEM Appbono1 DCEMS Csprout1E1 AppE1 ClusterEventEM Register11 clusterCsprout1 DCbono1C DCEMC Apphomestead CE1EM Appsprout1 Appcass OV12 Csprout1homestead DCE1S ChomesteadEM DCE1C Chomesteadcass ChomerEM ClusterEventE1 AppEM Cbono1sprout1 Cbono1E1')
 s=Solver()
 s.add(CcassEM==And(DCEMC,AppEM,Appcass,ClusterEventEM))
 s.add(Csprout1E1==And(Appsprout1,clusterCsprout1,ClusterEventE1,AppE1,DCE1C))
 s.add(Register11==And(Appbono1,Apphomestead,Appsprout1,Chomesteadcass,Appcass,Csprout1homestead,Cbono1sprout1))
 s.add(CE1EM==And(AppEM,ClusterEventE1,ClusterEventEM,AppE1,OV12,DCEMC,DCE1C))
 s.add(Csprout1homestead==And(Apphomestead,Appsprout1,ClusterEventE1,ClusterEventEM,clusterCsprout1,OV12))
 s.add(ChomesteadEM==And(DCEMC,AppEM,Apphomestead,ClusterEventEM))
 s.add(Chomesteadcass==And(Apphomestead,Appcass,ClusterEventEM,DCEMC))
 s.add(ChomerEM==And(DCEMC,AppEM,ClusterEventEM))
 s.add(Cbono1sprout1==And(Appbono1,Appsprout1,ClusterEventE1,clusterCsprout1,DCbono1C,DCE1C))
 s.add(Cbono1E1==And(Appbono1,DCbono1C,ClusterEventE1,AppE1,DCE1C))
 s.add(Csprout1E1== False)
 s.add(Cbono1E1== False)
 s.add(CE1EM== False)
 s.add(AppE1== False)
 s.add(Register11== True)
 s.add(AppEM== True)
 liste=[]
 valT={}
 valSF={}
 liste.append(CcassEM)
 valT[CcassEM]=1
 valSF[CcassEM]=0
 liste.append(Appbono1)
 valT[Appbono1]=1
 valSF[Appbono1]=0
 liste.append(DCEMS)
 valT[DCEMS]=1
 valSF[DCEMS]=1
 liste.append(ClusterEventEM)
 valT[ClusterEventEM]=0
 valSF[ClusterEventEM]=0
 liste.append(clusterCsprout1)
 valT[clusterCsprout1]=0
 valSF[clusterCsprout1]=0
 liste.append(DCbono1C)
 valT[DCbono1C]=1
 valSF[DCbono1C]=1
 liste.append(ChomesteadEM)
 valT[ChomesteadEM]=1
 valSF[ChomesteadEM]=0
 liste.append(Apphomestead)
 valT[Apphomestead]=1
 valSF[Apphomestead]=0
 liste.append(Appsprout1)
 valT[Appsprout1]=1
 valSF[Appsprout1]=0
 liste.append(Appcass)
 valT[Appcass]=1
 valSF[Appcass]=0
 liste.append(OV12)
 valT[OV12]=0
 valSF[OV12]=0
 liste.append(DCEMC)
 valT[DCEMC]=1
 valSF[DCEMC]=1
 liste.append(DCE1S)
 valT[DCE1S]=1
 valSF[DCE1S]=1
 liste.append(Cbono1sprout1)
 valT[Cbono1sprout1]=1
 valSF[Cbono1sprout1]=0
 liste.append(DCE1C)
 valT[DCE1C]=1
 valSF[DCE1C]=1
 liste.append(Chomesteadcass)
 valT[Chomesteadcass]=1
 valSF[Chomesteadcass]=0
 liste.append(ChomerEM)
 valT[ChomerEM]=1
 valSF[ChomerEM]=0
 liste.append(ClusterEventE1)
 valT[ClusterEventE1]=0
 valSF[ClusterEventE1]=0
 liste.append(Csprout1homestead)
 valT[Csprout1homestead]=1
 valSF[Csprout1homestead]=0
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
             print(e, "  is the root cause")
             sys.exit(0)
           elif valSF[e]==2: 
             print(e, "  is the root cause, check the auto recovery node") 
             sys.exit(0)
           else:  ObsF.append(str(e)) 
        elif a== True: 
           ObsT.append(str(e)) 
     elif valT[e] == 0:  
       ObsN.append(str(e)) 
 return(ObsT, ObsF, ObsN, liste)