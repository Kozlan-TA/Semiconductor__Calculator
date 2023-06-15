import os
import mysql.connector
import pandas as pd

def start_sql():
    if os.path.exists("C:\\xampp"):
        os.startfile("C:\\xampp\\mysql\\bin\\mysqld.exe")
    else:
        print('xammp не найден в папке по умолчанию')
        xampp_path = input("Введите полный путь папки, в которую установлен xammp установлен(пример: C:\\xampp): ")
        if os.path.exists(xampp_path):
            os.system(xampp_path + "\\mysql\\bin\\mysqld.exe")
        else:
            print('xampp не найден"')
            print("Используется pandas")


def find_material(material, mode):
    if mode == "xampp":
        mydb = mysql.connector.connect(host = 'localhost', user = 'root', password ='', database = "semiconductors")
        select_query = "SELECT * FROM semiconductors WHERE material='" + material + "' ORDER BY material DESC"
        cursor = mydb.cursor()
        cursor.execute(select_query)
        if cursor != tuple():
            for i in cursor:
                result = {"material":i[0], "Eps":i[1], "mu_n":i[2], "mu_p":i[3], "mn":i[4], "mp":i[5], "mdn":i[6], "mdp":i[7], "Eg":i[8], "Tm":i[9], "Ea":i[10], "Ed":i[11]}
                return result
        else:
            print("Материал не найден, перезапустите программу в режиме 'pandas'")
        mydb.close()
    else:
        data = pd.read_csv("utils\\semiconductors.csv")
        raw_data = data[data["material"]==material].to_dict()
        _ = []
        for k, v in raw_data.items():
            for key, value in v.items():
                _.append(value)
        result = {"material":_[0], "Eps":_[1], "mu_n":_[2], "mu_p":_[3], "mn":_[4], "mp":_[5], "mdn":_[6], "mdp":_[7], "Eg":_[8], "Tm":_[9], "Ea":_[10], "Ed":_[11]}
        print(result)
        return result


def insert_in_db(material, material_chars):
    mydb = mysql.connector.connect(host = 'localhost', user = 'root', password ='', database = "semiconductors")
    insert_query = ("INSERT INTO semiconductors " + 
                        "(material, dielectric_const, mobility_n, mobility_p, effective_mass_n, effective_mass_p, dos_effective_mass_n, dos_effective_mass_p, Eg, melting_T, Ea, Ed)" +
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = [material] + [v for k, v in material_chars.items()]
    cursor = mydb.cursor()
    cursor.execute(insert_query, val)
    mydb.commit()
    print("Материал добавлен в базу данных")
    mydb.close()