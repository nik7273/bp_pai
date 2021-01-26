import numpy as np 
import planning_utils as pu

class Action:
	def __init__(self, name, obj, constraints=[], params=[]):
		self.name = name
		self.obj = obj
		self.constraints = constraints
		self.params = params

class Variable_node:
	def __init__(self, name):
		self.name = name
		self.type = typename
		self.num_particles = 50
		self.weighted_particles={} 

	def send_msg_to_constraint(self, constraint):
		all_particles = [] 
		for c in self.weighted_particles:
			if c is not constraint:
				all_particles+=self.weighted_particles[c]
		wts = [pw[1] for pw in all_particles]
		pts = [pw[0] for pw in all_particles]
		wts = wts/np.sum(wts)
		msg = [(pt,wt) for pt, wt in zip(pts, wts)]
		return msg 


	def receive_msg_from_constraint(self, constraint, msg):
		self.weighted_particles[constraint] = msg


	def belief_update(self):
		for c in self.weighted_particles: 
			all_particles+=self.weighted_particles[c]
		wts = [pw[1] for pw in all_particles]
		pts = [pw[0] for pw in all_particles]
		wts = wts/np.sum(wts)
		belief = [(pt,wt) for pt, wt in zip(pts, wts)]
		return belief 


	def get_sample_from_belief(self):
		belief = self.belief_update()
		sampled_particles = []
		norm_weights = [b[1] for b in belief]
		sample = np.random.choice(items, size=len(norm_weights), p=norm_weights )
		return sample 




class Constraint_node:
	def __init__(self, name, variables, constraint_function):
		self.constraint_function = constraint_function
		self.variables = variables
		self.name = name
		self.variable_msgs = {}

	def receive_msg_from_variable(self, variabletype, msg):
		self.variable_msgs[variabletype] = msg 

	def send_msg_to_variable(self, sampled_belief, variablename, variabletype):
		if self.name == 'CFree':
			msg = None
			if variabletype == 'Trajectory':
				msg = self.constraint_function(sampled_belief, self.variable_msgs['Pose'], target=variabletype)
			elif variabletype == 'Pose':
				msg = self.constraint_function(self.variable_msgs['Trajectory'],sampled_belief, target=variabletype)
			return msg

		elif self.name == 'Kin':
			msg = None
			if variabletype == 'Grasp':
				msg = self.constraint_function(sampled_belief, self.variable_msgs['Configuration'], self.variable_msgs['Pose'],target=variabletype)
			elif variabletype == 'Configuration':
				msg = self.constraint_function(self.variable_msgs['Grasp'], sampled_belief, self.variable_msgs['Pose'],target=variabletype)
			elif variabletype == 'Pose':
				msg = self.constraint_function(self.variable_msgs['Grasp'], self.variable_msgs['Configuration'], sampled_belief, target=variabletype)
			return msg 

		elif self.name == 'Grasp':
			msg = self.constraint_function(sampled_belief, None, None)
			return msg 

		elif self.name == 'Stable':
			msg = self.constraint_function(sampled_belief, None, None)
			return msg 

 
	def kin_func(self, grasps, confs, poses, target):


class HCSP: 
	factor_graph = {}


