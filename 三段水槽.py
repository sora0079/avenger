import gym
import numpy as np 
import csv
import time
import os

gamma = 0.8
alpha = 0.8

class agent:
	def __init__(self, num_states, num_actions):
		self.num_states = num_states
		self.num_actions = num_actions
		self.brain = brain(num_states, num_actions)

	def update_q_function(self, observation,action, reward, observation_next):
		self.brain.update_qtable(observation, action,reward,observation_next)

	def get_action(self, observation,episode):
		action = self.brain.decide_action(observation, episode)
		return action

class brain:
	def __init__(self, num_states, num_actions):
		self.num_states = num_states
		self.num_actions = num_actions
		self.q_table = np.random.uniform(low=0,high=1,size=(20**self.num_states,self.num_actions))

	def bins(self, clip_min, clip_max,num):
		return np.linspace(clip_min, clip_max, num+1)[1:-1]

	def digitize_state(self, observation):
		LI001, LI002, LI003, FI001,FI002,V001= observation
		digitized =[
		np.digitize(LI001, self.bins(0, 100, 20)),
		np.digitize(LI002, self.bins(0, 100, 20)),
		np.digitize(LI003, self.bins(0, 100, 20)),
		np.digitize(FI001, self.bins(0, 100, 20)),
		np.digitize(FI002, self.bins(0, 100, 20)),
		np.digitize(V001, self.bins(0, 100, 20))
		]
		return sum([x*(20**i) for i, x in enumerate(digitized)])

	def update_qtable(self, observation, action, reward, observation_next):#Qtable更新

		state = self.digitize_state(observation)
		state_next = self.digitize_state(observation_next)
		Max_Q_next = max(self.q_table[state_next])
		self.q_table[state, action] = self.q_table[state, action] + alpha * (reward + gamma * Max_Q_next - self.q_table[state, action])
 
	def decide_action(self, observation, episode):
		state = self.digitize_state(observation)

		epsilon = 0.3*(1/(1+episode))

		if epsilon <= np.random.uniform(0, 1):
			action = np.argmax(self.q_table[state]) - 2
		else:
			action = np.random.choice(self.num_actions) - 2
		return action

class Environment:
	def __init__(self):
		self.num_states = 6
		self.num_actions = 5#[-2,-1,0,1,2]
		self.agent = agent(self.num_states, self.num_actions)

	def run(self):
		os.chdir("C:/Users/30043376/Documents/SandansuisouAPI")# ! delete later 

		for episode in range(1):
			reward = 0
			value = 10
			num_episode = 0

			while(True):
				os.system("read.bat")#csvからデータを初期化する
				with open ('readitems.csv','r') as observation:
					observation = csv.reader(observation)
					for i,rows in enumerate(observation):
						if i ==1:
							observation = rows
				observation = list(map(float,observation))
				if observation[0] > 5:# ! 修正
					break
				time.sleep(1)

			episode_str = str(episode+1)
			filename = 'data'+ episode_str + '.csv'
			with open(filename,"w",newline='') as csvfile:
				data = csv.writer(csvfile)
				data.writerow(["LI001","LI002","LI003","FI001","FI002","V001"])

			for step in range(200):

				with open(filename,"a",newline='') as csvfile:
					data = csv.writer(csvfile)
					data.writerows([observation])

				action = self.agent.get_action(observation, episode)
				value_next = value + action
				write_bat = open("write.bat",'w')
				write_bat.write('call SandanSuisouAPI.exe -cmd w -value %d' % value_next)
				value = value_next#value更新

				if observation[0] > 45 and observation[0] < 55:
					reward = 1
					num_episode +=1
				else:
					reward = -1 

				time.sleep(0.01)

				os.system("read.bat")
				with open ('readitems.csv','r') as observation_next:
					observation_next = csv.reader(observation_next)
					for i,rows in enumerate(observation_next):
						if i ==1:
							observation_next = rows
				observation_next = list(map(float,observation_next))

				self.agent.update_q_function(observation, action, reward, observation_next)
				observation = observation_next

			if num_episode >= 180:
				print("学習成功")
				break

		print("学習評価を行います")

		value = 10
		while(True):
			os.system("read.bat")#csvからデータを初期化する
			with open ('readitems.csv','r') as observation:
				observation = csv.reader(observation)
				for i,rows in enumerate(observation):
					if i ==1:
						observation = rows
			observation = list(map(float,observation))
			if observation[0] > 5:
				break
			time.sleep(1)

		with open("test.csv","w",newline='') as csvfile:
			data = csv.writer(csvfile)
			data.writerow(["LI001","LI002","LI003","FI001","FI002","V001"])

		for step in range(200):

			with open("test.csv","a",newline='') as csvfile:
				data = csv.writer(csvfile)
				data.writerows([observation])

			action = self.agent.get_action(observation, episode)
			value_next = value + action
			write_bat = open("write.bat",'w')
			write_bat.write('call SandanSuisouAPI.exe -cmd w -value %d' % value_next)
			value = value_next

			time.sleep(0.01)

			os.system("read.bat")
			with open ('readitems.csv','r') as observation_next:
				observation_next = csv.reader(observation_next)
				for i,rows in enumerate(observation_next):
					if i ==1:
						observation_next = rows
			observation_next = list(map(float,observation_next))

			observation = observation_next


SandanSuisou = Environment()
SandanSuisou.run()

