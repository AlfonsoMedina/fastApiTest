import shutil






def copy_file(origen:str,destino:str):
    shutil.copy2(origen, destino)

def copy_file2(file:str,destino:str):
    file_src = file  
    f_src = open(file_src, 'rb')
    file_dest = destino  
    f_dest = open(file_dest, 'wb')
    shutil.copyfileobj(f_src, f_dest)

#copy_file('//SP10//Users//agray//Documents//CV Rossana 2022 Part. 2.pdf', './')

copy_file2('//SP10//Users//agray//Pictures//16452001455521.jpg','//192.168.50.183//mea//escritos')


#//192.168.50.183//mea//escritos