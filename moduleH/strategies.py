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



class GoTestStrategy ( Strategy ):
    def __init__ ( self , strength = None ):
        Strategy . __init__ ( self , "Go - getter " )
        self . strength = strength
    def compute_strategy ( self , state , id_team , id_player ):
        s =SupState( state , id_team , id_player )
        move = Move (s )
        shoot = Shoot2(s )
        return move . to_ball () + shoot . to_goal ( self . strength )


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
        
        
class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)  
        if sup.dist_fil()>10 and sup.can_shoot():
                return SoccerAction(shoot=(sup.centre()-sup.my_position).norm_max(1.3),acceleration=(sup.predict_ball()-sup.my_position))
    
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

                       
                                                         
        
        
        

                                                                                                                                                
class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
           ball=state.ball.position
           player=state.player_state(id_team,id_player).position
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



class SoloStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Test")
        self.i=0
        
    def compute_strategy(self, state, id_team, id_player):
        ball=state.ball.position
        sup=SupState(state,id_team,id_player)
        if self.i == 0 :
            if sup.dist_my_but()<settings.GAME_WIDTH//6 and sup.can_shoot() :
                return SoccerAction(shoot=Vector2D(500*sup.sens,0))
            if sup.my_position.y>3*settings.GAME_HEIGHT/4 or sup.my_position.y<settings.GAME_HEIGHT/4 :    #JE SUIS DANS LES DEUX QUARTS              
                if sup.can_shoot() : #je peux tirer vu que proche de la balle
                     if(sup.dist_but_adv()<settings.GAME_WIDTH/5): #autorisation pour tirer
                         return sup.shoot_goal()#tirer vers les bois
                     if (sup.my_position.x<settings.GAME_WIDTH/5 and sup.sens==-1)or(4*settings.GAME_WIDTH/5<sup.my_position.x and sup.sens==1):
                        return sup.shoot_goal()
                     elif sup.adv_closer_dist() <  2*sup.dist_my_wall() and sup.can_shoot_lonely():                         
                       shoot=Shoot2(sup).to_goal2()
                       self.i=int(sup.dist_my_wall())
                       return shoot+SoccerAction(acceleration=Vector2D(sup.dist_my_wall()*sup.sens,0))#faire un rebond
                     else :
                       return sup.shoot_goal()
                else:
                      return SoccerAction(acceleration=(ball-sup.my_position)*300)       #je peux pas tirer trop loin de la balle donc je vais vers la balle          
            else:
                if sup.can_shoot() : #si je suis dans les deux quarts du milieu
                      if(sup.dist_but_adv()<settings.GAME_WIDTH/6): #j'ai l'autorisation pour tirer
                          return sup.shoot_goal() #je tire
                      else:
                          return sup.shoot_goal() #je drible ac la balle 
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



class DefenseStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defense")


    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)
        centre=sup.def_bonne_pos((9*settings.GAME_WIDTH/10 if sup.sens==-1 else settings.GAME_WIDTH/10) if len(sup.co_players)==1 else  (4*settings.GAME_WIDTH/5 if sup.sens==-1 else settings.GAME_WIDTH/5))
        if sup.can_shoot():
            return SoccerAction(shoot=(sup.pos_coplayer(0) - sup.my_position).norm_max(sup.my_position.distance(sup.pos_coplayer(0))/10) , acceleration = centre - sup.my_position)
        if sup.proche_ball():
            return SoccerAction(acceleration = sup.predict_ball() - sup.my_position)
        if (sup.predict_ball().x > 5 * settings.GAME_WIDTH/8 and sup.sens==-1) or ( sup.predict_ball().x < 3* settings.GAME_WIDTH/8 and sup.sens==1):
            return SoccerAction(acceleration = sup.predict_ball() - sup.my_position)
        return SoccerAction( acceleration = centre - sup.my_position)



class GardienStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Gardien")
        #self.i=-50

    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)
        centre=sup.def_bonne_pos(x=29*settings.GAME_WIDTH/30 if sup.sens==-1 else settings.GAME_WIDTH/30)
        if sup.can_shoot():
            return SoccerAction(shoot= ((sup.pos_coplayer(2) - sup.my_position)), acceleration = centre - sup.my_position)
        if sup.predict_ball().distance(sup.my_position)< 5 :#or ( sup.dist_adv_nearby()< 30 and sup.pos_adv_nearby().distance(sup.ball_position())> sup.dist_ball() and sup.dist_ball() < 15 and sup.ball_position().x < settings.GAME_WIDTH/5):#sup.proche_ball():
            return SoccerAction(acceleration = sup.predict_ball() - sup.my_position)
        return SoccerAction( acceleration = centre - sup.my_position)
    
    
    
