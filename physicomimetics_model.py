import math
import random
import copy
import matplotlib.pyplot as plt

def begin(num_agents):
	robot_pos = []
	robot_vel = []

	for i in range(num_agents):
		pos_x = random.uniform(0, grid_size-1)
		pos_y = random.uniform(0, grid_size-1)

		vel_x = random.uniform(0, grid_size-1)
		vel_y = random.uniform(0, grid_size-1)
		vel = [vel_x, vel_y]
		if (get_norm(vel) >= v_max):
			vel = v_max * normalize(vel)

		robot_pos.append([pos_x, pos_y])
		robot_vel.append(vel)

	return robot_pos, robot_vel

def get_distance(pos1, pos2):
	return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_angle(pos1, pos2):
	return math.atan2((pos2[1] - pos1[1]), (pos2[0] - pos1[0]))

def get_norm(vec):
	norm = get_distance(vec, [0, 0])
	return norm

def normalize(vec):
	if (vec == [0, 0]):
		return vec
	else:
		norm = get_distance(vec, [0, 0])
		return [vec[0]/norm, vec[1]/norm]

def plot(pos):
	for i in range(len(pos)):
		plt.scatter(x=pos[i][0], y=pos[i][1], c='r')
	plt.xlim(-60, 60)
	plt.ylim(-60, 60)
	sc = str(count)
	if (len(sc) == 1):
		sc = '00' + sc
	elif (len(sc) == 2):
		sc = '0' + sc
	plt.savefig('./results/physicomimetics_model/without_target/img/' + sc + '.jpg')
	plt.close()

if (__name__ == '__main__'):
	R = 23
	G = 270
	F_max = 1
	m = 1
	delta_T = 0.1
	grid_size = 20
	n_agents = 20
	v_max = 2
	target = False
	target_force = 0.25
	target_pos = [0, 0]
	
	count = 0

	robot_positions, robot_vel = begin(n_agents)

	while (True):

		plot(robot_positions)

		robot_positions_temp = robot_positions.copy()
		robot_vel_temp = robot_vel.copy()

		for i in range(n_agents): # for all agents
			F_total = [0, 0]
			for j in range(n_agents):
				if (i != j):
					d = get_distance(robot_positions[i], robot_positions[j])
					F = [robot_positions[j][0] - robot_positions[i][0], robot_positions[j][1] - robot_positions[i][1]]
					F = normalize(F)
					F_mag = G / (d*d)
					if (F_mag > F_max):
						F_mag = F_max
					F = [F[0] * F_mag, F[1] * F_mag]
					if (d < R):
						F = [-F[0], -F[1]]
					if (d > 1.5*R):
						F = [0, 0]
					F_total = [F_total[0] + F[0], F_total[1] + F[1]]
					print (F_total)
					if (target):
						force_due_to_target = [target_pos[0] - robot_positions_temp[i][0], target_pos[1] - robot_positions_temp[i][1]]
						force_due_to_target = normalize(force_due_to_target)
						force_due_to_target = [target_force * force_due_to_target[0], target_force * force_due_to_target[1]]
						F_total = [F_total[0] + force_due_to_target[0], F_total[1] + force_due_to_target[1]]
			a = [F_total[0] / m, F_total[1] / m]
			s = [robot_vel_temp[i][0]*delta_T + 0.5*a[0]*delta_T*delta_T, robot_vel[i][1]*delta_T + 0.5*a[1]*delta_T*delta_T]
			robot_vel_temp[i] = [robot_vel_temp[i][0] + a[0]*delta_T, robot_vel_temp[i][1] + a[1]*delta_T] 
			if (get_norm(robot_vel_temp[i]) > v_max):
				robot_vel_temp[i] = v_max * normalize(robot_vel_temp[i])
			robot_positions_temp[i] = [robot_positions_temp[i][0] + s[0], robot_positions_temp[i][1] + s[1]]

		count += 1

		robot_positions = robot_positions_temp.copy()
		robot_vel = robot_vel_temp.copy()

		if (count == 300):
			break



				


