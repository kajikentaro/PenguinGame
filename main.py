#%%
import colorsys
import tkinter as tk
import random
from tkinter.constants import BOTTOM, CENTER
class PenguinGame:
	CARD_NUM = 7
	PLAYER_NUM = 4
	CARDS_CLASS = 5


	selectingCol = None
	selectingRow = None
	selectingColor = None
	playerNo = 0
	field = []
	ground = None
	canvas = None

	rectWidth = int(640 / CARD_NUM)
	rectHeight = int(480 / CARD_NUM)

	def __init__(self):
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
		for i in range(1,self.CARDS_CLASS+1,1):
			def command():
				val = i
				def closer():
					self.onClick(color = val)
				return closer
			button = tk.Button(buttonParent, text=str(i), command=command(), width=10)
			button.pack(side = tk.RIGHT)
		# フィールド初期化
		for i in range(self.CARD_NUM):
			line = [-1] * self.CARD_NUM
			for j in range(i+1):
				line[j] = 0
			self.field.append(line)
		# カードを配る
		cardSum = int((1 + self.CARD_NUM) * self.CARD_NUM / 2)
		cards = []
		for i in range(cardSum):
			cards.append(i % self.CARDS_CLASS)
		random.shuffle(cards)
		playerHands = []
		for i in range(self.PLAYER_NUM):
			playerHands.append([0] * self.CARDS_CLASS)
		for i in range(cardSum):
			self.playerNo = i % self.PLAYER_NUM 
			card = cards[i]
			playerHands[self.playerNo][card] += 1
		self.updateDraw()
		self.ground.mainloop()
		
	def onClick(self,row = None, col = None, color = None):
		# ゲーム用関数
		def isLegalCardSelect(color, row, col):
			if(row >= self.CARD_NUM or row < 0): return False
			if(col >= self.CARD_NUM or col < 0): return False
			if(color >= self.CARDS_CLASS + 1 or color < 0): return False
			# すでにカードがおいてあるか、場外の場合
			if(self.field[row][col] != 0): return False
			# 最下行の場合
			if(row == self.CARD_NUM - 1):
				# 端の場合
				if(col == 0 or col == self.CARD_NUM - 1): return True
				# 端じゃない場合、側にカードが無いと置けない
				if(self.field[row][col-1] != 0 or self.field[row][col+1] != 0): return True
				return False
			# 中段の場合、下二枚が埋まっていないとダメ
			if(self.field[row+1][col] == 0 or self.field[row+1][col+1] == 0): return False
			# 中段の場合、そのどちらかの下が同じ色の必要がある
			if(self.field[row+1][col] == color or self.field[row+1][col+1] == color): return True
			else: return False
		if(row != None): self.selectingRow = row
		if(col != None): self.selectingCol = col
		if(color != None): self.selectingColor = color
		if(self.selectingCol == None or self.selectingRow == None or self.selectingColor == None): return
		# カードが正しく選ばれたか検証
		if(isLegalCardSelect(self.selectingColor, self.selectingRow, self.selectingCol) == False):
			print("wrong selection")
			self.selectingRow, self.selectingCol, self.selectingColor = None, None, None
			return
		# OKな場合は続ける
		self.field[self.selectingRow][self.selectingCol] = self.selectingColor
		self.selectingRow, self.selectingCol, self.selectingColor = None, None, None
		self.playerNo = (self.playerNo + 1) % self.PLAYER_NUM
		self.updateDraw()

	def updateDraw(self):
		def hsvToRgb(h,s,v):
			rgbTuple = colorsys.hsv_to_rgb(h,s,v)
			rgbHexStr = "#"
			for i in rgbTuple:
				rgbHexStr += hex(int(i * 255))[2:]
			return rgbHexStr

		def fieldToRGB(fieldStatus):
			if(fieldStatus == 0): return "#ddd"
			colorRatio = fieldStatus / self.CARDS_CLASS
			return hsvToRgb(colorRatio, 0.86, 0.9)

		def clickRect(v):
			y = int(v.y / self.rectHeight)
			x = int((v.x - self.rectWidth * (self.CARD_NUM - y - 1) / 2) / self.rectWidth)
			self.onClick(row = y, col = x)

		# キャンバスアップデート
		self.canvas.delete("all")
		for i in range(self.CARD_NUM):
			x0 = (self.CARD_NUM - i - 1) * self.rectWidth / 2
			y0 = self.rectHeight * i
			for j in range(i + 1):
				id = "rect" + str(i * self.CARD_NUM + j)
				self.canvas.create_rectangle(x0, y0, x0 + self.rectWidth, y0 + self.rectHeight, fill = fieldToRGB(self.field[i][j]), outline = "#000", tags=id)
				self.canvas.tag_bind(id, "<Button-1>", clickRect,3)
				x0 += self.rectWidth


main = PenguinGame()