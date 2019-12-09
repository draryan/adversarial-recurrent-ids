#!/usr/bin/env python3

# An ad-hoc script for plotting tables copy-pasted from LibreOffice Calc

import fileinput
import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.transforms import Affine2D

group_names = []
values = []

plt.rcParams['font.family'] = 'serif'
plt.rcParams['savefig.format'] = 'pdf'
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for line in fileinput.input('-'):
	field = line.rstrip().split('\t')
	group_names.append(field[0])
	values.append(field[1:])

feature_names = values[0]
group_names = group_names[1:]
values = values[1:]

#  print (group_names)
#  print (values)
values = np.array(values, dtype=float)

def importance():
	global values
	plt.figure(figsize=(5,4))
	values[values < 0] = 0
	values /= np.sum(values,axis=0)

	width = 1/(1+values.shape[1])

	order = np.argsort(-np.mean(values, axis=1))
	x = np.arange(len(group_names))
	for i in range(values.shape[1]):
		plt.bar(x +width*(i-values.shape[1]/2), values[order,i], width, label=feature_names[i])
	plt.legend()
	plt.xticks(x, [group_names[i] for i in order], rotation=45, horizontalalignment='right')
	for tick in plt.gca().xaxis.get_major_ticks():
		label = tick.label1
		# don't know how to specify translation in axis coordinates, so pdf output
		# looks slightly different from plot
		label.set_transform(label.get_transform() + Affine2D().translate(5,0))
	plt.ylabel('Normalized metric')
	plt.tight_layout()
	
def adv_results():
	global values
	plt.figure(figsize=(5,4))
	values = np.reshape(values, (-1,values.shape[1]//2,2))

	order = np.argsort(np.mean(values[:,:,1], axis=1))
	width = 0.95 / values.shape[1]

	x = np.arange(len(group_names))
	for i in range(values.shape[1]):
		plt.bar(x +width*(i-values.shape[1]/2), values[order,i,1], width, color='gray', alpha=.5, **({'label': 'Original'} if i==0 else {}))
	for i in range(values.shape[1]):
		plt.bar(x +width*(i-values.shape[1]/2), values[order,i,0], width, color=colors[i], label=feature_names[i*2].rstrip(' adv'))
	plt.legend()
	plt.xticks(x, [group_names[i] for i in order], rotation=45, horizontalalignment='right')
	for tick in plt.gca().xaxis.get_major_ticks():
		label = tick.label1
		label.set_transform(label.get_transform() + Affine2D().translate(8,0))
	plt.ylabel('Accuracy')
	plt.tight_layout()

	
def ars():
	plt.figure(figsize=(5,2))
	plt.plot(group_names, values)
	plt.legend(feature_names, ncol=2)
	plt.xlabel('Training duration in epochs')
	plt.ylabel('ARS')
	ylim1,ylim2 = plt.ylim()
	plt.ylim((ylim1,ylim2+20)) # move plots away from legend
	plt.tight_layout()
	
globals()[sys.argv[1]]()
if len(sys.argv) > 2:
	plt.savefig(sys.argv[2], bbox_inches = 'tight', pad_inches = 0)
plt.show()