class SoloStrategy2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Test")
        self.i=0
        self.first=0
        
    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)
        if self.i == 0 :
            if self.first>0:
                self.first-=1
                return sup.bien_pos()
            else:
                
                if sup.my_position.y>3*settings.GAME_HEIGHT/4 or sup.my_position.y<settings.GAME_HEIGHT/4 :    #JE SUIS DANS LES DEUX QUARTS     
                    
                    if sup.can_shoot() : #je peux tirer vu que proche de la balle
                         if (sup.my_position.x<settings.GAME_WIDTH/5 and sup.sens==-1)or(4*settings.GAME_WIDTH/5<sup.my_position.x and sup.sens==1)or sup.someone_there():# aqlagh g chwaki on dois faire le rebond ahid le corner
                             return sup.shoot_goal() #return SoccerAction(shoot=(sup.but_adv-sup.my_position))
                         elif sup.someone_there() and sup.adv_closer_dist() < sup.dist_my_wall()*2 :                            
                           shoot=Shoot2(sup).to_goal2()
                           self.i=2*int(sup.dist_my_wall())/3
                           #if sup.proche_ball():
                           return shoot+SoccerAction(acceleration=Vector2D(2*sup.dist_my_wall()*sup.sens,0))#faire un rebond
                         else :
                           return sup.shoot_goal()
                    else:
                         if sup.autor_attaq():
                             return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position)*300)       #je peux pas tirer trop loin de la balle donc je vais vers la balle          
                         else:
                             return sup.bien_pos()
                else:
                    if sup.can_shoot() : #si je suis dans les deux quarts du milieu
                          return sup.shoot_goal()+SoccerAction(acceleration = (sup.predict_ball() - sup.my_position)*100) #je drible ac la balle 
                    else:
                          if sup.autor_attaq():
                              return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position)*300)   #je vais vers la balle vu que j'ai pas d'autorisation pour tirer
                          else:
                              return sup.bien_pos()
                              
                          
        elif self.i > 0: #a utiliser pour aller tout droit dans le cas du rebon
            self.i -= 1
            qte=(2*math.sqrt(2*((sup.dist_my_wall())**2)))
            qte2=math.sqrt(qte)
            
            return SoccerAction(acceleration=Vector2D(sup.sens*qte2,0)) #aller tout droit aprés le rebond
        else :
            self.i+=1
            print( "le probleme est iciii")
            qte=(2*math.sqrt(2*((sup.dist_adv_corner())**2)))
            qte2=math.sqrt(qte)
            return SoccerAction(acceleration=Vector2D(0,sup.sens*qte2)) #aller vers la direction de la balle    

        
        
        
