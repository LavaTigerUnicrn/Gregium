"""
Gambling
"""

import random

class Gambler:

    def __init__(self,chips:int=10,luck=0):
        """A gambler that can communicate with GameInst's to bet chips on it
        
        Args:
            chips:
                Starting chips
            luck:
                Starting luck (0-100)
                """
        self._chips = chips
        self._luck = max(min(luck,100),0)

    @property
    def luck(self):
        return self._luck
    
    @luck.setter
    def luck(self,value:int):
        assert type(value) == int
        self._luck = max(min(value,100),0)

class GameBase:

    def __init__(self):
        """Base class for all gambling games"""

        self._casino = None
        self._id = -1
        self._wins = 0
        self._losses = 0

    def generate(self,gambler:Gambler):
        """Generates new game inst based on current game settings"""
        ...

    def _register(self,casino,id:int):

        self._casino = casino
        self._id = id

class GameInst:

    def __init__(self,parent:GameBase,player:Gambler,bet:int):
        """Base class for allgambling game instances"""

        self._parent = parent
        self._player = player
        self._bet = bet
        player._chips -= bet
        self._isRunning = True

    def play(self,inputs:dict[str,str]):
        """Runs a game based on inputs
        
        Args:
            inputs:
                Inputs to the game, differs based on each game"""
        ...

    def report_win(self):
        self._parent._wins += 1
    def report_loss(self):
        self._parent._losses += 1
class Casino:

    def __init__(self,bank:int=100):
        """
        A casino base capable of monitoring losses per table, dealing out chips, and more
        Tables can be registered by doing .register(table)
        
        Args:
            bank:
                The starting number of chips in the casino (-1 gives infinite)
        """

        self._chips = bank
        self._tables = {}
        self._maxTables = 10
        self._tableId = 0

    def register(self,table:GameBase):
        """
        Registers given table to casino for tracking,
        will assign a unique id to the table

        Args:
            table:
                The generated table class
        """
        
        table._register(self,self._tableId)
        self._tables[self._tableId] = {"table":table}

        self._tableId += 1

    def __str__(self):

        rtrn = f"-- Casino --\n Chips: {self._chips}\n- Tables -\n"
        for tableId in self._tables:
            
            table = self._tables[tableId]
            rtrn += f" {tableId}: {table["table"].__class__.__name__} - Stats\n  Casino Wins: {table["table"]._wins}\n  Casino Losses: {table["table"]._losses}"

        return rtrn
        
class BlackjackInst(GameInst):

    def __init__(self,parent:GameBase,player:Gambler,bet:int):
        """
        Created by BlackJack table
        """

        self._state = {"dealer":random.randint(2,11),
                       "dealerInvis":random.randint(1,10),
                       "player":random.randint(2,11)+random.randint(1,10),
                       "isFirstTurn":True}

        super().__init__(parent=parent,player=player,bet=bet)

    def _dealerPlay(self):

        dealerPlaying = True
        self._state["dealer"] += self._state["dealerInvis"]
        self._state["dealerInvis"] = 0

        while dealerPlaying:

            if self._state["dealer"] < self._state["player"]:
                self._state["dealer"] += random.randint(1,11 if self._state["dealer"] < 11 else 10)

            if self._state["dealer"] > 21:
                self._isRunning = False
                self._player._chips += self._bet * 2
                self.report_loss()
                return "Dealer Bust"
            
            elif self._state["dealer"] == self._state["player"]:
                self._isRunning = False
                self._player._chips += self._bet
                return "Tie"
            
            elif self._state["dealer"] > self._state["player"]:
                self._isRunning = False
                self.report_win()
                return f"Dealer Win ({self._state["dealer"]})"
            
    def play(self,inputs:dict[str,str]):
        """
        Runs a game based on inputs
        
        Args:
            inputs:
                Inputs to the game, MUST follow dictionary of
                "move":"hit"/"stand"
                """
        
        if self._isRunning:
            
            if self._state["isFirstTurn"]:
                if self._state["dealer"]+self._state["dealerInvis"] == 21:
                    self._isRunning = False
                    self._state["dealer"] = 21
                    self.report_win()
                    return "Dealer Blackjack"
                if self._state["player"] == 21:
                    self._isRunning = False
                    self._player._chips += self._bet * 2.5
                    self.report_loss()
                    return "Blackjack"
                self._state["isFirstTurn"] = False
            if inputs["move"] == "hit" and self._state["player"]:
                if self._state["player"] == 21:
                    return "You already have 21"
                
                if self._player._luck > random.randint(0,99):
                    self._state["player"] += random.randint(1,21-self._state["player"])

                else:
                    self._state["player"] += random.randint(1,11 if self._state["player"] < 11 else 10)

                if self._state["player"] > 21:
                    self._isRunning = False
                    self.report_win()
                    return "Bust"
                
                elif self._state["player"] == 21:

                    return self._dealerPlay()
                
                return ""
                
            elif inputs["move"] == "stand":
                
                return self._dealerPlay()
            
            else:
                
                return "Valid moves include: hit, stand"


        else:
            return "Game is over"
        
    def __str__(self):
        return f"Dealer: {self._state["dealer"]}\nPlayer: {self._state["player"]}"

class Blackjack(GameBase):

    def __init__(self):
        """
        A Blackjack table for gambling
        """

        super().__init__()

    def generate(self,player:Gambler,bet:int):
        assert bet > 0 and player._chips >= bet

        return BlackjackInst(parent=self,player=player,bet=bet)