#%%
import numpy as np
import colorsys
import tkinter as tk
import random
import gym
from gym import spaces
import math
from tkinter.constants import BOTTOM, CENTER
import os
from numpy.lib.function_base import place
from stable_baselines3 import PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.env_checker import check_env

class Field:
	CARD_NUM, CARD_SUM, PLAYER_NUM, CARDS_CLASS = None, None, None, None

	field2d = None
	field1d = None
	playerHands = None

	def __init__(self, CARD_NUM = 6, PLAYER_NUM = 2, CARDS_CLASS = 5):
		self.CARD_NUM = CARD_NUM
		self.CARD_SUM = int((1 + CARD_NUM) * CARD_NUM / 2)
		self.PLAYER_NUM = PLAYER_NUM
		self.CARDS_CLASS = CARDS_CLASS

		# フィールド初期化
		self.field1d = [0] * self.CARD_SUM
		self.field2d = []
		for i in range(self.CARD_NUM):
			# -2 が禁止エリア
			line = [-2] * self.CARD_NUM
			for j in range(i+1):
				# -1 が未配置
				line[j] = -1
			self.field2d.append(line)
		# カードを配る
		cards = []
		for i in range(self.CARD_SUM):
			cards.append(i % self.CARDS_CLASS)
		random.shuffle(cards)
		self.playerHands = []
		for i in range(self.PLAYER_NUM):
			self.playerHands.append([0] * self.CARDS_CLASS)
		for i in range(self.CARD_SUM):
			playerNo = i % self.PLAYER_NUM 
			card = cards[i]
			self.playerHands[playerNo][card] += 1
	def placeCard(self, row, col, color, playerNo):
		if(self.isLegalCardSelect(row, col, color, playerNo) == False):
			return False
		else:
			self.field2d[row][col] = color
			self.playerHands[playerNo][color] -= 1
			position = self.rowColToPos(row, col)
			self.field1d[position] = color + 1
			return True
	def getCardSet(self):
		return self.CARD_NUM, self.CARD_SUM, self.PLAYER_NUM, self.CARDS_CLASS
	def getObservation(self, playerNo):
		return np.array(self.field1d + self.playerHands[playerNo])

	# ゲーム用関数
	def isLegalCardSelect(self,row, col, color, playerNo):
		OUTBOARD = -2
		BLANK = -1
		if(row >= self.CARD_NUM or row < 0): return False
		if(col >= self.CARD_NUM or col < 0): return False
		if(color >= self.CARDS_CLASS or color < 0): return False
		# 手持ちのカードがない場合
		if(self.playerHands[playerNo][color] <= 0): return False
		# すでにカードがおいてあるか、場外の場合
		if(self.field2d[row][col] != BLANK): return False
		# 最下行の場合
		if(row == self.CARD_NUM - 1):
			# 端の場合
			if(col == 0 or col == self.CARD_NUM - 1): return True
			# 端じゃない場合、側にカードが無いと置けない
			if(self.field2d[row][col-1] != BLANK or self.field2d[row][col+1] != BLANK): return True
			return False
		# 中段の場合、下二枚が埋まっていないとダメ
		if(self.field2d[row+1][col] == BLANK or self.field2d[row+1][col+1] == BLANK): return False
		# 中段の場合、そのどちらかの下が同じ色の必要がある
		if(self.field2d[row+1][col] == color or self.field2d[row+1][col+1] == color): return True
		else: return False
	def posToRowCol(self, cardPos):
		row = int((1 + math.sqrt(8*cardPos)) / 2)
		col = cardPos - int(row * (row - 1) / 2)
		return (row, col)
	def rowColToPos(self, row, col):
		return int(row * (row - 1) / 2 + col)

	# ランダムにカードを配置する。成功したらTrue、失敗(負けた場合)はFalse
	def randomSelect(self, playerNo):
		BLANK = -1
		for i in range(self.CARD_NUM):
			for j in range(i+1):
				if(self.field2d[i][j] != BLANK): continue
				for k in range(self.CARDS_CLASS):
					if(self.placeCard(i,j,k,playerNo) == False): continue
					return True
		return False
	def isPlayerAlive(self, playerNo):
		BLANK = -1
		for i in range(self.CARD_NUM):
			for j in range(i+1):
				if(self.field2d[i][j] != BLANK): continue
				for k in range(self.CARDS_CLASS):
					if(self.isLegalCardSelect(i,j,k,playerNo) == False): continue
					return True
		return False


