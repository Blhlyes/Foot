# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam,settings
from soccersimulator import VolleySimulation, volley_show_simu
from moduleH.tools import SupState
from volleyball_question3 import Defense


class Multi(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)  
        if sup.dist_fil()<settings.GAME_WIDTH/4:
          if sup.dist_fil()>10 and sup.can_shoot():
                    return SoccerAction(shoot=(sup.centre()-sup.my_position)*0.5,acceleration=(sup.predict_ball()-sup.my_position))
        
          elif sup.can_shoot():
                if sup.sens==1:
                    if sup.adv_players_pos[0].y>settings.GAME_HEIGHT/2:
                        return  SoccerAction( shoot = (Vector2D(7*settings.GAME_WIDTH/8,settings.GAME_HEIGHT/4)-sup.my_position)*1000)
                    else:
                        return  SoccerAction( shoot = (Vector2D(7*settings.GAME_WIDTH/8,3*settings.GAME_HEIGHT/4)-sup.my_position)*1000)    
                else:
                     if sup.adv_players_pos[0].y>settings.GAME_HEIGHT/2:
                        return  SoccerAction( shoot =( Vector2D(settings.GAME_WIDTH/8,settings.GAME_HEIGHT/4)-sup.my_position)*1000)
                     else:
                        return  SoccerAction( shoot =( Vector2D(settings.GAME_WIDTH/8,3*settings.GAME_HEIGHT/4)-sup.my_position)*1000)
          elif sup.autor_terrain():
                return  SoccerAction(acceleration = sup.predict_ball() - sup.my_position)
          else:
                return SoccerAction(acceleration = (Vector2D(settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)if sup.sens == 1 else Vector2D(3*settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)) - sup.my_position)
    
        else:
                   if sup.can_shoot():
                    return SoccerAction( shoot = (sup.adv_players_pos[0] - sup.my_position)*2000)
             
                   elif sup.autor_terrain():
                    return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position))
                   else:
                    return SoccerAction(acceleration = (Vector2D(settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)if sup.sens == 1 else Vector2D(3*settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)) - sup.my_position)


       

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add playersandom 
team1.add("Attaquant", Multi())  # Random
team2.add("Defenseur", Defense())   # Random strategy
team1.add("Attaquant", Multi())  # Random
team2.add("Defenseur", Defense())   # Random strategy


# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)


