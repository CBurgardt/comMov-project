from math import log10, log

def fsPathLoss(dist,freq):
    """
    dist : Kilometros
    freq : Megahertz
    """

    return 32.44 + 20*log10(dist) + 20*log10(freq)

def okumuraHataPL(dist, freq, cityKind, areaKind, hb, hm):
    """OKUMURA-HATA URBAN model
    freq: signal frequency(500Mhz e 1500Mhz);
    AreaKind: area type (1-rural, 2-suburban e 3-urban);
    cityKind : cyte type (1-small, 2-medium e 3-large);
    hb: base station's height;
    hm: mobile's height;
    """
    a = 0.0
    if (freq <= 200 and cityKind==3):
        # Large cities and f<=200 Mhz
        a = 8.29*(log10(1.54*hm))**2- 1.1
    elif (freq>=400 and cityKind==3):
        #Large cities and f>= 400 MHz
        a = 3.2*((log10(11.75*hm)**2))- 4.97
    else:
        #a(hm) for small and medium cities, and large cities where f<200Mhz and f>400Mhz
        a = (1.1*log10(freq-0.7))*hm - (1.56*log10(freq-0.8))
    # Path loos for urban area
    lossUrban = 69.55 + (26.16)*log10(freq)-13.82*log10(hb) - a + (44.9-6.55*log10(hb))*log10(dist)
    if (areaKind== 1):
        lossOpen= lossUrban - 4.78 *((log10(freq))**2)+18.33*log10(freq)-40.94
        return lossOpen
    elif (areaKind==2):
        #Loss for open are
        lossSubUrban =  lossUrban  - 2*(log10(freq/28.0))**2 - 5.4# //#Loss for suburban area
        return lossSubUrban
    return lossUrban
    
def flatEarthPL(dist,freq,hb,hm):
    L1 = -20*log10(hb)
    L2 = -20*log10(hm)
    Lo = 120 + 10*4*log10(dist)
    L = Lo + L1 + 2
    return L

def cost231PL(dist, freq, hb, hm, ws, bs, hr,cityKind):
    """
    COST 231- Cost-Waldrosch-Ikegami Model
    freq: signal frequency
    hb: base station's height
    hm: mobile's height
    ws: average width of the street in meters
    bs: average setback of buildings in meters
    hr: mean height of houses in meters
    areaKind: area type (1-rural, 2-suburban e 3-urban).
    cityKind : cyte type(1-small, 2-medium e 3-large).
    """
    deltaH = hm/hb
    Lbsh = 18*log(1+deltaH)
    Ka = 54.0   
    Kd = 18.0
    Kf = 4.0

    if(hr > hb):
        Lbsh = 0

    if(hb <= hr and d >= 0.5):
        Ka= Ka -0.8*deltaH
    
    elif(hb <= hr and d < 0.5):
        Ka = Ka -0.8*daltaH*(d/0.5)
    
    if(hb < hr):
        Kd = Kd - 15*(hb-hr)/(hr-hm)
    
    if(cityKind == 1):
        Kf = Kf +0.7*(freq/925-1)
    else:
        Kf = Kf +1.5*(freq/925-1)
    
    Lo = 32.4+20*log10(dist)+20*log10(freq)                     #free space path loss
    Lrts = 8.2+10*log(ws) + 10*log10(freq) + 10*log(deltaH) # roofTop loss
    Lmsd =Lbsh +Ka +Kd*log10(dist)+Kf*log(freq)-9*log10(bs)    #Multpath loss
    #final path loss
    PL = Lo + Lrts + Lmsd
    return PL

def costHataPL(dist, freq, hb, hm, cityKind, areaKind):
    """
    COST 231- Cost-Hata Extension Model
    freq: signal frequency
    hb: base station's height
    hm: mobile's height
    cityKind : cyte type(1-small, 2-medium e 3-large).
    areaKind : area type(1-open, 2-semiurban, 3- urban)
    """
    c = 0
    if areaKind==3:
        c = 3
    
    ar =(1.1*log10(freq)-0.7)*hm-(1.56*log(freq)-0.8) 
    return 46.3 +33.9*log10(freq)-13.82*log10(hb)-ar+(44.9-6.55*log(hb))*log(dist)+c

def ericssonPL(dist, freq, hb, hm, cityKind, areaKind):
    """Ericsson Model
    freq: signal frequency(range from 100 to 2000Mhz)
    tyArea: area type (1-rural, 2-suburban e 3-urban).
    cityKind : cyte type(1-small, 2-medium e 3-large).
    hb: base station's height
    hm: mobile's height
    """
    g = 44.49*log10(freq)-4.78*(log10(freq))**2
    a2= 12
    a3= 0.1

    if(cityKind == 3):
        a0 = 36.2
        a1 = 30.2
    elif(cityKind == 2):
        a0 = 43.2
        a1 = 68.9
    else:
        a0 = 45.9
        a1 = 100.6

    PL = a0+a1*log10(dist)+a2*log10(hb)+a3*(log10(hb))*(log10(dist))-3.2*log10((11.75*hm)**2)+g
    return PL

#print (fsPathLoss(1,1000))
#print (okumuraHataPL(1,1000,3,2,50,1.5))
#print (flatEarthPL(1,1000,50,1.5))
#print (cost231PL(1,1000,50,1.5,20,10,35,2))
#print (costHataPL(1,1000,50,1.5,2,2))
#print (ericssonPL(1,1000,50,1.5,2,2))