import random
import matplotlib.pyplot as plt
import math
import numpy as np
import cv2 
import os

def distance(x0, y0, x1, y1):
	return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

def find_n_nearest(agent_idx, agent_pos, n_nearest):
	dis = []
	for i in range(num_agents):
		if (i != agent_idx):
			d = distance(agent_pos[agent_idx][0], agent_pos[agent_idx][1], agent_pos[i][0], agent_pos[i][1])
			dis.append(d)
	dis = np.asarray(dis)
	n_nearest_agents_idx = np.argsort(dis)[:n_nearest]
	return n_nearest_agents_idx

def find_lcm(agents_idx, agent_pos, n_nearest):
	x = 0
	y = 0
	for i in range(agents_idx.shape[0]):
		x += agent_pos[agents_idx[i]][0]
		y += agent_pos[agents_idx[i]][1]
	return [x/n_nearest, y/n_nearest]

def find_gcm(agent_pos):
	x = 0
	y = 0
	for i in range(num_agents):
		x += agent_pos[i][0]
		y += agent_pos[i][1]
	return [x/len(agent_pos), y/len(agent_pos)]	

def initialise_agents():
	agent_pos = []
	for i in range(num_agents):
		x = random.randint(0, grid_size-1)
		y = random.randint(0, grid_size-1)
		agent_pos.append([x, y])
	return agent_pos

def initialise_shepherd():
	#return [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
	return [130, 130]

def initialise_agent_velocities():
	vel = []
	for i in range(num_agents):
		vel.append([0, 0])
	return vel

def initialise_shepherd_velocity():
	return [0, 0]

def initialise_target_location():
	return [0, 0]

def normalize(vec):
	if (vec == [0, 0]):
		return vec
	else:
		norm = distance(vec[0], vec[1], 0, 0)
		return [vec[0]/norm, vec[1]/norm]

def plot(a_p, s_p):
	for i in range(len(a_p)):
		plt.scatter(x=a_p[i][0], y=a_p[i][1], c='r')
	plt.scatter(x=s_p[0], y=s_p[1])
	plt.xlim(-10, 160)
	plt.ylim(-10, 160)
	sc = str(count)
	if (len(sc) == 1):
		sc = '00' + sc
	elif (len(sc) == 2):
		sc = '0' + sc
	plt.savefig('./results/shepherding_model/img/' + sc + '.png')
	plt.close()

