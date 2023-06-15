import numpy as np
from utils import data
import utils.sql as sql


mode = input("Выберите режим работы программы[xampp/pandas]: ")
if mode == "xampp":
    #starting mysql from xammp
    sql.start_sql()
    #material characteristics
    material = input("Введите название материала для его поиска в базе данных: ")
    material_chars = sql.find_material(material = material, mode = mode)
    if not material_chars:
        material_chars = data.ask_for_characteristics()
        if input("Для добавления материала в базу данных введите да").lower() in ['y','yes','да']:
            sql.insert_in_db(material, material_chars)
elif mode == "pandas":
    material = input("Введите название материала для его поиска в файле с данными с помощью pandas: ")
    material_chars = sql.find_material(material = material, mode = mode)
else:
    print("Некорректный ответ, перезапустите программу и попробуйте еще раз")

#ask for doping
print("Ответьте на вопросы о легировании материала (пример ответа: 3*10^(17))")
Nd = float(eval(input("Введите концентрацию доноров в материале: ").replace("^","**")))
Na = float(eval(input("Введите концентрацию акцепторов в материале: ").replace("^","**")))
#calculate all
print("Начинаем рассчеты...")
temp = [i for i in range(1, int(np.floor(material_chars['Tm']))+1)]
Nc, Nv, Eg, ni, n1, n2, n3, n4, n5, inv_temp, result_n = data.calculate_concentration(temp = temp, material_chars = material_chars, Nd = Nd, Na = Na)
if Nd > Na:
    Ec, Ev, Ed, F, Fi = data.calculate_Fermi(temp = temp, Nc = Nc, Nv = Nv, Eg = Eg, material_chars = material_chars, Nd = Nd, Na = Na, result_n = result_n, ni = ni)
    mobility_e, mobility_e_tkr, mobility_e_KV, mobility_p, mobility_p_tkr, mobility_p_KV, c_T_e, c_T_p = data.calculate_mobility(temp = temp, Nd = Nd, Na = Na, F = F, doping_level = Ed, material_chars = material_chars)
else:
    Ec, Ev, Ea, F, Fi = data.calculate_Fermi(temp = temp, Nc = Nc, Nv = Nv, Eg = Eg, material_chars = material_chars, Nd = Nd, Na = Na, result_n = result_n, ni = ni)
    mobility_e, mobility_e_tkr, mobility_e_KV, mobility_p, mobility_p_tkr, mobility_p_KV, c_T_e, c_T_p = data.calculate_mobility(temp = temp, Nd = Nd, Na = Na, F = F, doping_level = Ea, material_chars = material_chars)
conductivity = data.calculate_conductivity(temp = temp, result_n = result_n, ni = ni, mobility_e = mobility_e, mobility_p = mobility_p, Nd = Nd, Na = Na)


from utils import plots
plots.plot_concentration(inv_temp = inv_temp, result_n = result_n, n1 = n1, n2 = n2, n3 = n3, n4 = n4, n5 = n5, ni = ni)
plots.plot_Fermi(temp = temp, Ec = Ec, Ev = Ev, F = F, Fi = Fi, doping_level = Ed, mode = 'electron') if Nd > Na else plots.plot_Fermi(temp = temp, Ec = Ec, Ev = Ev, F = F, Fi = Fi, doping_level = Ea, mode = 'hole')
plots.plot_mobility(temp = temp, mobility = mobility_e, mobility_tkr = mobility_e_tkr, mobility_KV = mobility_e_KV, mode = "electron")
plots.plot_mobility(temp = temp, mobility = mobility_p, mobility_tkr = mobility_p_tkr, mobility_KV = mobility_p_KV, mode = "hole")
plots.plot_conductivity(inv_temp = inv_temp, conductivity = conductivity)
print("Изображения посчитанных зависимостей сохранены в папке results, можете закрывать окно командной строки")
input(" ")