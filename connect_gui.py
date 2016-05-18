from Tkinter import *
import ttk
from ttk import Combobox
import random
import functools
import connectfour 
import minimax
import utility 
import player

class ConnectGui:
    def __init__(self,root):
	root.title("Connect Four") 
	self.turn= 1 
	self.last_piece= None
	self.p1= None
	self.p2= None

	frame = Frame(root)
	frame.pack(side=TOP)

	label1 = Label(frame, text="Player 1:")
	label1.pack(side= LEFT)
	
	self.combobox = Combobox(frame, values= ('Human', 'Minimax', 'Random'))
        self.combobox.pack(side=LEFT)

	label2 = Label(frame, text="Player 2:")
        label2.pack(side=LEFT)

	self.combobox1 = Combobox(frame, values= ('Human', 'Minimax','Random'))
        self.combobox1.pack(side= LEFT)

	frame2= Frame(root)
	frame2.pack(side=TOP)

	label3= Label(frame2, text= "(If Minimax Chosen) Ply-Depth:")
	label3.pack(side= LEFT) 
	
	self.spinner = Spinbox(frame2,width=5,from_=2, to=5)
	self.spinner.pack(side= LEFT ) 

	playbutton = Button(frame2, text= "Start Game", command= self.play_game) 
	playbutton.pack(side= LEFT, padx= 20) 

	frame1= Frame(root)
	frame1.pack(side=TOP)

	for x in range(7):
	    button0 = Button(frame1, text= "Column %i" %(x+1), command = functools.partial(self.human_turn,x))
	    button0.grid(row=0, column= x) 
	
	self.b= connectfour.ConnectFour()
	self.board= Canvas(frame1, width= 705, height= 605)
	self.board.grid(row= 1, columnspan=7) 

	#for x in range(7):
	#    self.board.create_line(5, x*100+5, 705,x*100+5)
	#for x in range(8):    
	#    self.board.create_line(x*100+5, 5, x*100+5, 605)
	
    def human_turn(self, col):
	assert self.p1 and self.p2!= None
	assert self.b.is_game_over()== None
	if self.b.board[5][col]== None:
	    y= 0 
	    while self.b.board[y][col]!= None:
		y+=1
	    self.b.play_turn(self.turn, col)
	if self.last_piece!= None:
	    self.board.itemconfig(self.last_piece, outline= "black", width= 1) 
	if self.turn== 1: 
	    self.last_piece= self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "red", outline= "green", width= 5)
	    self.turn=2
	    if self.b.is_game_over()!= None:
	        win= self.b.is_game_over()
		for i in range(4):
   		    self.board.create_oval(100*(win[1]+i*win[3])+5,505-100*(win[0]+i*win[2]),100*(win[1]+i*win[3])+105,605-100*(win[0]+i*win[2]), outline= "blue", width= 7)
		return
	if self.p2== "Human":
		pass
	elif self.p2== "Random":
		return self.random_turn()
	elif self.p2== "Minimax":
		return self.minimax_turn()
	elif self.turn==2:
	    self.last_piece=self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "yellow", outline= "green", width= 5) 
	    self.turn=1
	    if self.b.is_game_over()!= None:
	        win= self.b.is_game_over()
		for i in range(4):
   		    self.board.create_oval(100*(win[1]+i*win[3])+5,505-100*(win[0]+i*win[2]),100*(win[1]+i*win[3])+105,605-100*(win[0]+i*win[2]), outline= "blue", width= 7)
		return 
	if self.p1== "Human":
		pass
	elif self.p1== "Random":
		return self.random_turn()
	elif self.p1== "Minimax":
		return self.minimax_turn()
    
    def random_turn(self):
	if self.last_piece!= None:
	    self.board.itemconfig(self.last_piece, outline= "black", width= 1) 
	cols = []
        for col in range(7):
            if self.b.get_position(5, col) == None:
                cols.append(col)
	col= random.choice(cols)
	if self.b.board[5][col]== None:
	    y= 0 
	    while self.b.board[y][col]!= None:
		y+=1
	    self.b.play_turn(self.turn, col)
	if self.turn== 1: 
	    self.last_piece= self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "red", outline= "green", width= 5)
	    self.turn=2
	elif self.turn==2:
	    self.last_piece=self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "yellow", outline= "green", width= 5) 
	    self.turn=1
	if self.b.is_game_over()!= None:
	        win= self.b.is_game_over()
		for i in range(4):
   		    self.board.create_oval(100*(win[1]+i*win[3])+5,505-100*(win[0]+i*win[2]),100*(win[1]+i*win[3])+105,605-100*(win[0]+i*win[2]), outline= "blue", width= 7)

    

    def minimax_turn(self):
	if self.last_piece!= None:
	    self.board.itemconfig(self.last_piece, outline= "black", width= 1) 
	player= minimax.MinimaxPlayer(playernum=self.turn, ply_depth=int(self.spinner.get()), utility=utility.WithColumnUtility(5, 10, [1, 2, 3, 4, 3, 2, 1]))
        root = minimax.MinimaxNode.init_root(self.b, self.turn)
        childval = player.minimax(root, 0)
        for child in root.children:
            if child.get_minimax_value() == childval:
		col= child.from_parent_column
		y=0 
		while self.b.board[y][col]!= None:
		    y+=1
                self.b.play_turn(self.turn, col)
		if self.turn== 1: 
	    	    self.last_piece= self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "red", outline= "green", width= 5)
	    	    self.turn=2
		elif self.turn==2:
	    	    self.last_piece=self.board.create_oval(100*col+5,505-100*y,100*col+105,605-100*y, fill= "yellow", outline= "green", width= 5) 
		    self.turn=1
	        if self.b.is_game_over()!= None:
	            win= self.b.is_game_over()
		    for i in range(4):
   		        self.board.create_oval(100*(win[1]+i*win[3])+5,505-100*(win[0]+i*win[2]),100*(win[1]+i*win[3])+105,605-100*(win[0]+i*win[2]), outline= "blue", width= 7)
	        return
	

    def play_game(self):
	self.board.delete(ALL)
	self.b= connectfour.ConnectFour()
	self.turn= 1 
	self.last_piece= None
	for x in range(7):
	    self.board.create_line(5, x*100+5, 705,x*100+5)
	for x in range(8):    
	    self.board.create_line(x*100+5, 5, x*100+5, 605)	
	self.p1= self.combobox.get()
	self.p2= self.combobox1.get()	
	assert self.p1 and self.p2 != None   
	assert self.p1 or self.p2== "Human" 
	if self.p1== "Human":
	    pass
	elif self.p1== "Random": 
	    self.random_turn()
	elif self.p1== "Minimax":
	    self.minimax_turn()
	
	    
	        
	
root= Tk()
ConnectGui(root) 
root.mainloop()
