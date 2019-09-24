import gym
import numpy as np 
import matplotlib.pyplot as plt

from JSAnimation.IPython_display import display_animation
from matplotlib import animation
from IPython.display import display

def display_frames_as_gif(frames):
    """
    Displays a list of frames as a gif, with controls
    """
    plt.figure(figsize=(frames[0].shape[1]/72.0, frames[0].shape[0]/72.0),
               dpi=72)
    patch = plt.imshow(frames[0])
    plt.axis('off')
 
    def animate(i):
        patch.set_data(frames[i])
 
    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames),
                                   interval=50)
 
    display(display_animation(anim, default_mode='loop'))

gamma = 0.9
alpha = 0.8
max_step = 200
num_episodes = 1000

class agent:
	def __init__(self, num_states, num_actions):
		self.num_states = num_states
		self.num_actions = num_actions
		self.brain = Brain(num_states, num_actions)

	def update_q_function(self, observation,action, reward, observation_next):
		self.brain.update_qtable(observation, action,reward,observation_next)

	def get_action(self, observation,step):
		action = self.brain.decide_action(observation, step)
		return action

class Brain:
	def __init__(self, num_states, num_actions):
		self.num_states = num_states
		self.num_actions = num_actions
		self.q_table = np.random.uniform(low=0,high=1,size=(6**self.num_states,self.num_actions))

	def bins(self, clip_min, clip_max,num):
		return np.linspace(clip_min, clip_max, num+1)[1:-1]

	def digitize_state(self, observation):
		cart_pos, cart_v, pole_angle, pole_v= observation
		digitized =[
		np.digitize(cart_pos, bins=self.bins(-2.4, 2.4, 6)),
		np.digitize(cart_v, bins=self.bins(-3.0, 3.0, 6)),
		np.digitize(pole_angle, bins=self.bins(-0.5, 0.5, 6)),
		np.digitize(pole_v, bins=self.bins(-2.0, 2.0, 6))
		]
		return sum([x*(6**i) for i, x in enumerate(digitized)])
	def update_qtable(self, observation, action, reward, observation_next):
        # QテーブルをQ学習により更新
        # 観測を離散化
		state = self.digitize_state(observation)
		state_next = self.digitize_state(observation_next)
		Max_Q_next = max(self.q_table[state_next][:])
		self.q_table[state, action] = self.q_table[state, action] + alpha * (reward + gamma * Max_Q_next - self.q_table[state, action])
 
	def decide_action(self, observation, episode):
		state = self.digitize_state(observation)
		epsilon = 0.5*(1/(1+episode))

		if epsilon <= np.random.uniform(0, 1):
			action = np.argmax(self.q_table[state][:])
		else:
			action = np.random.choice(self.num_actions) # 0,1の行動をランダムに返す
		return action

class Environment:
	def __init__(self):
		self.env = gym.make('CartPole-v0')
		self.num_states = self.env.observation_space.shape[0]
		self.num_actions = self.env.action_space.n 
		self.agent = agent(self.num_states, self.num_actions)

	def run(self):
		complete_episodes = 0
		episode_final = False

		for episode in range(200):
			observation = self.env.reset()
			episode_reward = 0

			for step in range(200):

				if episode_final is True:
					frames.append(self.env.render(mode='rgb_array'))
				action = self.agent.get_action(observation, episode) 
				observation_next, reward_notuse, done, info_notuse = self.env.step(action)

				if done:
					if step < 195:
						reward = -1
						self.complete_episodes = 0 
					else:
						reward = 1 
						self.complete_episodes = self.complete_episodes + 1
				else:
					reward = 0

				episode_reward +=reward 

				self.agent.update_q_function(observation, action, reward, observation_next)
 
                # 観測の更新
				observation = observation_next
 
                # 終了時の処理
				if done:
					print('{0} Episode: Finished after {1} time steps'.format(episode, step+1))
					break
 
			if episode_final is True:
                # 動画を保存と描画
				display_frames_as_gif(frames)
				break
 
			if self.complete_episodes >= 10:
				print('10回連続成功')
				frames = []
				episode_final = True  # 次の試行を描画を行う最終試行とする

cartpole_env = Environment()
cartpole_env.run()
