import gym
import numpy as np
import random

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from gym import spaces


class Field():
	def make_agent(self, rank, seed=0):
		"""
		Utility function for multiprocessed env.

		:param env_id: (str) the environment ID
		:param num_env: (int) the number of environments you wish to have in subprocesses
		:param seed: (int) the inital seed for RNG
		:param rank: (int) index of the subprocess
		"""
		def _init():
			# FieldクラスをAgentにわたす。
			env = Agent(self)
			env.seed(seed + rank)
			return env
		set_random_seed(seed)
		return _init
	agents = []
	def regest_agent(self, agent):
		self.agents.push(agent)
	def get_distance(self):
		dist = self.agents[0].position + self.agents[1].position
		return np.array([dist]).astype(np.int)


	def __init__(self):
		agent_num = 2
		env = SubprocVecEnv([self.make_agent(i) for i in range(agent_num)])

		# Stable Baselines provides you with make_vec_env() helper
		# which does exactly the previous steps for you.
		# You can choose between `DummyVecEnv` (usually faster) and `SubprocVecEnv`
		# env = make_vec_env(env_id, n_envs=num_cpu, seed=0, vec_env_cls=SubprocVecEnv)

		model = PPO('MlpPolicy', env, verbose=1)
		model.learn(total_timesteps=25000)

		obs = env.reset()
		for _ in range(1000):
			action, _states = model.predict(obs)
			obs, rewards, dones, info = env.step(action)
			env.render()


class Agent(gym.Env):
	WALK = 0
	SHOT = 1
	GUARD = 2
	position = 0
	field = None
	def __init__(self, field):
		super(Agent, self).__init__()
		self.field = field
		self.field.regest_agent(self)
		# Define action and observation space
		# They must be gym.spaces objects
		# Example when using discrete actions, we have two: left and right
		n_actions = 3
		self.action_space = spaces.Discrete(n_actions)
		# The observation will be the coordinate of the agent
		# this can be described both by Discrete and Box space
		self.observation_space = spaces.Box(low=-10, high=10, shape=(1,), dtype=np.int)

	def reset(self):
		"""
		Important: the observation must be a numpy array
		:return: (np.array) 
		"""
		# 中心からの距離
		self.position = random.randint(10,0)
		# here we convert to float32 to make it more general (in case we want to use continuous actions)
		return self.field.get_distance()

	def step(self, action):
		if action == self.WALK:
			self.position -= 1
		elif action == self.SHOT:
			# shot method TODO
			print("TODO")
		elif action == self.GUARD:
			print("TODO")
		else:
			raise ValueError(
					"Received invalid action={} which is not part of the action space".format(action))

		# Account for the boundaries of the grid
		self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size)

		# Are we at the left of the grid?
		done = bool(self.agent_pos == 0)

		# Null reward everywhere except when reaching the goal (left of the grid)
		reward = 1 if self.agent_pos == 0 else 0

		# Optionally we can pass additional info, we are not using that for now
		info = {}

		return np.array([self.agent_pos]).astype(np.float32), reward, done, info

	def render(self, mode='console'):
		if mode != 'console':
			raise NotImplementedError()
		# agent is represented as a cross, rest as a dot
		print("." * self.agent_pos, end="")
		print("x", end="")
		print("." * (self.grid_size - self.agent_pos))

	def close(self):
		pass
