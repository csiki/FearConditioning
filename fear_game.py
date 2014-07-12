import threading
import time
import pygame as pg
from math import isnan
from basal_amygdala import *

# global variables
fear_rate = 0.0
cs_presented = False
us_presented = False
screen = None
sim_thread = None
io_thread = None
run_threads = True
happy_img = None
freezed_img = None
neutral_img = None
flute_img = None
shock_img = None
emo = 0

def stop_program():
	global run_threads
	pg.display.quit()
	run_threads = False

def sim_process():
	"""
	Specifies the thread process on which the simulation runs.
	"""
	global fear_rate, cs_presented, us_presented, screen, emo
	
	# amygdala init
	amygdala = BasalAmygdala(800, 160)
	ctx_ext = amygdala.create_context('extinction')
	ctx_fear = amygdala.create_context('fear')
	stim_ext = amygdala.create_cs(ctx_ext.associated_neurons)
	stim_fear = amygdala.create_cs(ctx_fear.associated_neurons)
	poprate_exc = PopulationRateMonitor(ctx_fear.associated_neurons, bin=100*ms)
	poprate_inh = PopulationRateMonitor(ctx_ext.associated_neurons, bin=100*ms)
	amygdala.network.add(poprate_exc, poprate_inh)
	
	# simulation loop
	amygdala.switch_context(ctx_ext)
	while( run_threads ):
		print cs_presented, us_presented
		if cs_presented and us_presented:
			amygdala.switch_context(ctx_fear) # fear conditioning
			amygdala.present_stimulus(stim_fear, stim_ext)
			amygdala.run(100*ms)
			emo = 2 # freezed
			
			# fear rate calc TODO
			fear_rate = mean(poprate_exc.rate[-10:-1])
			if isnan(fear_rate):
				fear_rate = 1.0
			print fear_rate
			if fear_rate > 2.0:
				print 'NOW START EXTINCTION!'
			
		elif cs_presented:
			amygdala.switch_context(ctx_ext) # fear extinction
			amygdala.present_stimulus(stim_ext, stim_fear)
			amygdala.run(100*ms)
			# fear rate calc
			fear_rate = mean(poprate_exc.rate[-10:-1])
			if isnan(fear_rate):
				fear_rate = 1.0
			print fear_rate
			# emo calc
			emo = 1 # happy default
			if fear_rate > 2.0:
				emo = 2 # freeze
			elif fear_rate >= 1.0:
				emo = 0 # neutral
		elif us_presented:
			emo = 2 # freeze
		else:
			emo = 0
			#~ amygdala.switch_context(ctx_ext) # nothing happens
			#~ amygdala.run(100*ms)
		cs_presented = False
		us_presented = False

		time.sleep(2)
		

def io_process():
	"""
	Specifies the thread process which handles the drawing and io operations.
	"""
	global fear_rate, cs_presented, us_presented, screen, \
		happy_img, freezed_img, neutral_img, flute_img, shock_img, emo
	
	emo_pics = [neutral_img, happy_img, freezed_img]
	while( run_threads ):
		screen.fill((255,255,255))
		screen.blit(emo_pics[emo],(100,20))
		
		events = pg.event.get()
		for event in events:
			if event.type == pg.KEYDOWN and event.key == pg.K_c:
				cs_presented = True
				screen.blit(flute_img,(300,100))
			elif event.type == pg.KEYDOWN and event.key == pg.K_u:
				us_presented = True
				screen.blit(shock_img,(450,100))
			elif event.type == pg.KEYDOWN and event.key == pg.K_q:
				stop_program()

		pg.display.flip()
		time.sleep(2)

if __name__ == '__main__':
	
	seed(1000)
	
	# screen init
	pg.init()
	screen = pg.display.set_mode((640, 480))
	screen.fill((255,255,255))
	# images
	happy_img = pg.image.load('happy.png').convert()
	freezed_img = pg.image.load('freezed.gif').convert()
	neutral_img = pg.image.load('neutral.png').convert()
	flute_img = pg.image.load('flute.gif').convert()
	shock_img = pg.image.load('shock.jpg').convert()
	# transform
	happy_img = pg.transform.scale(happy_img, (500,428))
	freezed_img = pg.transform.scale(freezed_img, (320,450))
	neutral_img = pg.transform.scale(neutral_img, (378,450))
	flute_img = pg.transform.scale(flute_img, (150,113))
	shock_img = pg.transform.scale(shock_img, (150,150))
	
	# threads
	sim_thread = threading.Thread(target=sim_process)
	io_thread  = threading.Thread(target=io_process)
	
	try:
		sim_thread.start()
		io_thread.start()
		sim_thread.join()
		io_thread.join()
	except:
		sim_thread.stop()
		io_thread.stop()
		pg.display.quit()
