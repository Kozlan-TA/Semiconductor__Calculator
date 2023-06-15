import math
import numpy as np


def ask_for_characteristics():
    print("Введите характеристики материала (разделителем целой и дробной части является точка)")
    dielectric_const = float(input("Введите диэлектрическую постоянную материала(пример 11.6): "))
    mobility_n = float(input("Введите подвижность электронов в см^2/(В*с): "))
    mobility_p = float(input("Введите подвижность дырок в см^2/(В*с): "))
    effective_mass_n = float(input("Введите эффективную массу электронов mn/m0 (пример 0.55): "))
    effective_mass_p = float(input("Введите эффективную массу дырок mp/m0 (пример 0.34): "))
    dos_effective_mass_n = float(input("Введите эффективную массу плотности состояний электронов mdn/m0 (пример 0.54): "))
    dos_effective_mass_p = float(input("Введите эффективную массу плотности состояний дырок mdp/m0 (пример 0.35): "))
    Eg = input("Введите температурную зависимость ширины запрещенной зоны (поддерживается и линейная аппроксимация и формула Варшни,пример 0.742-4.8*10^(-4)*T^(2)/(T+235)): ")
    melting_T = float("Введите температуру плавления")
    Ea = 13.52/pow(dielectric_const,2)*effective_mass_p
    Ed = 13.52/pow(dielectric_const,2)*effective_mass_n
    result = {"Eps":dielectric_const, "mu_n":mobility_n, "mu_p":mobility_p, "mn":effective_mass_n, "mp":effective_mass_p, "mdn":dos_effective_mass_n, "mdp":dos_effective_mass_p, "Tm":melting_T, "Eg":Eg, "Ea":Ea, "Ed":Ed}
    return result

def calculate_concentration(temp, material_chars, Nd, Na):
    Nc = []; Nv = []; Eg = []; ni = []; n1 = []; n2 =[]; n3 = []; n4 = []; n5 =[]; inv_temp = []
    for T in temp:
        inv_temp.append(1000/temp[T-1])
        Nc.append(4.83*10**15*pow(material_chars["mdn"]*T,3/2))
        Nv.append(4.83*10**15*pow(material_chars["mdp"]*T,3/2))
        Eg.append(eval((material_chars["Eg"].replace("^", "**")).replace("T", str(T))))
        ni.append((Nc[T-1]*Nv[T-1])**(1/2)*math.exp(-1*Eg[T-1]/(2*8.62*10**(-5)*T))) #концентрация собственных носителей заряда
        if Nd > Na:
            comp = Nd - Na
            n1.append(comp*Nc[T-1]*math.exp(-material_chars["Ed"]/(8.62*pow(10,-5)*T))/(2*Na)) #область компенсации примеси
            n2.append(pow((comp*Nc[T-1]/2),(1/2))*math.exp(-material_chars["Ed"]/((2*8.62*pow(10,-5))*T))) #область ионизации примеси
            try: #переходная область из области ионизации к области истощения примеси
                n3.append(2*comp/(1+(1+8*Nd/Nc[T-1]*math.exp(material_chars["Ed"]/(8.62*pow(10,-5)*T)))**(1/2)))
            except:
                n3.append(math.exp(-300))
            n4.append(comp) #область истощения примеси
            n5.append(comp/2*(1+pow((1+4*pow(ni[T-1],2)/(pow(comp, 2))),(1/2)))) #область перехода от истощения примеси к собственной проводимости
        else:
            comp = Na - Nd
            n1.append(comp*Nv[T-1]*math.exp(-material_chars["Ea"]/(8.62*pow(10,-5)*T))/(2*Nd)) #область компенсации примеси
            n2.append(pow((comp*Nv[T-1]/2),(1/2))*math.exp(-material_chars["Ea"]/(2*8.62*pow(10,-5)*T))) #область ионизации примеси
            try: #переходная область из области ионизации к области истощения примеси
                n3.append(2*comp/(1+pow((1+8*Na/Nv[T-1]*math.exp(material_chars["Ea"]/(8.62*pow(10,-5)*T))),(1/2))))
            except:
                n3.append(math.exp(-300))
            n4.append(comp) #область истощения примеси
            n5.append(comp/2*(1+pow((1+4*pow(ni[T-1],2)/(pow(comp, 2))),(1/2)))) #область перехода от истощения примеси к собственной проводимости
    result_n = [] #итоговая концентрация
    for i in range(len(temp)):
        first_zone = np.min([n1[i], n2[i], n3[i]])
        second_zone = np.max([ni[i], comp, n5[i]])
        if first_zone < 0.97 * comp:
            result_n.append(first_zone)
        else:
            result_n.append(second_zone)
    return Nc, Nv, Eg, ni, n1, n2, n3, n4, n5, inv_temp, result_n

