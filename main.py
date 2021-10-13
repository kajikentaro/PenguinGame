#%%
import colorsys
import tkinter as tk
import random
from tkinter.constants import BOTTOM, CENTER
CARD_NUM = 7
PLAYER_NUM = 4
CARDS_CLASS = 5

selectingCol = None
selectingRow = None
selectingColor = None

# ウィンドウ描写
rectWidth = int(640 / CARD_NUM)
rectHeight = int(480 / CARD_NUM)
ground  = tk.Tk()
ground.title("bousai")
ground.geometry(str(CARD_NUM * rectWidth + 200) + "x" + str(CARD_NUM * rectHeight + 200))

# クリックイベントの定義
def clickColor(color_num):
	onClick(color = color_num)
def clickRect(v):
	y = int(v.y / rectHeight)
	x = int((v.x - rectWidth * (CARD_NUM - y - 1) / 2) / rectWidth)
	onClick(row = y, col = x)

# カードボタンを表示
buttonParent = tk.Frame(ground)
buttonParent.pack(side = tk.BOTTOM)
for i in range(1,CARDS_CLASS+1,1):
	def command():
		val = i
		def closer():
			clickColor(val)
		return closer
	button = tk.Button(buttonParent, text=str(i), command=command(), width=10)
	button.pack(side = tk.RIGHT)

def hsvToRgb(h,s,v):
	rgbTuple = colorsys.hsv_to_rgb(h,s,v)
	rgbHexStr = "#"
	for i in rgbTuple:
		rgbHexStr += hex(int(i * 255))[2:]
	return rgbHexStr
def fieldToRGB(fieldStatus):
	if(fieldStatus == 0): return "#ddd"
	colorRatio = fieldStatus / CARDS_CLASS
	return hsvToRgb(colorRatio, 0.86, 0.9)

# 枠の描写とクリックイベントの設定
def drawField():
	canvasWidth = CARD_NUM * rectWidth
	canvasHeight = CARD_NUM * rectHeight
	canvas = tk.Canvas(ground, width = canvasWidth, height = canvasHeight)
	canvas.place(x=100, y=100)
	for i in range(CARD_NUM):
		x0 = (CARD_NUM - i - 1) * rectWidth / 2
		y0 = rectHeight * i
		for j in range(i + 1):
			id = "rect" + str(i * CARD_NUM + j)
			canvas.create_rectangle(x0, y0, x0 + rectWidth, y0 + rectHeight, fill = fieldToRGB(field[i][j]), outline = "#000", tags=id)
			canvas.tag_bind(id, "<Button-1>", clickRect,3)
			x0 += rectWidth
# カードを配る
cardSum = int((1 + CARD_NUM) * CARD_NUM / 2)
cards = []
for i in range(cardSum):
	cards.append(i % CARDS_CLASS)
random.shuffle(cards)
playerHands = []
for i in range(PLAYER_NUM):
	playerHands.append([0] * CARDS_CLASS)
for i in range(cardSum):
	playerNo = i % PLAYER_NUM 
	card = cards[i]
	playerHands[playerNo][card] += 1

# フィールド初期化
field = []
for i in range(CARD_NUM):
	line = [-1] * CARD_NUM
	for j in range(i+1):
		line[j] = 0
	field.append(line)
drawField()

# ゲーム用関数
def isLegalCardSelect(color, row, col):
	if(row >= CARD_NUM or row < 0): return False
	if(col >= CARD_NUM or col < 0): return False
	if(color >= CARDS_CLASS + 1 or color < 0): return False
	# すでにカードがおいてあるか、場外の場合
	if(field[row][col] != 0): return False
	# 最下行の場合
	if(row == CARD_NUM - 1):
		# 端の場合
		if(col == 0 or col == CARD_NUM - 1): return True
		# 端じゃない場合、側にカードが無いと置けない
		if(field[row][col-1] != 0 or field[row][col+1] != 0): return True
		return False
	# 中段の場合、その下が同じ色の必要がある
	if(field[row+1][col] == color or field[row+1][col+1] == color): return True
	else: return False

def onClick(row = None, col = None, color = None):
	global selectingCol, selectingRow, selectingColor
	if(row != None): selectingRow = row
	if(col != None): selectingCol = col
	if(color != None): selectingColor = color
	if(selectingCol == None or selectingRow == None or selectingColor == None): return
	# カードが正しく選ばれたか検証
	if(isLegalCardSelect(selectingColor, selectingRow, selectingCol) == False):
		print("wrong selection")
		selectingRow, selectingCol, selectingColor = None, None, None
		return
	# OKな場合は続ける
	field[selectingRow][selectingCol] = selectingColor
	drawField()
	selectingRow, selectingCol, selectingColor = None, None, None
	global playerNo
	playerNo = (playerNo + 1) % PLAYER_NUM

ground.mainloop()