class SoloStrategy4(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaq_Gard")
        self.i=0
        self.first=0
        
    def compute_strategy(self, state, id_team, id_player):
        sup=SupState(state,id_team,id_player)
        if self.i == 0 :
            if self.first>0:
                self.first-=1
                return sup.bien_pos(2,1)
            else:
                
                if sup.my_position.y>3*settings.GAME_HEIGHT/4 or sup.my_position.y<settings.GAME_HEIGHT/4 :    #JE SUIS DANS LES DEUX QUARTS     
                    
                    if sup.can_shoot() : #je peux tirer vu que proche de la balle
                         if (sup.my_position.x<settings.GAME_WIDTH/5 and sup.sens==-1)or(4*settings.GAME_WIDTH/5<sup.my_position.x and sup.sens==1)or sup.someone_there():# aqlagh g chwaki on dois faire le rebond ahid le corner
                             return sup.shoot_goal() #return SoccerAction(shoot=(sup.but_adv-sup.my_position))
                         elif sup.someone_there() and sup.adv_closer_dist() < sup.dist_my_wall()*2 :                            
                           shoot=Shoot2(sup).to_goal2()
                           self.i=2*int(sup.dist_my_wall())/3
                           #if sup.proche_ball():
                           return shoot+SoccerAction(acceleration=Vector2D(2*sup.dist_my_wall()*sup.sens,0))#faire un rebond
                         else :
                           return sup.shoot_goal()
                    else:
                         if sup.autor_attaq():
                             return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position)*300)       #je peux pas tirer trop loin de la balle donc je vais vers la balle          
                         else:
                             return sup.bien_pos(2,1)
                else:
                    if sup.can_shoot() : #si je suis dans les deux quarts du milieu
                          return sup.shoot_goal()+SoccerAction(acceleration = (sup.predict_ball() - sup.my_position)*100) #je drible ac la balle 
                    else:
                          if sup.autor_attaq():
                              return SoccerAction(acceleration=(sup.predict_ball()-sup.my_position)*300)   #je vais vers la balle vu que j'ai pas d'autorisation pour tirer
                          else:
                              return sup.bien_pos(2,1)
                              
                          
        elif self.i > 0: #a utiliser pour aller tout droit dans le cas du rebon
            self.i -= 1
            qte=(2*math.sqrt(2*((sup.dist_my_wall())**2)))
            qte2=math.sqrt(qte)
            
            return SoccerAction(acceleration=Vector2D(sup.sens*qte2,0)) #aller tout droit aprés le rebond
        else :
            self.i+=1
            print( "le probleme est iciii")
            qte=(2*math.sqrt(2*((sup.dist_adv_corner())**2)))
            qte2=math.sqrt(qte)
            
            return SoccerAction(acceleration=Vector2D(0,sup.sens*qte2)) #aller vers la direction de la balle



class Move(object): # mode tevyas zat n chikh hhh et je sais pas pk on nous a demandé de les mettre dans un fichier actions.py  or qu'on nous a demandé d'avoir juste les 3 dans notre dossier.
    def __init__( self ,SupState):
            self.SupState=SupState
            
    def move(self, acceleration=None):
            return SoccerAction(acceleration=acceleration)
    def to_ball(self):
            return SoccerAction(acceleration=self.SupState.ball_position()-self.SupState.my_position)         
        

      
class Shoot2(object):
    def __init__(self, SupState):
        self.SupState=SupState

    def shoot2(self, direction=None):
        if self.SupState.dist_ball() < settings.PLAYER_RADIUS + settings.BALL_RADIUS:
            return SoccerAction(shoot=direction)
        else :
            return SoccerAction(acceleration=self.SupState.ball_position-self.SupState.my_position)
        
    def to_goal(self, strength=1):
        return SoccerAction(shoot=(self.SupState.but_adv-self.SupState.my_position)*strength) 

    def to_goal2(self,angle2 = math.pi/4.): #direction de la frappe
     # return self.shoot2(direction=Vector2D(0,50))
     #print(((self.SupState.dist_but_adv()*2**-0.5)*2))
     qte=(2*math.sqrt(2*(((self.SupState.dist_my_wall()) if angle2 == math.pi/4 else self.SupState.dist_adv_corner())**2)))
     qte2=math.sqrt(qte)
     #print(self.i)
     if self.SupState.sens ==1:
         if self.SupState.my_position.y>settings.GAME_HEIGHT/2:    
             return SoccerAction(shoot=Vector2D(angle=1*(angle2),norm=qte*2),acceleration=(Vector2D(self.SupState.sens*qte2*5,0)if angle2== math.pi/4 else Vector2D(0,self.SupState.sens*qte2*5)))
         return  SoccerAction(shoot=Vector2D(angle=7*(angle2),norm=qte*2),acceleration=(Vector2D(self.SupState.sens*qte2*5,0)if angle2== math.pi/4 else Vector2D(0,self.SupState.sens*qte2*5)))   
     else:
         if self.SupState.my_position.y>settings.GAME_HEIGHT/2:
             return SoccerAction(shoot=Vector2D(angle=3*(angle2),norm=qte*2),acceleration=(Vector2D(self.SupState.sens*qte2*5,0)if angle2== math.pi/4 else Vector2D(0,self.SupState.sens*qte2*5)))
         return  SoccerAction(shoot=Vector2D(angle=5*(angle2),norm=qte*2),acceleration=(Vector2D(self.SupState.sens*qte2*5,0)if angle2== math.pi/4 else Vector2D(0,self.SupState.sens*qte2*5)))   
