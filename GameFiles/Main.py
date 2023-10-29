# Imports
import arcade 
import os

#Global Const
SCREEN_TITLE = "The Kings Game"

ROW_COUNT = 8
COLUMN_COUNT = 8

#the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# the margin between each cell and on the edges of the screen.
MARGIN = 1

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

SPRITE_SCALING_PIECES = 0.1

class Piece(arcade.Sprite): # A class that contains the Information on a Chess Piece
    def __init__(self, Team, Type, scale= 0.1):
        self.team = Team
        self.type = Type
        self.image = f"GameFiles/Piece_Images/{self.team}{self.type}.png"
        # Call the parent
        super().__init__(self.image, scale,)

    def Pawn_Promote(self, New_Type):
        if self.type == "Pawn":
            print(New_Type)
            self.type = New_Type
            print(self.type)
            self.image = f"GameFiles/Piece_Images/{self.team}{self.type}.png"
            print(self.image)
        super().__init__(self.image, 0.1)

class ChessGame(arcade.Window): # The Main application class for the game.

    def __init__(self, width, height, title): # The Initializer

        # Call the parent class initializer
        super().__init__(width, height, title)

        #Controls which Players Turn it is 
        self.Player_Turn = "White"
        self.Turn_Number = 1
        self.King_check = None #Notes if a King is in Check or Check mate

        self.Selected_Piece = ["None", "None"]
        self.Piece_Position = []

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()
        #Two dimensional spirites List
        self.grid_sprites = []

        # Variables that will hold sprite lists for the pieces
        self.White_player_list = arcade.SpriteList()
        self.Black_player_list = arcade.SpriteList()

        # Background image 
        self.background = None
        self.background_color = arcade.color.BLACK


        #The Sound files
        self.OpeningSound = arcade.Sound("GameFiles/Sound_Files/Board_Opening.mp3")
        self.MoveSound = arcade.Sound("GameFiles/Sound_Files/Piece_Move.mp3")
        self.CaptureSound = arcade.Sound("GameFiles/Sound_Files/Piece_Lost.mp3")
        self.DefeatSound = arcade.Sound("GameFiles/Sound_Files/King_Lost.mp3")
        


        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                if (row % 2 != 0):
                    if(column % 2 == 0):
                        sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.ANTIQUE_BRASS)
                    else:
                        sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.ANTIQUE_WHITE)
                else:
                    if(column % 2 == 0):
                        sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.ANTIQUE_WHITE)
                    else:
                        sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.ANTIQUE_BRASS)
                    
                
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)
        self.setup()

    def Color_Check(self,row,column):
        if ((row + 2) % 2 != 0):
            if((column + 2) % 2 != 0):
                return "White"
        else:
            if((column + 2) % 2 == 0):
                return "White"
        return "Brass"

    def play(self, sound):
        if sound == 1: 
            self.OpeningSound.play()
        elif sound == 2: 
            self.MoveSound.play()
        elif sound == 3: 
            self.CaptureSound.play()
        elif sound == 4: 
            self.DefeatSound.play()

    def setup(self):
        # Set up the Black Pawn Pieces
        for column in range(COLUMN_COUNT):
            x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
            y = 6 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
            B_Pawn = Piece("Black", "Pawn", SPRITE_SCALING_PIECES)
            B_Pawn.center_x = x
            B_Pawn.center_y = y
            self.Black_player_list.append(B_Pawn)

        # Set up the White Pawn Pieces
        for column in range(COLUMN_COUNT):
            x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
            y = 1 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
            W_Pawn = Piece("White", "Pawn", SPRITE_SCALING_PIECES)

            W_Pawn.center_x = x
            W_Pawn.center_y = y
            self.White_player_list.append(W_Pawn)

        #Set Up the Black Rooks
        B_Rook= Piece("Black", "Rook", SPRITE_SCALING_PIECES)
        B_Rook.center_x = 0 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Rook.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Rook)
        B_Rook2 = Piece("Black", "Rook", SPRITE_SCALING_PIECES)
        B_Rook2.center_x = 7 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Rook2.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Rook2)

        #Set Up the White Rooks
        W_Rook = Piece("White", "Rook", SPRITE_SCALING_PIECES)
        W_Rook.center_x = 0 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Rook.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Rook)
        W_Rook2 = Piece("White", "Rook", SPRITE_SCALING_PIECES)
        W_Rook2.center_x = 7 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Rook2.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Rook2)

        #Set Up the Black Knights
        B_Knight= Piece("Black", "Knight", SPRITE_SCALING_PIECES)
        B_Knight.center_x = 1 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Knight.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Knight)
        B_Knight2= Piece("Black", "Knight", SPRITE_SCALING_PIECES)
        B_Knight2.center_x = 6 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Knight2.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Knight2)

        #Set Up the White Knights
        W_Knight = Piece("White", "Knight", SPRITE_SCALING_PIECES)
        W_Knight.center_x = 1 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Knight.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Knight)
        W_Knight2 = Piece("White", "Knight", SPRITE_SCALING_PIECES)
        W_Knight2.center_x = 6 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Knight2.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Knight2)

        #Set Up the Black Bishops
        B_Bishop = Piece("Black", "Bishop", SPRITE_SCALING_PIECES)
        B_Bishop.center_x = 2 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Bishop.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Bishop)
        B_Bishop2 = Piece("Black", "Bishop", SPRITE_SCALING_PIECES)
        B_Bishop2.center_x = 5 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Bishop2.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Bishop2)

        #Set Up the White Bishops
        W_Bishop = Piece("White", "Bishop", SPRITE_SCALING_PIECES)
        W_Bishop.center_x = 2 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Bishop.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Bishop)
        W_Bishop2 = Piece("White", "Bishop", SPRITE_SCALING_PIECES)
        W_Bishop2.center_x = 5 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Bishop2.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Bishop2)

        #Set Up the Black Queen
        B_Queen = Piece("Black", "Queen", SPRITE_SCALING_PIECES)
        B_Queen.center_x = 3 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_Queen.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_Queen)

        #Set Up the White Queen
        W_Queen = Piece("White", "Queen", SPRITE_SCALING_PIECES)
        W_Queen.center_x = 3 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_Queen.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_Queen)

        #Set Up the Black King
        B_King = Piece("Black", "King", SPRITE_SCALING_PIECES)
        B_King.center_x = 4 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        B_King.center_y = 7 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.Black_player_list.append(B_King)

        #Set Up the White King
        W_King =  Piece("White", "King", SPRITE_SCALING_PIECES)
        W_King.center_x = 4 * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        W_King.center_y = 0 * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
        self.White_player_list.append(W_King)
        self.play(1)

    def on_resize(self, width, height):
        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

    def on_draw(self): #Render the  Board
        # We should always start by clearing the window pixels
        self.clear()

        # Batch draw the grid sprites
        self.grid_sprite_list.draw()
        self.Black_player_list.draw()
        self.White_player_list.draw()
    #def update(self):

    def on_update(self, delta_time):
        #self.grid_sprite_list.update()
        self.Black_player_list.update()
        self.White_player_list.update()
        if self.Selected_Piece[0] != "None":
            self.Selected_Piece[0][0].update()
    def on_key_press(self, symbol, modifiers):
       if symbol == arcade.key.Q:
           return "Queen"
       if symbol == arcade.key.K:
           return "Knight"
       if symbol == arcade.key.B:
           return "Bishop"
       if symbol == arcade.key.R:
           return "Rook"

    def Check_Rook(self, initial_Row, New_Row, initial_Column, New_Column):
        if(initial_Column == New_Column):
            i = initial_Row
            n = New_Row
            if n > i:
                while (i < (n-1)):  # Check to see if their is piece blocking the way
                    #TODO check to see if piece one further prevents move
                    i += 1
                    Block = arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)),((i + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                    if len(Block) > 0: 
                        return False
                    Block = arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)),((i + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                    if len(Block) > 0: 
                        return False
            elif i > n: # Check to see if their is piece blocking the way
                while (i > (n +1)):
                    i -= 1
                    Block = arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)),((i + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                    if len(Block) > 0: 
                        return False
                    Block = arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)),((i + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                    if len(Block) > 0: 
                        return False
            return True
        elif(initial_Row == New_Row):
            print("Attempting Horizontal Movement")
            i = initial_Column
            n = New_Column
            if n > i:
                print("H1 Flag")
                while (i < (n - 1)):  # Check to see if their is piece blocking the way
                    #TODO check to see if piece one further prevents move
                    i += 1
                    Block = arcade.get_sprites_at_point((((i + 0.5) * (WIDTH + MARGIN)),((New_Row + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                    if len(Block) > 0:
                        print("White Piece Flag") 
                        return False
                    Block = arcade.get_sprites_at_point((((i + 0.5) * (WIDTH + MARGIN)),((New_Row + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                    if len(Block) > 0: 
                        print("Black Piece Flag")
                        return False
                return True
            elif i > n: # Check to see if their is piece blocking the way
                print("H2 Flag")
                while (i > (n +1)):
                    i -= 1
                    Block = arcade.get_sprites_at_point((((i + 0.5) * (WIDTH + MARGIN)),((New_Row + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                    if len(Block) > 0: 
                        print("White Piece Flag") 
                        return False
                    Block = arcade.get_sprites_at_point((((i + 0.5) * (WIDTH + MARGIN)),((New_Row + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                    if len(Block) > 0: 
                        print("Black Piece Flag")
                        return False
                return True
        else:
            print("failed Flag")
            return False
        
    

    def Check_Bishop(self, initial_Row, New_Row, initial_Column, New_Column):
        dx = abs(New_Column - initial_Column)
        dy = abs(New_Row - initial_Row)
        r = initial_Row
        c = initial_Column
        if((New_Column - initial_Column) >= 1 and (New_Row - initial_Row) >= 1): 
            while(c < (New_Column -1) and r < (New_Row - 1)):
                c += 1
                r += 1 
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                if len(Block) > 0: 
                    return False
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                if len(Block) > 0: 
                    return False
        if((New_Column - initial_Column) >= 1 and (New_Row - initial_Row) < 1): 
            while(c < (New_Column - 1) and r > (New_Row +1)):
                c += 1
                r -= 1 
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                if len(Block) > 0: 
                    return False
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                if len(Block) > 0: 
                    return False
        if((New_Column - initial_Column) < 1 and (New_Row - initial_Row) >= 1): 
            while(c > (New_Column + 1) and r < (New_Row - 1)):
                c -= 1
                r += 1 
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                if len(Block) > 0: 
                    return False
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                if len(Block) > 0: 
                    return False
        if((New_Column - initial_Column) < 1 and (New_Row - initial_Row) < 1): 
            while(c > (New_Column + 1) and r > (New_Row - 1)):
                c -= 1
                r -= 1 
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.White_player_list)
                if len(Block) > 0: 
                    return False
                Block = arcade.get_sprites_at_point((((c + 0.5) * (WIDTH + MARGIN)),((r + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)
                if len(Block) > 0: 
                    return False               
        if (dx == dy) and (dx > 0):
            return True
        else:
            return False







    def Show_Viable_Moves(self, row, column):
        C_check = self.Color_Check(row,column) 
        if (self.Player_Turn == "White" and self.Selected_Piece[0][0].type == "Pawn"): #check for which pawn is being moved to determine direction
            if (C_check == "White"):
                if (row == 1):
                    #self.grid_sprites[row + 1][column].color = (205, 149, 117, 200) #Brown Space
                    #self.grid_sprites[row + 2][column].color = 	(250, 235, 215, 200) #White space
                    return
                else: 
                    #self.grid_sprites[row + 1][column].color = (205, 149, 117, 200) #Brown Space  
                    return                  
        #     elif (C_check == "Brass"):
        #         if (row == 1):
        #             self.grid_sprites[row + 1][column].color = (250, 235, 215, 200) #White space
        #             self.grid_sprites[row + 2][column].color = (205, 149, 117, 200) #Brown Space
        #         else: 
        #             self.grid_sprites[row + 1][column].color = (250, 235, 215, 200) #White space

        # elif self.Player_Turn == "Black" and self.Selected_Piece[0][0].type == "Pawn": #check for which pawn is being moved to determine direction
        #     if (C_check == "White"):
        #         if (row == 6): 
        #             self.grid_sprites[row - 1][column].color = (205, 149, 117, 200) #Brown Space	
        #             self.grid_sprites[row - 2][column].color = (250, 235, 215, 200) #White space
        #         else:
        #             self.grid_sprites[row - 1][column].color = (205, 149, 117, 200) #Brown Space
        #     elif (C_check == "Brass"):
        #         if (row == 6):
        #             self.grid_sprites[row - 1][column].color = 	(250, 235, 215, 200) #White space
        #             self.grid_sprites[row - 2][column].color = 	(205, 149, 117, 200) #Brown Space
        #         else:
        #             self.grid_sprites[row - 1][column].color = 	(250, 235, 215, 200) #White space



    def Check_Viable_Move(self, New_Column, New_Row, x, y):
        initial_Row = self.Selected_Piece[0][0].center_y // (HEIGHT + MARGIN)
        initial_Column = self.Selected_Piece[0][0].center_x // (HEIGHT + MARGIN)
        if self.Player_Turn == "White":
            allies = arcade.get_sprites_at_point((x, y), self.White_player_list)
            if len(allies) > 0:
                return False
        elif self.Player_Turn == "Black":
            allies = arcade.get_sprites_at_point((x, y), self.Black_player_list)
            if len(allies) > 0:
                return False

        if self.Selected_Piece[0][0].type == "Pawn":
            if self.Player_Turn == "White":
                #CHECK TO SEE IF THEIR IS PIECE IN THE WAY OF MOVEMENT
                White_P = arcade.get_sprites_at_point((((initial_Column + 0.5) * (WIDTH + MARGIN)), ((initial_Row + 1.5) * (WIDTH + MARGIN))), self.White_player_list)
                Black_P = arcade.get_sprites_at_point((((initial_Column + 0.5) * (WIDTH + MARGIN)), ((initial_Row + 1.5) * (WIDTH + MARGIN))), self.Black_player_list)
                if(initial_Row == 1):
                    if (initial_Column == New_Column and New_Row > initial_Row and (New_Row - initial_Row) <= 2):
                        if(len(Black_P) <= 0 and len(White_P) <= 0):
                            if(len(arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)), ((New_Row + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)) <= 0):
                                return True
                            else:
                                return False 
                        else:
                            return False
                    else:
                        return False
                elif initial_Column == New_Column: # are they moving straight ?
                    if (initial_Column == New_Column and New_Row > initial_Row and (New_Row - initial_Row) == 1 and len(Black_P) <= 0):
                        return True 
                    else:
                        return False
                elif ((initial_Column +1) == New_Column or (initial_Column - 1) == New_Column): # check to see if pawn moved diagonal
                    if (initial_Row + 1 == New_Row): #make sure the white pawn is only moving forward
                        if len(arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)), ((New_Row + 0.5) * (WIDTH + MARGIN))), self.Black_player_list)) > 0: #check to make sure there is a piece to capture
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
                
                    
            elif self.Player_Turn == "Black":
                #CHECK TO SEE IF THEIR IS PIECE IN THE WAY OF MOVEMENT
                White_P = arcade.get_sprites_at_point((((initial_Column + 0.5) * (WIDTH + MARGIN)), ((initial_Row - 1.5) * (WIDTH + MARGIN))), self.White_player_list)
                Black_P = arcade.get_sprites_at_point((((initial_Column + 0.5) * (WIDTH + MARGIN)), ((initial_Row - 1.5) * (WIDTH + MARGIN))), self.Black_player_list)

                if(initial_Row == 6):
                    if (initial_Column == New_Column and New_Row < initial_Row and (initial_Row - New_Row) <= 2):
                        if(len(Black_P) <= 0 and len(White_P) <= 0):
                            if(len(arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)), ((New_Row + 0.5) * (WIDTH + MARGIN))), self.White_player_list)) <= 0): #make sure there is no piece occupying this space as pawns cannot capture vertically
                                return True
                            else:
                                return False 
                        else:
                            return False
                    else:
                        return False
                elif(initial_Column == New_Column): # are they moving straight ?
                    if (initial_Column == New_Column and New_Row < initial_Row and (initial_Row - New_Row) == 1):
                        return True 
                    else:
                        return False
                elif ((initial_Column +1) == New_Column or (initial_Column - 1) == New_Column): # check to see if pawn moved diagonal
                    if (initial_Row - 1 == New_Row): #make sure that Black pawns only move Downward
                        if len(arcade.get_sprites_at_point((((New_Column + 0.5) * (WIDTH + MARGIN)), ((New_Row + 0.5) * (WIDTH + MARGIN))), self.White_player_list)) > 0: #check to make sure there is a piece to capture
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
                

        if self.Selected_Piece[0][0].type == "Rook":
            return self.Check_Rook(initial_Row, New_Row, initial_Column, New_Column)
            

        elif self.Selected_Piece[0][0].type == "Knight":
            if(((initial_Column + 1) == New_Column and (initial_Row + 2) == New_Row) or ((initial_Column - 1) == New_Column and (initial_Row + 2) == New_Row)):
                return True
            elif(((initial_Column + 2) == New_Column and (initial_Row + 1) == New_Row) or ((initial_Column - 2) == New_Column and (initial_Row + 1) == New_Row)):
                return True
            elif(((initial_Column + 2) == New_Column and (initial_Row - 1) == New_Row) or ((initial_Column - 2) == New_Column and (initial_Row - 1) == New_Row)):
                return True
            elif(((initial_Column + 1) == New_Column and (initial_Row - 2) == New_Row) or ((initial_Column - 1) == New_Column and (initial_Row - 2) == New_Row)):
                return True
            else:
                return False  


        elif self.Selected_Piece[0][0].type == "Bishop":
            return self.Check_Bishop(initial_Row, New_Row, initial_Column, New_Column)
            

        elif self.Selected_Piece[0][0].type == "Queen":
            if (abs(New_Column - initial_Column) <= 1  and abs(New_Row - initial_Row) <= 1): #moves only a single spaces so there is nothing to get in its way
                return True
            elif ((abs(New_Column - initial_Column) == abs(New_Row - initial_Row)) and abs(New_Column - initial_Column) > 0):
                if self.Check_Bishop(initial_Row, New_Row, initial_Column, New_Column) == True:
                    return True
            elif(initial_Column == New_Column): 
                if self.Check_Rook(initial_Row, New_Row, initial_Column, New_Column) == True:
                    return True
            elif(initial_Row == New_Row):
                if self.Check_Rook(initial_Row, New_Row, initial_Column, New_Column) == True:
                    return True
            else: 
                return False
            

        elif self.Selected_Piece[0][0].type == "King":
            if (abs(New_Row - initial_Row) <= 1 and abs(New_Column - initial_Column) <= 1):
                return True
            else:
                return False
            

    def on_mouse_press(self, x, y, button, modifiers): # Called when the user presses a mouse button.
 
        # Convert the clicked mouse position into the appropriate grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        
        # Validate the selected coordinates
        if row >= ROW_COUNT or column >= COLUMN_COUNT: # IS it on the board
            return
        if (self.Selected_Piece[0] == "None"):        
            if self.Player_Turn == "White": # Check who's turn it is 
                Piece = arcade.get_sprites_at_point((x, y), self.White_player_list) #Get the Pieces we've clicked on
                if len(Piece) > 0: # Validate that a piece has been clicked
                    self.Selected_Piece[0] = Piece
                    #self.Piece_Position = [self.Selected_Piece[0].center_x , self.Selected_Piece[0].center_y]
            elif self.Player_Turn == "Black": # Check who's turn it is  
                Piece = arcade.get_sprites_at_point((x, y), self.Black_player_list) #Get the Pieces we've clicked on
                if len(Piece) > 0: # Validate that a piece has been clicked
                    self.Selected_Piece[0] = Piece
                    #self.Piece_Position = [self.Selected_Piece[0].center_x , self.Selected_Piece[0].center_y]
            self.Show_Viable_Moves(row, column) #Show Viable Moves of piece
            return
        
        elif (self.Selected_Piece[0] != "None"):
            if self.Player_Turn == "White": 
                if (len(arcade.get_sprites_at_point((x, y), self.White_player_list)) > 0 ): #check to see if there is already a ally piece on that square
                    return
            elif self.Player_Turn == "Black":
                if (len(arcade.get_sprites_at_point((x, y), self.Black_player_list)) > 0 ): #check to see if there is already a ally piece on that square
                    return

            if self.Check_Viable_Move(column, row, x, y) == True:
                sound_Cap = 0 
                if (self.Selected_Piece[0][0].center_x != ((column + 0.5) * (WIDTH + MARGIN)) or self.Selected_Piece[0][0].center_y != ((row + 0.5) * (WIDTH + MARGIN))):  #Check to see if the selected position is different from initial position
                    if self.Player_Turn == "White": 
                        for enemy in self.Black_player_list: # check to see if there is piece to be captured
                            if ((enemy.center_x // (WIDTH + MARGIN))==  column and (enemy.center_y // (HEIGHT + MARGIN)) == row):
                                if enemy.type == "King":
                                    self.King_check = "WhiteWins"
                                enemy.remove_from_sprite_lists()
                                if enemy.type == "King":
                                   sound_Cap = 1
                                   self.play(4)
                                else: 
                                    sound_Cap = 1
                                    self.play(3)
                    if self.Player_Turn == "Black": 
                        for enemy in self.White_player_list: # check to see if there is piece to be captured
                            if ((enemy.center_x // (WIDTH + MARGIN))==  column and (enemy.center_y // (HEIGHT + MARGIN)) == row):
                                if enemy.type == "King":
                                    self.King_check = "BlackWins"
                                enemy.remove_from_sprite_lists()
                                if enemy.type == "King":
                                   sound_Cap = 1
                                   self.play(4)
                                else: 
                                    sound_Cap = 1
                                    self.play(3)
                    if sound_Cap == 0:
                        self.play(2)
                    self.Selected_Piece[0][0].center_x = ((column + 0.5) * (WIDTH + MARGIN))
                    self.Selected_Piece[0][0].center_y = ((row + 0.5) * (WIDTH + MARGIN))
                    if self.Player_Turn == "White": 
                        if row == 7:
                            if (self.Selected_Piece[0][0].type == "Pawn"):
                                #x = self.on_key_press()
                                self.Selected_Piece[0][0].type = "Queen"
                                v = f"GameFiles/Piece_Images/{self.Selected_Piece[0][0].team}{self.Selected_Piece[0][0].type}.png"
                                self.Selected_Piece[0][0].image = f"GameFiles/Piece_Images/{self.Selected_Piece[0][0].team}{self.Selected_Piece[0][0].type}.png"                
                                print("Pawn Promoted")
                     
                            
                            
                                #TODO Complete Pawn Promotion Method            

                    self.Selected_Piece = ["None", "None"]
                    if(self.Player_Turn == "White"):
                        self.Player_Turn = "Black"
                    elif(self.Player_Turn == "Black"):
                        self.Player_Turn = "White"
                    else:
                        print("There was an Error changing Turns")
        if self.King_check == "WhiteWins":
            print("white wins")
            message = arcade.draw_text("White has Won",0, 0, arcade.color.BLACK, 20, font_name="Kenney Future")
            #self.grid_sprite_list.append(message)
            arcade.close_window()

        elif self.King_check == "BlackWins":
            message = arcade.draw_text("Black has Won",200, 200, arcade.color.BLACK, 80, font_name="Kenney Future")
            #self.grid_sprite_list.append(message)
            arcade.close_window()



def main():
    ChessGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()




#TODO Add forced Check and Checkmate Functions