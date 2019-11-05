import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import os
import cv2
import numpy.linalg as npla
from mpl_toolkits.mplot3d import Axes3D


def get_distance(point_1, point_2):
	return npla.norm(point_1 - point_2)

def get_vector(point_1, point_2):
	return point_1 - point_2

def begin(num_agents):
	agent_pos = np.random.uniform(low=0, high=grid_size-1, size=(N, 3))
	agent_vel = np.random.uniform(low=0, high=1, size=(N, 3))
	agent_vel = normalize(agent_vel)
	return agent_pos, agent_vel

def normalize(v):
	if (npla.norm(v) == 0):
		return v
	else:
		return v / npla.norm(v, 2)

def plot(pos, ang):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c='b')
	ax.set_zlim(-grid_size,4*grid_size)
	ax.set_xlim(-grid_size,4*grid_size)
	ax.set_ylim(-grid_size,4*grid_size)
	plt.savefig('./results/couzin_model/images/' + str(count) + '.png')
	plt.close()

def save(image_folder, video_name):
	images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
	frame = cv2.imread(os.path.join(image_folder, images[0]))
	height, width, layers = frame.shape
	
	video = cv2.VideoWriter(video_name, 0, 1, (width,height))

	for image in images:
	    video.write(cv2.imread(os.path.join(image_folder, image)))

	cv2.destroyAllWindows()
	video.release()


if (__name__ == '__main__'):
	# global variables
	N = 20
	tau = 0.1
	grid_size = 500
	rr = float(input('Enter Zone of repulsion : '))
	ro = float(input('Enter Zone of orientation : '))
	ra = float(input('Enter Zone of Attraction : '))
	s = 3
	theta = 50
	count = 0

	agent_positions, agent_velocities = begin(N)

	while (True):

		print (agent_positions)
		print (agent_velocities)
		print ('\n')

		agent_positions_temp = agent_positions.copy()
		agent_velocities_temp = agent_velocities.copy()

		for i in range(N): # for all agents

			pos_1 = agent_positions_temp[i]
			vel_1 = agent_velocities_temp[i]
			nr = []
			num_nr = False
			no = []
			na = []

			for j in range(N): # finding distance and bearing from all agents
				
				if (i != j):
					pos_2 = agent_positions_temp[j]
					vel_2 = agent_velocities_temp[j]	
					dis = get_distance(pos_1, pos_2)
					vec = get_vector(pos_1, pos_2)
					if (dis < rr):
						nr.append(vec)
						num_nr = True
					elif (dis > rr and dis < ro):
						no.append(vec)
					elif (dis > ro and dis < ra):
						na.append(vec)
			
			if(num_nr==True):
				nr = sum(nr)
				nr = np.asarray(nr)
				nr = normalize(nr)
				target_angle = nr
			
			else:
				num_na = len(na)
				num_no = len(no)
				no = sum(no)
				no = np.asarray(no)
				no = normalize(no)

				na = sum(na)
				na = np.asarray(na)
				na = normalize(na)

				if(num_na!=0 and num_no!=0):
					target_angle = 0.5 * (no + na)
				else:
					if(num_no!=0):
						target_angle = no
					else:
						target_angle = na

			agent_velocities_temp[i] += 2.5 * (target_angle - agent_velocities_temp[i]) / normalize(target_angle - agent_velocities_temp[i]) * tau
			agent_positions_temp[i] += s * agent_velocities_temp[i] * tau

		count += 1

		agent_positions = agent_positions_temp.copy()
		agent_velocities = agent_velocities_temp.copy()
		plot(agent_positions, agent_velocities)

		if (count == 15):
			save('./results/couzin_model/images/', './results/couzin_model/results/videos/video_swarms.avi')
			break



		