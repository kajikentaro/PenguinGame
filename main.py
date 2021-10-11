#%%
import tkinter as tk
import random
from tkinter.constants import BOTTOM, CENTER
CARD_NUM = 7
PLAYER_NUM = 4
CARDS_CLASS = 5

selectingCol = 0

test_col = 0
testCol = 0
testcol = 0

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
for i in range(CARDS_CLASS):
	def command():
		val = i
		def closer():
			clickColor(val)
		return closer
	button = tk.Button(buttonParent, text=str(i), command=command(), width=10)
	button.pack(side = tk.RIGHT)

# 枠の描写とクリックイベントの設定
canvasWidth = CARD_NUM * rectWidth
canvasHeight = CARD_NUM * rectHeight
canvas = tk.Canvas(ground, width = canvasWidth, height = canvasHeight)
canvas.place(x=100, y=100)
for i in range(CARD_NUM):
	x0 = (CARD_NUM - i - 1) * rectWidth / 2
	y0 = rectHeight * i
	for j in range(i + 1):
		id = "rect" + str(i * CARD_NUM + j)
		canvas.create_rectangle(x0, y0, x0 + rectWidth, y0 + rectHeight, fill = "#ddd", outline = "#000", tags=id)
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
print(playerHands)

# フィールド初期化
field = []
for i in range(CARD_NUM):
	line = [-1] * CARD_NUM
	for j in range(i+1):
		line[j] = 0
	field.append(line)
print(field)

# ゲーム用関数
def isLegalCardSelect(color, row, col):
	if(row >= CARD_NUM or row < 0): return False
	if(col >= CARD_NUM or col < 0): return False
	if(color >= CARDS_CLASS or color < 0): return False
	# すでにカードがおいてあるか、場外の場合
	if(field[row][col] != 0): return False
	# 最下行の場合
	if(row == CARD_NUM - 1):
		# 端の場合
		if(row == 0 or row == CARD_NUM - 1): return True
		# 端じゃない場合、両側にカードが無いと置けない
		if(field[row][col-1] != 0 and field[row][col+1] != 0): return True
	# 中段の場合、その下が同じ色の必要がある
	if(field[row+1][col] == color and field[row+1][col+1] == color): return True
	else: return False

def onClick(row = None, col = None, color = None):
	print("clicked")
	print(testCol)
	print(testcol)
	print(test_col)
	print(selectingCol)
	if(row): selectingRow = row
	if(col): selectingCol = col
	if(color): selectingColor = color
	print(row, col, color)
	if(not (row and col and color)): return
	if(isLegalCardSelect(selectingColor, selectingRow, selectingCol)):
		print("selection is ok")
	else:
		print("wrong selection")
		selectingRow, selectingCol, selectingColor = None, None, None


# ゲームスタート
playerNo = 0
# while True:
	# print("player no: ", playerNo)






ground.mainloop()
#for i in range(CARD_NUM):
	#canvas.create_rectangle()
# %%
