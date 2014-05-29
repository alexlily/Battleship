import Tkinter as tk

textfont = 'Times'
textsize= 14
bgcolor='white'

class Player(tk.Frame):
    def __init__(self, game, number):
        tk.Frame.__init__(self)
        self.game = game
        self.number = number
        self.placed = 0
        self.numboats = 0
        self.board = self.makeBoard() # will represent self's opponent's board; 
        #the one it's attacking.
        self.done = False
        self.pieces = -1
        self.destroyed = 0
    def __str__(self):
        return "player " + str(self.number)
    def makeBoard(self):
        array = []
        for i in range(10):
            array.append([])
        for j in array:
            for i in range(10):
                j.append(0)
        return array
    def print_board(self):        
        print 'The board for {0} so far:'.format(str(self))
        print ' | 0 1 2 3 4 5 6 7 8 9'
        print '-----------------------'
        count = 0
        for line in self.board: 
            print str(count) + '|',
            for char in line:
                print char,
            count += 1
            print ''  
    def fixbuttons(self, buttongrid,cmd):
        for x in range(10):
            for y in range(10):
                if ((cmd == 'attack' and self.board[x][y]=='x') or (cmd == 'setup' and self.board[x][y]==1)):
                    buttongrid[y][x].config(text=self.board[x][y])
                else:
                    buttongrid[y][x].config(text='  ')
    
    def take_turn(self, pos, labeltext,buttongrid):
        self.fixbuttons(buttongrid,'attack')
        x = int(pos[1])
        y = int(pos[0])
        if self.check_coord(x,y):
            #print 'Made a hit!'
            self.destroyed += 1
            hit = True
        else:
            #print 'Missed!'
            hit = False
        self.board[x][y] = 'x'
        self.fixbuttons(buttongrid,'attack')
        #self.print_board()
        
        if self.gameover():
            #print str(self)
            self.game.endGame(self)
        
        self.game.changePlayer()
        labeltext.set(str(self.game.player) + "\nclick to attack a spot.")
        t = tk.Toplevel(self)
        t.title("Switch Players")
        message = tk.StringVar()
        msg = tk.Message(t, textvariable=message, font = (textfont,textsize),bg=bgcolor)
        if hit:
            message.set("Hit! \n\n\nYour turn is over. Switch to next player.\n\n")
        else:
            message.set("Miss! \n\n\nYour turn is over. Switch to next player.\n\n")
        msg.pack()
        button = tk.Button(t, text="OK", 
                           command = lambda t = t: self.game.player.clearboard(t, buttongrid))
        button.pack()
        return
    def clearboard(self, t,buttongrid):
        t.destroy();
        
        self.fixbuttons(buttongrid,'attack')
    def check_coord(self,x,y):
        #print self.board[x][y]
        if self.board[x][y]== 1:
            return True
        else:
            return False
    def gameover(self):
        if self.destroyed == self.pieces:
            return True
        return False

    def check_fit(self, x,y,size,orientation):
        if orientation == 'horizontal':
          if y+size-1 > 9:
            print 'Boat does not fit there'
            return False
          for i in range(size):
            if self.board[x][y+i] == 1:
              print 'Cannot overlap boats'
              return False
        if orientation == 'vertical':
          if x+size-1 > 9:
            print 'Boat does not fit there'
            return False
          for i in range(size):
            if self.board[x+i][y] == 1:
              print 'Cannot overlap boats'
              return False
        return True


