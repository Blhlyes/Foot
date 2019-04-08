# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam,settings
from soccersimulator import VolleySimulation, volley_show_simu
from moduleH.tools import SupState


class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Echauffement")

    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)
        
        if sup.can_shoot():
            return SoccerAction( shoot = (sup.adv_players_pos[0] - sup.my_position)*2000)
     
        elif sup.autor_terrain():
            return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position))
        else:
            return SoccerAction(acceleration = (Vector2D(settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)if sup.sens == 1 else Vector2D(3*settings.GAME_WIDTH/4,settings.GAME_HEIGHT/2)) - sup.my_position)




# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Player 1", Echauffement())  # Random strategy
team2.add("Player 2", Echauffement())   # Random strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)
