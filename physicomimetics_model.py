import math
import random
import copy
import matplotlib.pyplot as plt

def ap(robots_distance, robots_bearing):
	# both are lists containing bearing and distance of robots of all robots wrt to one robot
	index = 0
	sum_fx = 0
	sum_fy = 0
	vx = 0 # full friction
	vy = 0

	for index in range(len(robots_bearing)): # For all neighbours do
		theta = robots_bearing[index]
		r = robots_distance[index]

		if (r > 1.5*R): # if robot is too far ignore it
			F = 0
		else:
			F = G / r*r
			if (F > F_max):
				F = F_max
			if (r < R):
				F = -F # repulsive force

		fx = F * math.cos(theta)
		fy = F * math.sin(theta)
		sum_fx += fx
		sum_fy += fy

	delta_vx = delta_T * sum_fx
	delta_vy = delta_T * sum_fy

	vx += delta_vx
	vy += delta_vy

	delta_x = delta_T * vx
	delta_y = delta_T * vy

	distance = int(math.sqrt(delta_vx*delta_vx + delta_vy*delta_vy))
	turn = int(math.atan2(delta_y, delta_x))
	# check if we require this
	if (delta_x < 0):
		turn += math.pi

	return distance, turn

def begin(num_agents):
	robot_pos = []
	robot_angle = []

	for i in range(num_agents):
		pos_x = random.randint(0, grid_size-1)
		pos_y = random.randint(0, grid_size-1)
		# can also do -pi to pi
		angle = random.uniform(-math.pi, math.pi)
		robot_pos.append([pos_x, pos_y])
		robot_angle.append(angle)

	return robot_pos, robot_angle

def get_distance(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_angle(pos1, pos2):
	return math.atan2((pos2[1] - pos1[1]), (pos2[0] - pos1[0]))

def plot(pos, ang):
	for i in range(len(pos)):
		plt.scatter(x=pos[i][0], y=pos[i][1])
	plt.show()

if (__name__ == '__main__'):
	# global variables
	R = 10
	G = 10
	F_max = 10
	delta_T = 1
	grid_size = 10
	n_agents = 4

	robot_positions, robot_angles = begin(n_agents)

	# print ('Positions = ')
	# print (robot_positions)
	# print ('Angles = ')
	# print (robot_angles)
	# print ('============================================')
	# print ('\n')
	plot(robot_positions, robot_angles)

	while (True):

		robot_positions_temp = []
		robot_angles_temp = []

		for i in range(n_agents): # for all agents
			pos_1 = robot_positions[i]
			angle_1 = robot_angles[i]
			
			distances = []
			bearings = []

			for j in range(n_agents): # finding distance and bearing from all agents
				if (i != j):
					pos_2 = robot_positions[j]
					angle_2 = robot_angles[j]
							
					dis = get_distance(pos_1, pos_2)
					ang = get_angle(pos_1, pos_2)

					distances.append(dis)
					bearings.append(ang)

			dis, turn = ap(distances, bearings)

			pos_1_new = copy.copy(pos_1)
			angle_1_new = copy.copy(angle_1)

			pos_1_new[0] += dis * math.cos(turn)
			pos_1_new[1] += dis * math.sin(turn)
			angle_1_new += turn

			robot_positions_temp.append(pos_1_new)
			robot_angles_temp.append(angle_1_new)

		robot_positions = robot_positions_temp
		robot_angles = robot_angles_temp

		plot(robot_positions, robot_angles)

		# print ('Positions = ')
		# print (robot_positions)
		# print ('Angles = ')
		# print (robot_angles)
		# print ('============================================')
		# print ('\n')















