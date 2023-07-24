import os
from threading import Thread
import time #----------------------




def test(arg):
	print(f'Hello thread {arg}')

def suma_decena(base):
	for i in range(0,10):
		base = base + 1
		print(base)
		time.sleep(1)

def suma_centena(base):
	for i in range(0,10):
		base = base + 100
		print(base)
		time.sleep(0.5)


if __name__ == '__main__':
	hilos=[] #core list

	#capture list core 
	core=os.cpu_count()
	print(f'available core {core}')

	print('----------Begin')
	# Create Thread
	for n in range(core):
		hilo = Thread(target=test, args=(n,))
		hilos.append(hilo)
  
	print('---------Execute')
	for hilo in hilos:
		hilo.start()

	print('---------pause')
	for hilo in hilos:
		hilo.join()

	print('---------continue program flow')
	time.sleep(5)

	T1 = Thread(target=suma_decena, args=(0,))
	T1.start()

	T2 = Thread(target=suma_centena, args=(100,))
	T2.start()	