class Plan_skeleton:
	def __init__(self, instructions):
		self.actions=[]
		self.instructions=instructions
		self.constraints = {'CFree':[('T','Trajectory'),('p', 'Pose')],
							'Kin':[('p', 'Pose'),('g','Grasp'),('q','Configuration')]}
		self.cfuncs = {'CFree': self.collision_free_func,
					   'Kin': self.kin_func,
					   'Stable':self.stable_func,
					   'Grasp':self.grasp_func}


	def get_skeleton(self):
		#forward search to densify instructions
		pick = Action('pick','mug', ['CFree', 'Kin'], ['q','p','g','T'])
		place = Action('place','mug', ['CFree', 'Kin'], ['q','p','g','T'])
		actions = [pick, place]
		self.actions=actions
		return actions


	def build_hcsp(self):
		hcsp = HCSP()
		cons = []
		for c in self.constraints:
			func = self.cfuncs[c]
			constraint = Constraint_node(c, self.constraints[c], func)
			variables = [Variable_node(n[0],n[1]) for n in self.constraints[c]]
			hcsp.factor_graph[c] = [constraint, (variables)] 
		return hcsp


	def print_hcsp(self, hcsp):
		for c in hcsp.factor_graph:
			print(c)
			print([v.name for v in hcsp.factor_graph[c][1]])
			print('______________________')


	def collision_free_func(self, trajs, poses, target):
		if target == 'Trajectory':
			traj_weights=[] 
			pose_max = self.get_best(poses)
			only_traj = [t[0] for t in trajs]
			for traj in only_traj:
				wt = pu.collision_score_traj_obst(traj, pose_max)
				traj_weights.append(wt)
			traj_weights = traj_weights/np.sum(traj_weights)
			msg = [(pt, wt) for pt,wt in zip(only_traj, traj_weights)]
			return msg

		elif target == 'Pose':
			pose_weights=[] 
			traj_max = self.get_best(trajs)
			only_pose = [p[0] for p in poses]
			for pose in only_pose:
				wt = pu.collision_score_pose_obst(pose, traj_max)
				pose_weights.append(wt)
			pose_weights = pose_weights/np.sum(pose_weights)
			msg = [(pt,wt) for pt, wt in zip(only_pose, pose_weights)]
			return msg


	def grasp_func(self, grasps, blah=None, bloh=None):
		only_grasps = [g[0] for g in grasps]
		grasp_weights = []
		for grasp in only_grasps:
			wt = pu.grasp_score_grasp(grasp)
			grasp_weights.append(wt)
		grasp_weights = grasp_weights/np.sum(grasp_weights)
		msg = [(pt, wt) in zip(only_grasps, grasp_weights)]
		return msg 


	def stable_func(self, stables, blah=None, bloh=None):
		only_stables = [g[0] for g in stables]
		stable_weights = []
		for stable in only_stables:
			wt = pu.stable_score_stable(stable)
			stable_weights.append(wt)
		stable_weights = stable_weights/np.sum(stable_weights)
		msg = [(pt, wt) in zip(only_stables, stable_weights)]
		return msg


	def get_best(self, particles):
		pwts = [p[1] for p in particles]
		max_part = particles[np.argmax(pwts)][0]
		return max_part


	def kin_func(self, grasps, confs, poses, target):
		if target == "Configuration":
			gmax = self.get_best(grasps)
			pmax = self.get_best(poses)
			only_confs = [q[0] for q in confs]
			conf_weights = []
			for conf in only_confs:
				wt = pu.kin_score_conf(conf, pmax, gmax)
				conf_weights.append(wt)
			conf_weights = conf_weights/np.sum(conf_weights)
			msg = [(pt,wt) for pt, wt in zip(only_confs, conf_weights)]
			return msg

		elif target == "Pose":
			gmax = self.get_best(grasps)
			cmax = self.get_best(confs)
			only_pose = [p[0] for p in poses]
			pose_weights=[]
			for pose in only_pose:
				wt = pu.kin_score_poses(pose, cmax, gmax)
				pose_weights.append(wt)
			pose_weights = pose_weights/np.sum(pose_weights)
			msg = [(pt,wt) for pt, wt in zip(only_pose, pose_weights)]
			return msg

		elif target == "Grasp":
			pmax = self.get_best(poses)
			cmax = self.get_best(confs)
			only_grasps = [g[0] for g in grasps]
			grasp_weights = []
			for grasp in only_grasps:
				wt = pu.kin_score_grasps(grasp, cmax, pmax)
				grasp_weights.append(wt)
			grasp_weights = grasp_weights/np.sum(grasp_weights)
			msg = [(pt, wt) in zip(only_grasps, grasp_weights)]
			return msg

		else:
			return None  


class PMPNBP:
	def __init__(self, hcsp):
		self.hcsp = hcsp 


	def initialize_variables_with_prior(self, prior):
		pass

	def pass_variables_to_constraint_msg(self):
		for constraint in self.hcsp.factor_graph:
			variables = self.hcsp.factor_graph[constraint][1]
			const = self.hcsp.factor_graph[constraint][0]
			for var in variables:
				msg = var.send_msg_to_constraint(constraint)
				const.receive_msg_from_variable(var.type, msg)

	def pass_constraint_to_variable_msg(self):
		for constraint in self.hcsp.factor_graph:
			variables = self.hcsp.factor_graph[constraint][1]
			const = self.hcsp.factor_graph[constraint][0]
			for var in variables:
				sampled_belief = var.get_sample_from_belief()
				msg = const.send_msg_to_variable(sampled_belief, var.name, var.type)
				var.receive_msg_from_constraint(const.name, msg)

	def pass_messages_across_factor_graph(self):
		self.pass_variables_to_constraint_msg()
		self.pass_constraint_to_variable_msg()









if __name__ == '__main__':
	ps = Plan_skeleton(['pick mug', 'pour water in mug'])
	hcsp = ps.build_hcsp()	
	ps.print_hcsp(hcsp) 