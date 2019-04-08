# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam,settings
from soccersimulator import VolleySimulation, volley_show_simu
from moduleH.tools import SupState
class Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)  
        if sup.autor_terrain():
            if sup.can_shoot():
                return SoccerAction( shoot = (sup.adv_players_pos[0] - sup.my_position)*2000)
            return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position))        
        else: 
            
                if sup.sens==-1:
                    if sup.my_position.y>settings.GAME_HEIGHT/2:
                        return  SoccerAction(acceleration= (Vector2D(7*settings.GAME_WIDTH/8,settings.GAME_HEIGHT/4)-sup.my_position)*2000)
                    else:
                        return  SoccerAction( acceleration = (Vector2D(7*settings.GAME_WIDTH/8,3*settings.GAME_HEIGHT/4)-sup.my_position)*2000)    
                else:
                     if sup.my_position.y>settings.GAME_HEIGHT/2:
                        return  SoccerAction( acceleration=( Vector2D(settings.GAME_WIDTH/8,settings.GAME_HEIGHT/4)-sup.my_position)*2000)
                     else:
                        return  SoccerAction(acceleration =( Vector2D(settings.GAME_WIDTH/8,3*settings.GAME_HEIGHT/4)-sup.my_position)*2000)





# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("attaq", Defense())  # Random strategy
team2.add("DEF", Defense())   # Random strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)
