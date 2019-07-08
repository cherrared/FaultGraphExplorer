from z3 import *


def compte(m, liste):
    t = 0
    for e in liste:
        if m[e] == False: t = t + 1
    return (t)


def comp(s, m):
    b = 0
    for e in s:
        if str(s[e]) == str(m):
            b = b + 1
    return b


def SMTAlgo(ObsT, ObsF):
    Appbono2, Appbono1, Apphomestead, Appsprout1, Register21, Chomesteadcass, Appcass, AppE1, Csprout2homestead, Register11, clusterCsprout1, DCbono1C, Cbono1sprout1, Csprout1homestead, Cbono2sprout2, DCE1C, Appsprout2 = Bools(
        'Appbono2 Appbono1 Apphomestead Appsprout1 Register21 Chomesteadcass Appcass AppE1 Csprout2homestead Register11 clusterCsprout1 DCbono1C Cbono1sprout1 Csprout1homestead Cbono2sprout2 DCE1C Appsprout2'
    )
    s = Solver()
    s.add(
        Register21 == And(Appbono2, Apphomestead, Csprout2homestead,
                          Appsprout2, Chomesteadcass, Appcass, Cbono2sprout2))
    s.add(Chomesteadcass == And(Apphomestead, Appcass))
    s.add(Csprout2homestead == And(Apphomestead, Appsprout2))
    s.add(Register11 == And(Appbono1, Apphomestead, Appsprout1, Chomesteadcass,
                            Appcass, Csprout1homestead, Cbono1sprout1))
    s.add(Cbono1sprout1 == And(Appbono1, Appsprout1, AppE1, clusterCsprout1,
                               DCbono1C, DCE1C))
    s.add(Csprout1homestead == And(Apphomestead, Appsprout1, AppE1,
                                   clusterCsprout1))
    s.add(Cbono2sprout2 == And(Appbono2, Appsprout2))
    s.add(Cbono1sprout1 == False)
    s.add(Register11 == False)
    s.add(Register21 == True)
    liste = []
    valT = {}
    valSF = {}
    liste.append(Appbono2)
    valT[Appbono2] = 0
    valSF[Appbono2] = 0
    liste.append(Appbono1)
    valT[Appbono1] = 0
    valSF[Appbono1] = 0
    liste.append(DCbono1C)
    valT[DCbono1C] = 1
    valSF[DCbono1C] = 1
    liste.append(Apphomestead)
    valT[Apphomestead] = 0
    valSF[Apphomestead] = 0
    liste.append(Appsprout1)
    valT[Appsprout1] = 0
    valSF[Appsprout1] = 0
    liste.append(Chomesteadcass)
    valT[Chomesteadcass] = 1
    valSF[Chomesteadcass] = 0
    liste.append(Appcass)
    valT[Appcass] = 0
    valSF[Appcass] = 0
    liste.append(AppE1)
    valT[AppE1] = 0
    valSF[AppE1] = 0
    liste.append(clusterCsprout1)
    valT[clusterCsprout1] = 0
    valSF[clusterCsprout1] = 0
    liste.append(Csprout2homestead)
    valT[Csprout2homestead] = 1
    valSF[Csprout2homestead] = 0
    liste.append(Csprout1homestead)
    valT[Csprout1homestead] = 1
    valSF[Csprout1homestead] = 0
    liste.append(Cbono2sprout2)
    valT[Cbono2sprout2] = 1
    valSF[Cbono2sprout2] = 0
    liste.append(DCE1C)
    valT[DCE1C] = 1
    valSF[DCE1C] = 1
    liste.append(Appsprout2)
    valT[Appsprout2] = 0
    valSF[Appsprout2] = 0
    fi = open("Solutions.txt", "w")
    Sauve = {}
    Sauve2 = {}
    save = []
    i = 1
    s.check()
    c = compte(s.model(), liste)
    Sauve[0] = (c, s.model())
    Sauve2[0] = s.model()
    while s.check() == sat:
        j = 0
        while j < len(liste):
            if ((s.check() == sat) and (comp(Sauve2, s.model()) == 0)):
                c = compte(s.model(), liste)
                Sauve[i] = (c, s.model())
                Sauve2[i] = s.model()
                i = i + 1
            if (s.check() == sat): save = s.model()
            if (save[liste[j]] == False):
                s.add(And(liste[j] == True))
            j = j + 1
    t = sorted(Sauve.itervalues())
    i = 0
    while i < len(t):
        Sauve[i] = t[i]
        fi.write(str(i) + ":" + str(t[i]) + " \n ")
        i = i + 1
    for e in liste:
        if t[0][1][e] == False:
            if valT[e] == 1:
                print("Please check the value of: ", e)
                a = input()
                if a == False:
                    if valSF[e] == 1:
                        print(e, "  is the root cause")
                        sys.exit(0)
                    elif valSF[e] == 2:
                        print(
                            e,
                            "  is the root cause, check the auto recovery node"
                        )
                        sys.exit(0)
                    else:
                        ObsF.append(str(e))
                elif a == True:
                    ObsT.append(str(e))
            elif valT[e] == 0:
                ObsF.append(str(e))
    return (ObsT, ObsF)
