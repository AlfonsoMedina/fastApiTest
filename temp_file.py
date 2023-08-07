import json
from os import remove
import os.path

new_item = [{"fileNbr":"2361426","tram_id":"26906","fecha":"2023-08-03T09:35:12","email":"xxx@gov.py","sigla":"REG"}]
path = './inProcess.txt'


def compile_data_list(param):
    total_list = []

    print(json.dumps(param))
    
    '''
    check_file = os.path.isfile(path)
    #Crea el fichero si no existe
    if check_file == False:
        with open("inProcess.txt","w") as file:
            file.write(param) # nuevos datos capturados
    
    #Lee el fichero ya que existe
    archi1=open("inProcess.txt","r")
    linea=archi1.readline()
    while linea!='':
        total_list.append(linea) # datos en el fichero existente
        linea=archi1.readline()
    archi1.close() 


    remove("inProcess.txt")

    total_list.append(str(param).replace("[","").replace("]",""))

    with open("inProcess.txt","w") as file:
        file.write(str(total_list)) '''


print(compile_data_list(new_item))















'''
#Create file with first data
with open("inProcess.txt","w") as file:
    file.write('[{"fileNbr":2361426,"tram_id":"26906","fecha":"2023-08-03T09:35:12","email":"xxx@gov.py","sigla":"REG"}]')


#File Read
archi1=open("inProcess.txt","r")
linea=archi1.readline()
while linea!='':
    print(linea.replace("[","").replace("]",""))
    linea=archi1.readline()
archi1.close()



#File Delete
remove("inProcess.txt")



#file Exist
check_file = os.path.isfile(path)
'''