def calculate_Fermi(temp, Nc, Nv, Eg, material_chars, Nd, Na, result_n, ni):
    Ec = []; Ev =[]; F = []; Fi =[]
    np.seterr(all = 'raise')
    if Nd < Na:
        Ea = []
        for i in range(len(temp)):
            Ec.append(Eg[i]/2)
            Ev.append(-Eg[i]/2)
            Ea.append(Ev[i] + material_chars["Ea"])
            try:
                F.append(Ev[i] - 8.62*pow(10, -5)*temp[i]*np.log(result_n[i] / Nv[i]))
            except:
                F.append(Ea[i])
            try:
                Fi.append(Ec[i] - 8.62*pow(10, -5)*temp[i]*np.log(Nc[i] / ni[i]))
            except:
                Fi.append(0.0)
        return Ec, Ev, Ea, F, Fi
    else:
        Ed = []
        for i in range(len(temp)):
            Ec.append(Eg[i]/2)
            Ev.append(-Eg[i]/2)
            Ed.append(Ec[i] - material_chars["Ed"])
            try:
                F.append(Ec[i] - 8.62*pow(10, -5)*temp[i]*np.log(Nc[i] / result_n[i]))
            except:
                F.append(Ed[i])
            try:
                Fi.append(8.62*pow(10, -5)/2*temp[i]*np.log(Nv[i] / Nc[i]))
            except:
                Fi.append(0.0)
        return Ec, Ev, Ed, F, Fi

def calculate_mobility(temp, Nd, Na, F, doping_level, material_chars):
    N_ion =[]; mobility_e_tkr = []; mobility_p_tkr = []; mobility_e_KV = []; mobility_p_KV = []; ln = []; mobility_e = []; mobility_p = []
    const_e = 8 * pow(2, 1/2) * pow(1.38*pow(10,-23), 3/2) * pow((material_chars["Eps"]*8.85*pow(10,-12)),2) / ((pow(math.pi,2)*pow(1.6*pow(10,-19),3)*pow(material_chars['mn']*9.1*pow(10,-31),1/2)))
    const_p = 8 * pow(2, 1/2) * pow(1.38*pow(10,-23), 3/2) * pow((material_chars["Eps"]*8.85*pow(10,-12)),2) / ((pow(math.pi,2)*pow(1.6*pow(10,-19),3)*pow(material_chars['mp']*9.1*pow(10,-31),1/2)))
    if Nd > Na:
        for i in range(len(temp)):
            N_ion.append(Na + Nd / (1+2*math.exp( (F[i] - doping_level[i]) / (8.62*pow(10,-5)*temp[i]) ) ) )
            mobility_e_tkr.append(material_chars["mu_n"] * pow(temp[i]/300, -3/2))
            mobility_p_tkr.append(material_chars["mu_p"] * pow(temp[i]/300, -3/2))
            ln.append(1 + pow((3*1.38*pow(10,-23)*8.85*pow(10,-12)*material_chars["Eps"]*temp[i])/(pow(N_ion[i],1/3)*pow(1.6*pow(10,-19),2)),2))
            mobility_e_KV.append(const_e*pow(temp[i],3/2)/(N_ion[i]*np.log(ln[i])))
            mobility_p_KV.append(const_p*pow(temp[i],3/2)/(N_ion[i]*np.log(ln[i])))
            mobility_e.append(1/(1/mobility_e_tkr[i]+1/mobility_e_KV[i]))
            mobility_p.append(1/(1/mobility_p_tkr[i]+1/mobility_p_KV[i]))
    else:
        for i in range(len(temp)):
            N_ion.append(Nd + Na / (1+2*math.exp( (doping_level[i]-F[i]) / (8.62*pow(10,-5)*temp[i]) ) ) )
            mobility_e_tkr.append(material_chars["mu_n"] * pow(temp[i]/300, -3/2))
            mobility_p_tkr.append(material_chars["mu_p"] * pow(temp[i]/300, -3/2))
            ln.append(1 + pow((3*1.38*pow(10,-23)*8.85*pow(10,-12)*material_chars["Eps"]*temp[i])/(pow(N_ion[i],1/3)*pow(1.6*pow(10,-19),2)),2))
            mobility_e_KV.append(const_e*pow(temp[i],3/2)/(N_ion[i]*np.log(ln[i])))
            mobility_p_KV.append(const_p*pow(temp[i],3/2)/(N_ion[i]*np.log(ln[i])))
            mobility_e.append(1/(1/mobility_e_tkr[i]+1/mobility_e_KV[i]))
            mobility_p.append(1/(1/mobility_p_tkr[i]+1/mobility_p_KV[i]))
    c_T_e = mobility_e.index(max(mobility_e)) + 1
    c_T_p = mobility_p.index(max(mobility_p)) + 1
    return mobility_e, mobility_e_tkr, mobility_e_KV, mobility_p, mobility_p_tkr, mobility_p_KV, c_T_e, c_T_p
                  
def calculate_conductivity(temp, result_n, ni, mobility_e, mobility_p, Nd, Na):
    conductivity = []; n = []
    if Nd > Na:
        for i in range(len(temp)):
            try:
                result = result_n[i] / ni[i]
                n.append(result if result < result_n[i] else 0.0)
            except:
                n.append(math.exp(-600))
            conductivity.append((result_n[i]*mobility_e[i] + n[i]*mobility_p[i])*1.6*pow(10,-19))
    else:
        for i in range(len(temp)):
            try:
                result = result_n[i] / ni[i]
                n.append(result if result < result[i] else 0.0)
            except:
                n.append(math.exp(-600))
            conductivity.append((result_n[i]*mobility_p[i] + n[i]*mobility_e[i])*1.6*pow(10,-19))
    return conductivity