class BattleshipGame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)        
        self.orientation='horizontal'
        title=tk.PhotoImage(file="battleshipbanner.gif")
        titlelabel = tk.Label(self, image=title)
        titlelabel.photo = title
        titlelabel.pack()
        photo = tk.PhotoImage(file="shipline_color.gif")
        w = tk.Label(self, image=photo)
        w.photo = photo
        w.pack()        
        self.instr = tk.Button(self, text="Instructions", 
                                command=self.play)
        self.instr.pack(side="top")
        self.play = tk.Button(self, text="Play game",
                                 command=self.setup)
        self.play.pack(side="top")
        
        self.close = tk.Button(self,text="Quit",
                               command = lambda: self.closeall(self))
        self.close.pack(side="top")
        self.player0 = Player(self, 0)
        self.player1 = Player(self, 1)
        self.player = self.player0
        self.opponent = self.player1
    def clearall(self):
        self.orientation='horizontal'
        self.player0=Player(self,0)
        self.player1 = Player(self,1)
        self.player=self.player0
        self.opponent=self.player1
    def changePlayer(self,buttongrid=False):
        #if buttongrid:
        #    self.player.clearbuttons(buttongrid)
        self.player, self.opponent = self.opponent, self.player
        #if buttongrid:
        #    self.player.fixbuttons(buttongrid)
    def play(self):
        t = tk.Toplevel(self, bg = bgcolor)
        instructiontext = """
Battleship is a game where you try to sink the other person's ships.
Each player gets (up to) 5 ships that they place on a personal 10 by 10 gameboard at the beginning
After each player's ships are placed, players take turns entering coordinates that they'd like to shoot at
Whoever sinks all of the other person's ships first wins!
Start by setting pieces. Don't let your opponent see where you place your ships!
Player 0 aims first. Good luck! 
"""
        t.wm_title("Instructions")
        l = tk.Label(t, text=instructiontext, bg = bgcolor, font = (textfont,textsize))
        l.pack(side="top",fill="both", expand=True,padx=100,pady=10)
        close = tk.Button(t, text="close", command=lambda : self.closewindow(t))
        close.pack(side="top",padx=100,pady=10)
    def closeall(self, thing):
        thing.quit()
    def closewindow(self, container):
        container.destroy()
    def setShip(self, pos,labeltext,container,buttongrid):
        if self.opponent.placed <= self.opponent.numboats:
            if self.opponent.placed < self.opponent.numboats:
                self.place_piece(pos,self.boats[self.boatlist[self.opponent.placed]],buttongrid,labeltext) 
                if self.opponent.placed < self.opponent.numboats:
                    labeltext.set(self.placement_instructions())
            #self.opponent.print_board() 
        self.opponent.fixbuttons(buttongrid,'setup')
        if self.opponent.placed==self.opponent.numboats:
            self.opponent.done= True
            self.orientation = 'horizontal'  
            self.swapTurn(container)
    def place_piece(self, coords, size,buttongrid,labeltext):
        #if self.opponent.placed < self.opponent.numboats:
        #        labeltext.set(self.placement_instructions()) 
        
        x = int(coords[1])
        y = int(coords[0])
        if not (self.opponent.check_fit(x,y,size,self.orientation)):
            self.invalidCommand("Cannot put ship there.")
        else:
            if self.orientation == 'vertical':
                for i in range (size):
                    self.opponent.board[x+i][y]=1
            elif self.orientation == 'horizontal':
                for i in range (size):
                    self.opponent.board[x][y+i]=1 
            self.opponent.placed += 1
            self.opponent.fixbuttons(buttongrid,'setup')
        
    def setup(self):
        self.clearall()
        t = tk.Toplevel(self)
        t.wm_title("Set Up")
        frame = tk.Frame(t,height = 50, width=1000, bg = bgcolor)
        frame.grid()
        grid = tk.Frame(frame,bg=bgcolor)
        grid.grid(stick=tk.N)
        instr = tk.Label(grid, text="\nHow many boats do you want to play with?\n", 
                         bg = bgcolor, 
                         font = (textfont, textsize), padx = 20, pady=20)
        instr.grid(row=0,columnspan=5)
        for x in range(5):
            pos = str(x + 1)
            btn = pos
            btn = tk.Button(grid, text=btn, command=lambda num=pos:self.num_boats(num, t), bg=bgcolor)
            btn.grid(column=x,row=3)
        spacer = tk.Label(grid,text='\n',bg=bgcolor)
        spacer.grid(row=4)
        quitbtn = tk.Button(grid, text='quit', command=t.quit,bg=bgcolor)
        quitbtn.grid(row=5,column=2)
    def num_boats(self, num,container):
        if num == '5':
          self.boats = {'Aircraft Carrier':5, 'Battleship':4, 'Submarine':3, 'Cruiser': 3, 'Destroyer': 2}
        elif num == '4':
          self.boats =  {'Aircraft Carrier':5, 'Battleship':4, 'Submarine':3, 'Cruiser': 3}
        elif num == '3':
          self.boats = {'Aircraft Carrier':5, 'Battleship':4, 'Submarine':3}
        elif num == '2':
          self.boats = {'Aircraft Carrier':5, 'Battleship':4}
        elif num == '1':
          self.boats = {'Aircraft Carrier': 5}
        self.boatlist = self.boats.keys()
        self.player0.numboats = len(self.boatlist)
        self.player1.numboats = len(self.boatlist)
        self.player0.pieces = sum(self.boats.values())
        self.player1.pieces = sum(self.boats.values())
        self.set_gameboard()
        container.destroy()
    def placement_instructions(self):
        return "\n{3} \n\nPlace {0}\n({1} pieces)\n{2} orientation\n(press v for vertical, h for horizontal)".format(
            self.boatlist[self.opponent.placed], 
            str(self.boats[self.boatlist[self.opponent.placed]]), 
            self.orientation,
            self.player)
    def set_gameboard(self):
        buttongrid = [[x for x in range(10)] for i in range(10)]
        labeltext = tk.StringVar()
        labeltext.set(self.placement_instructions())            
        t = tk.Toplevel(self)
        t.wm_title("battlefield")
        frame = tk.Frame(t, width=1000,bg=bgcolor)
        frame.bind("<Key>", lambda event: self.setOrientation(frame, event,labeltext))
        frame.focus_set()
        frame.grid()
        grid=tk.Frame(frame,bg=bgcolor)
        grid.grid(stick=tk.N+tk.S+tk.E+tk.W, column=0,row=7,columnspan=3)
        labeltext = tk.StringVar()
        label= tk.Label(grid, textvariable=labeltext,bg=bgcolor)
        label.grid(row=0, rowspan=3, columnspan=10)   
        labeltext.set(self.placement_instructions())            
        for x in range(10):
            for y in range(10):
                pos = str(x)+str(y)
                btn = pos                
                btn = tk.Button(grid, text='  ', 
                                command=lambda xy=pos: self.setShip(xy, labeltext,t, buttongrid),
                                bg='blue')
                buttongrid[x][y] = btn
                btn.grid(column=x, row=y+3)
        label = tk.Label(grid, text='', height = 5,bg=bgcolor)
        label.grid(row=20)
        quitbutton = tk.Button(grid, text='quit',command=lambda:self.closeall(t),bg=bgcolor)
        quitbutton.grid(row=21, columnspan = 10)
    def setOrientation(self, frame, event, labeltext):
        #print "pressed", repr(event.char)
        if (event.char == 'h' or event.char == 'v'):
            if (event.char == 'h'):
                self.orientation = "horizontal"            
            else:
                self.orientation = "vertical"
            
            labeltext.set(self.placement_instructions())
            #print self.orientation
            #print self.placement_instructions
        else:
            self.invalidCommand("""Invalid orientation key. \nUse v for vertical placement \nand h for horizontal placement.\t\t""")
                
    def swapTurn(self, c2):
        t = tk.Toplevel(self,bg=bgcolor)
        t.title("Switch Players")
        msg = tk.Message(t, text="Your turn is over. Switch to next player.", 
                         width = 1000,
                         font = (textfont,textsize),
                         bg='white')
        msg.pack()
        button = tk.Button(t, text="OK", command = lambda c=c2: self.close_and_next(t,c))
        button.pack()
        self.changePlayer()
    def close_and_next(self, container1, container2):
        #print 'current player:', str(self.player)
        container1.destroy()
        container2.destroy()
        if not self.player0.done or not self.player1.done:            
            self.set_gameboard()
        else:
            self.popup()
        
    def attack(self, container):
        buttongrid = [[x for x in range(10)] for i in range(10)]
        container.destroy()
        t = tk.Toplevel(self)
        t.wm_title("battlefield")
        frame = tk.Frame(t, width=1000)
        frame.bind("<Key>", lambda event: self.setOrientation(frame, event,labeltext))
        frame.focus_set()
        frame.grid()
        grid=tk.Frame(frame)
        grid.grid(stick=tk.N+tk.S+tk.E+tk.W, column=0,row=7,columnspan=3)
        labeltext = tk.StringVar()
        label= tk.Label(grid, textvariable=labeltext)
        label.grid(row=0, rowspan=3, columnspan=10)   
        labeltext.set(str(self.player) + "\nclick to attack a spot.")
        buttontext= tk.StringVar()
        for x in range(10):
            for y in range(10):
                pos = str(x)+str(y)
                btn = pos
                btn = tk.Button(grid, text='  ',
                                command=lambda coords=pos: self.player.take_turn(coords, labeltext,buttongrid),
                                bg='blue')
                buttongrid[x][y]=btn
                btn.grid(column=x, row=y+3)
        label = tk.Label(grid, text=' ', height = 5)
        label.grid(row=20)
        quitbutton = tk.Button(grid, text='quit',command=lambda:self.closeall(t))
        quitbutton.grid(row=21, columnspan = 10)
        
        
    def popup(self):
        top = tk.Toplevel()
        top.title("Time to Play")
        photo = tk.PhotoImage(file="label1.gif")
        button=tk.Button(top, 
                         #text="\n\nClick here to begin\n(Player 0 goes first)\n\n",
                         command = lambda e=top:self.attack(top),
                         image = photo)
        button.photo=photo
        button.pack()
    def endGame(self, winner):
        player0win = tk.PhotoImage(file="P0win.gif")
        player1win = tk.PhotoImage(file="P1win.gif")
        if winner == self.player0:
            message = player0win
        else:
            message = player1win
        top = tk.Toplevel(bg=bgcolor)
        top.title("Game Over")
        msg = tk.Label(top, image=message)
        msg.image=message
        msg.pack()
        button = tk.Button(top, text="Quit", command=top.quit)
        button.pack() 
    def invalidCommand(self, message):
        top = tk.Toplevel()
        top.title("Invalid Command ")
        msg = tk.Message(top, text=message,width=50000,font=(textfont,textsize),bg='white')
        msg.pack()

        button = tk.Button(top, text="OK", command=top.destroy)
        button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    main = BattleshipGame(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