class PenguinGame(gym.Env):
	model = None
	field = None
	


	def __init__(self):
		super(PenguinGame, self).__init__()
		field = Field()
		CARD_NUM, CARD_SUM, PLAYER_NUM, CARDS_CLASS = field.getCardSet()
		self.action_space = spaces.MultiDiscrete([CARD_SUM, CARDS_CLASS])
		self.observation_space = spaces.MultiDiscrete([CARDS_CLASS + 1] * CARD_SUM + [int(CARD_SUM / PLAYER_NUM + 1)] * CARDS_CLASS)
		if os.path.exists("saved-model.zip"):
			self.model = PPO.load("saved-model")
	def reset(self):
		self.field = Field()
		return self.field.getObservation(0)
	def predictEnemy(self, observation):
		if self.model == None:
			self.field.randomSelect(1)
			return True
		# 5回predictしても配置できなかったらランダムになる
		for _ in range(5):
			action, _ = self.model.predict(observation)
			(row, col) = self.field.posToRowCol(action[0])
			color = action[1]
			if self.field.placeCard(row, col, color, 1) == True:
				return True
		self.field.randomSelect(1)
			

		
	def step(self, action):
		observation, reward, done, info = None, None, False, {}
		(row, col) = self.field.posToRowCol(action[0])
		color = action[1]
		if self.field.placeCard(row, col, color, 0) == False:
			# 選択に失敗した場合
			observation = self.field.getObservation(0)
			reward = -0.2
			done = False
			return observation, reward, done, info

		if self.field.isPlayerAlive(1) == False:
			# 勝ち越し
			# 渡さなくてもいいTODO
			observation = self.field.getObservation(0)
			reward = 1.0
			done = True
			return observation, reward, done, info
		else: 
			# 敵の番
			observation_enemy = self.field.getObservation(1)
			self.predictEnemy(observation_enemy)
			if self.field.isPlayerAlive(0) == True:
				# 続行できる場合
				observation = self.field.getObservation(0)
				reward = 0.5
				return observation, reward, done ,info
			else:
				# 負けた場合
				observation = self.field.getObservation(0)
				reward = 0.5
				done = True
				return observation, reward, done, info

	renderMod = None
	def render(self, mode="console"):
		if mode != 'console':
			raise NotImplementedError()
		if self.renderMod == None:
			self.renderMod = Render(self.field)
		self.renderMod.updateDraw()

class Render:
	CARD_NUM, CARD_SUM, PLAYER_NUM, CARDS_CLASS = None, None, None, None
	rectWidth = None
	rectHeight = None
	ground = None
	canvas = None
	labelText1 = None
	labelText2 = None
	labelText3 = None

	field = None
	def __init__(self, field):
		self.CARD_NUM, self.CARD_SUM, self.PLAYER_NUM, self.CARDS_CLASS = field.getCardSet()
		self.rectWidth = int(640 / self.CARD_NUM)
		self.rectHeight = int(480 / self.CARD_NUM)
		self.field = field
		self.initDraw()

	def initDraw(self):
		# ウィンドウ描写
		self.ground  = tk.Tk()
		self.ground.title("bousai")
		self.ground.geometry(str(self.CARD_NUM * self.rectWidth + 200) + "x" + str(self.CARD_NUM * self.rectHeight + 200))
		# キャンバス(ピラミッド)作成
		canvasWidth = self.CARD_NUM * self.rectWidth
		canvasHeight = self.CARD_NUM * self.rectHeight
		self.canvas = tk.Canvas(self.ground, width = canvasWidth, height = canvasHeight)
		self.canvas.place(x=100, y=100)
		# カードボタンを表示
		buttonParent = tk.Frame(self.ground)
		buttonParent.pack(side = tk.BOTTOM)
		for i in range(self.CARDS_CLASS,0,-1):
			def command():
				val = i
				def closer():
					self.onClick(color = val)
				return closer
			button = tk.Button(buttonParent, text=str(i), command=command(), width=10)
			button.pack(side = tk.RIGHT)
		# ラベル表示
		self.labelText1= tk.StringVar()
		self.labelText1.set("init text")
		self.labelText2= tk.StringVar()
		self.labelText2.set("init text")
		self.labelText3= tk.StringVar()
		self.labelText3.set("")
		tk.Label(self.ground, textvariable=self.labelText1).pack(side = tk.TOP)
		tk.Label(self.ground, textvariable=self.labelText2).pack(side = tk.TOP)
		tk.Label(self.ground, textvariable=self.labelText3).pack(side = tk.TOP)

	def updateDraw(self):
		def hsvToRgb(h,s,v):
			rgbTuple = colorsys.hsv_to_rgb(h,s,v)
			rgbHexStr = "#"
			for i in rgbTuple:
				rgbHexStr += hex(int(i * 255))[2:]
			return rgbHexStr

		def fieldToRGB(fieldStatus):
			if(fieldStatus == -1): return "#ddd"
			colorRatio = fieldStatus / self.CARDS_CLASS
			return hsvToRgb(colorRatio, 0.86, 0.9)

		def clickRect(v):
			y = int(v.y / self.rectHeight)
			x = int((v.x - self.rectWidth * (self.CARD_NUM - y - 1) / 2) / self.rectWidth)
			self.onClick(row = y, col = x)

		# ラベルアップデート
		self.labelText1.set(str(self.field.playerHands[0]))
		self.labelText2.set(str(self.field.playerHands[1]))
		# キャンバスアップデート
		self.canvas.delete("all")
		for i in range(self.CARD_NUM):
			x0 = (self.CARD_NUM - i - 1) * self.rectWidth / 2
			y0 = self.rectHeight * i
			for j in range(i + 1):
				id = "rect" + str(i * self.CARD_NUM + j)
				self.canvas.create_rectangle(x0, y0, x0 + self.rectWidth, y0 + self.rectHeight, fill = fieldToRGB(self.field.field2d[i][j]), outline = "#000", tags=id)
				self.canvas.tag_bind(id, "<ButtonRelease-1>", clickRect,3)
				x0 += self.rectWidth
		self.ground.update()

# %%
"""
for i in range(15):
	env = PenguinGame()
	model = PPO('MlpPolicy', env, verbose=1)
	if i != 0:
		model.load("saved-model")
	model.learn(total_timesteps=25000)
	model.save("saved-model")
	print(i)
"""
env = PenguinGame()
model = PPO('MlpPolicy', env, verbose=1)
model.load("saved-model3")
#model.learn(total_timesteps=50000)
#model.save("saved-model3")

import time
obs = env.reset()
while True:
	action, _states = model.predict(obs)
	obs, rewards, dones, info = env.step(action)
	if dones:
		print("done")
		time.sleep(10)
		break
	env.render()
