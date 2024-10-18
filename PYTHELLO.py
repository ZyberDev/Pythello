print("""-----------[PYTHELLO]-----------
Developed by ZyberDev
for (and on) the
TI-84 Plus CE-T Python Edition

Dependencies: QGFX (1.0)



""")

bw=8
bh=8
board=[-1]*bw*bh
sqsz=24
cr=7

sx=0
sy=0
turn=0
takeable=[]

colors=[(16,16,16),(255,255,255)]
exec("board[27:29]=[0,1];board[35:37]=[1,0]")
if input("Enable 4 players? (y/n):")=="y":
  exec("colors=[(255,0,0),(0,192,0),(0,0,255),(255,192,0)];board[18:22]=[0,0,1,1];board[26:30]=[0,0,1,1];board[34:38]=[2,2,3,3];board[42:46]=[2,2,3,3]")

from ti_system import *
import QGFX as gr

def get_square(x,y):
  if not (0<=x<bw and 0<=y<bh):
    return -1
  return board[x+y*bw]

def set_square(x,y,v):
  board[x+y*bw]=v
  draw_coin(x,y)

def get_coords(x,y):
  return (x-bw*0.5+0.5)*sqsz+160,(y-bh*0.5+0.5)*sqsz+135

def draw_square(x,y):
  x,y=get_coords(x-0.5,y-0.5)
  gr.draw_rect(x,y,sqsz,sqsz)

def draw_coin(x,y):
  t=get_square(x,y)
  x,y=get_coords(x,y)
  if t==-1:return
  c=gr.Color.from_8bit(colors[t])
  gr.set_color(c)
  gr.fill_circle(x,y,cr)
  gr.set_color(c.mul(.75))
  gr.fill_circle(x,y,cr-2)

def draw_big_coin():
  c=gr.Color.from_8bit(colors[turn])
  gr.set_color(0,96,0)
  gr.fill_circle(290,60,26)
  gr.set_color(c)
  gr.fill_circle(290,60,24)
  gr.set_color(c.mul(.75))
  gr.fill_circle(290,60,20)

def draw_board():
  gr.set_color(0,128,0)
  gr.fill_rect(0,0,320,240)
  gr.set_color(0,96,0)
  gr.set_pen(3,0)
  for _ in range(2):
    for i in range(bw*bh):
      draw_square(i//bh,i%bh)
    gr.set_color(0,64,0)
    gr.set_pen(1,0)

def draw_coins():
  for i in range(bw*bh):
    draw_coin(i//bh,i%bh)

def select_square(x,y):
  global sx,sy
  gr.set_color(0,64,0)
  gr.set_pen(1,0)
  draw_square(sx,sy)
  sx,sy=x,y
  if len(takeable)==0:
    gr.set_color(255,0,0)
    gr.set_pen(1,1)
  else:
    gr.set_color(255,255,255)
  draw_square(x,y)

def get_takeable(x,y):
  global takeable
  takeable=[]
  if get_square(x,y)!=-1:
    return
  for dx,dy in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
    l=[]
    for i in range(1,max(bw,bh)):
      s=get_square(x+dx*i,y+dy*i)
      if s==-1:
        break
      if s==turn:
        takeable.extend(l)
        break
      l.append((x+dx*i,y+dy*i))

def take():
  set_square(sx,sy,turn)
  for x,y in takeable:
    set_square(x,y,turn)

draw_board()
draw_coins()
select_square(4,4)
draw_big_coin()
gr.set_color(0,64,0)
gr.draw_string(270,90,"TURN")
gr.flush()
while True:
  k=wait_key()
  if k in [1,2,3,4]:
    dx,dy=[(1,0),(-1,0),(0,-1),(0,1)][k-1]
    x,y=(sx+dx)%bw,(sy+dy)%bh
    get_takeable(x,y)
    gr.flush()
    select_square(x,y)
    gr.flush()
  elif k==5 and len(takeable)!=0:
    gr.flush()
    take()
    turn=(turn+1)%len(colors)
    gr.flush()
    for i in range(bw*bh):
      get_takeable(i//bw,i%bh)
      if len(takeable)!=0:
        select_square(i//bw,i%bh)
        break
    if len(takeable)==0:
      break
    draw_big_coin()
    gr.flush()
  elif k==9:
    break
sleep(1)
gr.set_color(0,128,0)
gr.fill_rect(0,0,320,240)
gr.set_color(0,64,0)
gr.draw_string(120,64,"GAME OVER")
gr.flush()
x=160+-(len(board)-board.count(-1))//8*4-8*(len(colors)-1)
for i in range(len(colors)):
  gr.set_color(colors[i])
  n=board.count(i)
  for j in range(n):
    gr.fill_circle((j//8)*8+x+2.5,161.5-(j%8)*8,2.5)
    gr.flush()
  gr.draw_string(x,169,str(n))
  x+=-(-n//8)*8+16
disp_wait()