if (__name__ == '__main__'):
	num_agents = 100
	grid_size = 150
	n = 30
	rs = 65
	ra = 2
	c = 1.05
	rho_a = 2
	rho_s = 1
	m = 0.5
	shepherd_speed = 1
	num_steps = 300
	tau = 0.1

	agent_positions = initialise_agents()
	print ('Agent Positions = ', agent_positions)
	agent_velocities = initialise_agent_velocities()

	shepherd_position = initialise_shepherd()
	print ('Shepherd Position = ', shepherd_position)
	shepherd_velocity = initialise_shepherd_velocity()

	target_location = initialise_target_location()

	count = 0
	while True:

		#print ('Agent Positions: ', agent_positions)
		#print ('Agent Velocities: ', agent_velocities)
		print (count)
		print ('Shepherd Position: ', shepherd_position)
		print ('Shepherd Velocity: ', shepherd_velocity)
		print ('\n')

		agent_positions_temp = []
		agent_velocities_temp = []
		shepherd_position_temp = []
		shepherd_velocity_temp = []

		## Compute agent movements
		for current_agent in range(num_agents):

			n_nearest_neighbours = find_n_nearest(current_agent, agent_positions, n)
			neighbourhood_com = find_lcm(n_nearest_neighbours, agent_positions, n)
			C_cap = [neighbourhood_com[0] - agent_positions[current_agent][0], neighbourhood_com[1] - agent_positions[current_agent][1]]
			C_cap = normalize(C_cap)
			
			shepherd_distance = distance(shepherd_position[0], shepherd_position[1], agent_positions[current_agent][0], agent_positions[current_agent][1])
			if (shepherd_distance < rs):
				Rs = [agent_positions[current_agent][0] - shepherd_position[0], agent_positions[current_agent][1] - shepherd_position[1]]
				Rs = normalize(Rs)
			else:
				Rs = [0, 0]

			Ra = [0, 0]
			for j in range(num_agents):
				if (j != current_agent):
					d = distance(agent_positions[current_agent][0], agent_positions[current_agent][1], agent_positions[j][0], agent_positions[j][1])
					if (d < ra):
						Ra[0] += agent_positions[current_agent][0] - agent_positions[j][0]
						Ra[1] += agent_positions[current_agent][1] - agent_positions[j][1]
			Ra = normalize(Ra)

			F = [c*C_cap[0] + rho_s*Rs[0] + rho_a*Ra[0], c*C_cap[1] + rho_s*Rs[1] + rho_a*Ra[1]]
			a = [F[0] / m, F[1] / m]
			agent_velocities_temp.append([agent_velocities[current_agent][0] + tau * a[0], agent_velocities[current_agent][1] + tau * a[1]])
			s = [agent_velocities[current_agent][0] * tau + 0.5*a[0]*tau*tau, agent_velocities[current_agent][1] * tau + 0.5*a[1]*tau*tau]

			agent_newpos = [agent_positions[current_agent][0] + s[0], agent_positions[current_agent][1] + s[1]]
			if (agent_newpos[0] > grid_size):
				agent_newpos[0] = grid_size
			elif (agent_newpos[0] < 0):
				agent_newpos[0] = 0
			if (agent_newpos[1] > grid_size):
				agent_newpos[1] = grid_size
			elif (agent_newpos[1] < 0):
				agent_newpos[1] = 0

			agent_positions_temp.append(agent_newpos)

		## Decide shepherd action
		dis_from_agents = 0
		for agent in range(num_agents):
			d = distance(shepherd_position[0], shepherd_position[1], agent_positions[agent][0], agent_positions[agent][1])
			dis_from_agents = max(dis_from_agents, d)
		if (dis_from_agents < 3 * ra):
			shepherd_velocity_temp = [0, 0]
		else:
			gcom = find_gcm(agent_positions)
			dis_from_gcom = 0
			agent_farthest_from_gcom = 0
			for a in range(num_agents):
				d = distance(gcom[0], gcom[1], agent_positions[a][0], agent_positions[a][1])
				if (d > dis_from_gcom):
					dis_from_gcom = d
					agent_farthest_from_gcom = a
			
			f_n = ra * math.pow(num_agents, 2/3)
			if (dis_from_gcom < f_n):
				Pd = [gcom[0] + 0.5*(gcom[0] - target_location[0]), gcom[1] + 0.5*(gcom[1] - target_location[1])]
				shepherd_velocity_temp = [Pd[0] - shepherd_position[0], Pd[1] - shepherd_position[1]]
				shepherd_velocity_temp = shepherd_speed * normalize(shepherd_velocity_temp)
			else:
				Pc = [agent_positions[agent_farthest_from_gcom][0] + 0.1*(agent_positions[agent_farthest_from_gcom][0] - gcom[0]), agent_positions[agent_farthest_from_gcom][1] + 0.1*(agent_positions[agent_farthest_from_gcom][1] - gcom[1])]
				shepherd_velocity_temp = [Pc[0] - shepherd_position[0], Pc[1] - shepherd_position[1]]
				shepherd_velocity_temp = shepherd_speed * normalize(shepherd_velocity_temp)

		shepherd_position_temp = [shepherd_velocity_temp[0]*tau + shepherd_position[0], shepherd_velocity_temp[1]*tau + shepherd_position[1]]

		agent_positions = agent_positions_temp
		agent_velocities = agent_velocities_temp
		shepherd_position = shepherd_position_temp
		shepherd_velocity = shepherd_velocity_temp

		plot(agent_positions, shepherd_position)

		count += 1

		if (count == num_steps):
			break







