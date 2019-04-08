from moduleH.strategies import Attaque,Echauffement,GardienStrategy,SoloStrategy4, SoloStrategy2, FonceurStrategy,DefenseStrategy, SoloStrategy
from soccersimulator import SoccerTeam


def get_team(nb_players):
    team = SoccerTeam(name="Strange's Team")
    if nb_players == 1:
        team.add("F",Attaque())
    if nb_players == 2:
        team.add("F",Echauffement())
        team.add("F",Attaque())
       
    if nb_players == 4:
        team.add("S",SoloStrategy2())
        team.add("###",DefenseStrategy())
        team.add("S2",SoloStrategy4())
        team.add("###",GardienStrategy())
    return team
