#!/usr/bin/env python2
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, event,data
import os
import itertools
import numpy as np
_thisDir = os.path.dirname(os.path.abspath( __file__))
import csv
TRIAL_REPETITION = 24
response_left = ['a','A']
response_right = ['l','L']
RIGHT = 0
LEFT = 1
responses = response_right + response_left
LOG_HEADER = ['prime_side','prime_type','target_side','congruency','rt','accuracy','response']

def quit(log):
	log.close()
	core.quit()


def main():
	win = visual.Window((1000, 1000), allowGUI=False, color=1,
        monitor='testMonitor', winType='pyglet', units='norm' )

	breakText = visual.TextStim(win=win, text="Take a break\npress any key to continue",color=u'black')
	beginningText = visual.TextStim(win=win, text="The experiment will begin shortly",color=u'black')

 	#    text='+',    font=u'Arial',
 	#    pos=[0, 0], height=1, wrapWidth=None,
 	#    color=u'black', colorSpace='rgb', opacity=1,
 	#    depth=0.0)
	# `donut` has a true hole, using two loops of vertices:
	# fixation = visual.ShapeStim(win, vertices=donutVert, fillColor='orange', lineWidth=0, size=.75)
	fixation = visual.Circle(win=win, fillColor='grey', lineColor='grey', radius=0.1)
	arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
	rightArrow = visual.ShapeStim(win, vertices=arrowVert, fillColor='black', size=.5,pos=(0.1,0))
	arrowVert = [(0.4,-0.05),(0.4,0.05),(.2,0.05),(.2,0.1),(0,0),(.2,-0.1),(.2,-0.05)]
	leftArrow = visual.ShapeStim(win, vertices=arrowVert, fillColor='black', size=.5,pos=(-0.1,0))

 	image_LB = visual.ImageStim(win=win, image='hand_images/LB.bmp')
 	image_LP = visual.ImageStim(win=win, image='hand_images/LP.bmp')
 	image_RB = visual.ImageStim(win=win, image='hand_images/RB.bmp')
 	image_RP = visual.ImageStim(win=win, image='hand_images/RP.bmp')

 	images = [[image_RB, image_RP], [image_LB, image_LP]]
 	#TODO add neutral
 	arrows = [rightArrow, leftArrow]
 	conditionMatrix = np.zeros((2*2*2,4),dtype=int)
 	x =0
 	for i in xrange(len(images)):
 		for j in xrange(len(images[0])):
 			for k in xrange(len(arrows)):
 				congruency = i==k 
	 			conditionMatrix[x] = [i,j,k,congruency]
	 			x+=1
 	conditionMatrix = np.repeat(conditionMatrix, TRIAL_REPETITION, axis=0)
 	np.random.shuffle(conditionMatrix)

 	log = open(r'test-log.tsv','w')
 	writer = csv.writer(log,delimiter='\t')
 	writer.writerow(LOG_HEADER)
	trialClock = core.Clock()

 	"""
 	disc - 500 ms
	empty 1000 ms
	35 ms prime
	50 ms empty white screen
	70 ms arrow in disc
	blank until press or timeout at 1500ms after arrow offset
 	"""
 	beginningText.setAutoDraw(True)
 	win.flip()
 	core.wait(2)
 	beginningText.setAutoDraw(False)
 	beginningText.text
 	image_prime = None
 	arrow = None
 	rtClock = core.Clock()
 	trial_time = (500+1000+35+50+70+1500)/1000
 	for i,trial in enumerate(conditionMatrix):
	 	continueRoutine = True
		routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
	 	trialClock.reset()
	 	routineTimer.add(trial_time)
		#init trial
	 	drawn = False
	 	image = images[trial[0]][trial[1]]
		arrow = arrows[trial[2]]
		log_row = trial.tolist() + [None]*3
		event.clearEvents()
	 	while continueRoutine and routineTimer.getTime() > 0:
			t = trialClock.getTime()
			if t >= 0.0 and t < 0.5 and not drawn:
				fixation.setAutoDraw(True)
				drawn = True
			elif t >= 0.5 and t < 1.5 and drawn:
				fixation.setAutoDraw(False)
				drawn = False
			elif t >= 1.5 and t < 1.535 and not drawn:
	 			image.setAutoDraw(True)
	 			drawn = True
	 		elif t >= 1.535 and t<  1.585 and drawn:
				image.setAutoDraw(False)
				drawn = False
			elif t >= 1.585 and  t < 1.655 and not drawn:
	 			fixation.setAutoDraw(True)
	 			arrow.setAutoDraw(True)
	 			drawn = True
	 			rtClock.reset()
	 			event.clearEvents()
	 		elif t > 1.655:
	 			if drawn:
					fixation.setAutoDraw(False)
					arrow.setAutoDraw(False)
					drawn = False
				pressed = event.getKeys(keyList=responses)
				if pressed:
					rt = rtClock.getTime()*1000
					response = str.lower(pressed[0])
					if ((response in response_right and trial[2]==RIGHT) or 
					   (response in response_left and trial[2]==LEFT)):
					   accuracy = True
					else:
						accuracy = False
					log_row[4] = "%.4f" % rt
					log_row[5] = int(accuracy)
					log_row[6] = response
					continueRoutine = False
	 		win.flip()
			if event.getKeys(keyList=['escape','Q','q']):
				print "q"
				quit(log)
		print "{}: {}".format(i,log_row)
		writer.writerow(log_row)
		log.flush()
		if i%30 == 29:
 			event.clearEvents()
			breakText.setAutoDraw(True)
			win.flip()
			event.waitKeys()
			breakText.setAutoDraw(False)
			win.flip()
 	quit(log)

if __name__ == "__main__":
   main()
