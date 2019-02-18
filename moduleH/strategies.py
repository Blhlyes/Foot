from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, settings
import math
from .tools import SupState
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
       	return SoccerAction(Vector2D.create_random(-1.,1.),Vector2D.create_random(-1.,1.))


"""class Defense(Strategy):
	def __init__(self, name="defense"):
		Strategy.__init__(self, name)
	def compute_strategy(self,state, idteam, idplayer):
"""

                                                                                                                                                  
class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
       	#return SoccerAction(Vector2D.create_random(-1.,1.),Vector2D.create_random(-1.,1.))
           ball=state.ball.position
           player=state.player_state(id_team,id_player).position
           #d=b-p
           if id_team==1:
               goal= Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
           else:
               goal = Vector2D(0,settings.GAME_HEIGHT/2)
           if player.distance(ball) < settings.PLAYER_RADIUS + settings.BALL_RADIUS:
               shoot_alt=goal-player
               if id_team==1:# ici on doit voir s'il y a un joueur a coté de la balle 
                   shoot_alt.scale(1)
               else:
                   shoot_alt.scale(1)
               return SoccerAction(shoot=shoot_alt)
           else:
               return SoccerAction(acceleration=ball-player)
           #return SoccerAction(d,Vector2D(1,0))

class SoloStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Test")
        self.i=-50
        
    def compute_strategy(self, state, id_team, id_player):
        """"ball=state.ball.position
        player=state.player_state(id_team,id_player).position
        if player.distance(ball) > (settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return SoccerAction(acceleration=ball-player)"""
        ball=state.ball.position
        sup=SupState(state,id_team,id_player)
        if self.i == 0 :
            if sup.dist_my_but()<settings.GAME_WIDTH//5 and sup.can_shoot() :
                return SoccerAction(shoot=Vector2D(500*sup.sens,0))
            if sup.my_position.y>3*settings.GAME_HEIGHT/4 or sup.my_position.y<settings.GAME_HEIGHT/4 :    #JE SUIS DANS LES DEUX QUARTS              
                if sup.can_shoot() : #je peux tirer vu que proche de la balle
                     if(sup.dist_but_adv()<settings.GAME_WIDTH/5): #autorisation pour tirer
                         return SoccerAction(shoot=(sup.but_adv-sup.my_position)) #tirer vers les bois
                     if (sup.my_position.x<settings.GAME_WIDTH/5 and sup.sens==-1)or(4*settings.GAME_WIDTH/5<sup.my_position.x and sup.sens==1):
                        return SoccerAction(shoot=(sup.but_adv-sup.my_position))
                     else :                            
                       shoot=Shoot2(sup).to_goal2()
                       #print(sup.dist_my_wall())
                       self.i=int(sup.dist_my_wall())*2
                       #if sup.proche_ball():
                       return shoot+SoccerAction(acceleration=Vector2D(2*sup.dist_my_wall()*sup.sens,0))#faire un rebond
                else:
                      return SoccerAction(acceleration=(ball-sup.my_position)*300)       #je peux pas tirer trop loin de la balle donc je vais vers la balle          
            else:
                if sup.can_shoot() : #si je suis dans les deux quarts du milieu
                      if(sup.dist_but_adv()<settings.GAME_WIDTH/6): #j'ai l'autorisation pour tirer
                          return SoccerAction(shoot=(sup.but_adv-sup.my_position)) #je tire
                      else:
                          return SoccerAction(shoot=(sup.but_adv-sup.my_position).norm_max(10)) #je drible ac la balle 
                else:
                      return SoccerAction(acceleration=(ball-sup.my_position)*300)   #je vais vers la balle vu que j'ai pas d'autorisation pour tirer
        elif self.i > 0: #a utiliser pour aller tout droit dans le cas du rebon
            self.i -= 1
            qte=(2*math.sqrt(2*((sup.dist_my_wall())**2)))
            qte2=math.sqrt(qte)
            
            return SoccerAction(acceleration=Vector2D(sup.sens*qte2,0)) #aller tout droit aprés le rebond
        else :
            self.i+=1
            return SoccerAction(acceleration=Vector2D(0,0)) #on reste immobile au début 

    

class Move(object): #MOVE et SHOOT copié du cours mode tevyas zat n chikh hhh et je sais pas pk on nous a demandé de les mettre dans un fichier actions.py  or qu'on nous a demandé d'avoir juste les 3 dans notre dossier.
    def __init__( self ,SupState):
            self.SupState=SupState
            
    def move(self, acceleration=None):
            return SoccerAction(acceleration=acceleration)
    def to_ball(self):
            return self.move(self.SupState.ball_dir()) 
        
        
        
class Shoot2(object):
    def __init__(self, SupState):
        self.SupState=SupState

    def shoot2(self, direction=None):
        if self.SupState.dist_ball() < settings.PLAYER_RADIUS + settings.BALL_RADIUS:
            return SoccerAction(shoot=direction)
        else :
            return SoccerAction(acceleration=self.SupState.ball_position-self.SupState.my_position)
        
    def to_goal(self, strength=1):
        return self.Shoot2((self.SupState.but_adv-self.SupState.my_position)*strength) 

    def to_goal2(self): #direction de la frappe
     # return self.shoot2(direction=Vector2D(0,50))
     #print(((self.SupState.dist_but_adv()*2**-0.5)*2))
     qte=(2*math.sqrt(2*((self.SupState.dist_my_wall())**2)))
     qte2=math.sqrt(qte)
     #print(self.i)
     if self.SupState.sens ==1:
         if self.SupState.my_position.y>settings.GAME_HEIGHT/2:    
             return SoccerAction(shoot=Vector2D(angle=1*(math.pi/4.),norm=qte*2),acceleration=Vector2D(self.SupState.sens*qte2*5,0))
         return  SoccerAction(shoot=Vector2D(angle=7*(math.pi/4.),norm=qte*2),acceleration=Vector2D(self.SupState.sens*qte2*5,0))   
     else:
         if self.SupState.my_position.y>settings.GAME_HEIGHT/2:
             return SoccerAction(shoot=Vector2D(angle=3*(math.pi/4.),norm=qte*2),acceleration=Vector2D(self.SupState.sens*qte2*5,0))
         return  SoccerAction(shoot=Vector2D(angle=5*(math.pi/4.),norm=qte*2),acceleration=Vector2D(self.SupState.sens*qte2*5,0))   
  