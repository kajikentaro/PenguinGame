#%%
import tkinter as tk
import random
CARD_NUM = 7
PLAYER_NUM = 4
CARDS_CLASS = 4

# ウィンドウ描写
rectWidth = int(640 / CARD_NUM)
rectHeight = int(480 / CARD_NUM)
def clickRect(v):
	y = int(v.y / rectHeight)
	x = int((v.x - rectWidth * (CARD_NUM - y - 1) / 2) / rectWidth)
	print(y,x)
ground  = tk.Tk()
ground.title("bousai")
ground.geometry(str(CARD_NUM * rectWidth + 200) + "x" + str(CARD_NUM * rectHeight + 200))

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

field = []
for i in range(CARD_NUM):
	line = [-1] * CARD_NUM
	for j in range(i+1):
		line[j] = 0
	field.append(line)

playerNo = -1







ground.mainloop()
#for i in range(CARD_NUM):
	#canvas.create_rectangle()
# %%
