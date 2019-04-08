    #from "notre dossier" import "nos strategies"

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from soccersimulator import Simulation, show_simu
from moduleH import get_team
if __name__ == '__main__':
   
    
    #Test avec 1 et 2 joueurs
    team1 = get_team(1)
    team2 = get_team(1)
    
    # Create a match 
    simulation1 = Simulation(team2,team1)
    
    # Simulate and display the match
    volley_show_simu(simulation1)
    
    #Deuxieme simulation 2 vs 2 
    #team2_2 = get_team(2)
    
    #Lancement de la simulation 
    #simulation2 = Simulation(team2,team2_2)
    #show_simu(simulation2)
