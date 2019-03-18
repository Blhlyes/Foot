#objets pour un match

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, settings
from sklearn.model_selection import ParameterGrid


class GoalSearch ( object ):
    def __init__ ( self , strategy , params , simu = None , trials =20 ,
                  max_steps =1000000 , max_round_step =40):
        self.strategy = strategy
        self.params = params.copy()
        self.simu = simu
        self.trials = trials
        self.max_steps = max_steps
        self.max_round_step = max_round_step
    def start( self , show = True ):
        if not self.simu :
            team1 = SoccerTeam ( " Team ␣ 1 " )
            team2 = SoccerTeam ( " Team ␣ 2 " )
            team1.add(self.strategy.name , self.strategy )
            team2.add(Strategy().name , Strategy())
            self.simu = Simulation( team1 , team2 , max_steps = self.max_steps )
        self.simu.listeners += self
        if show :
            show_simu(self.simu)
        else :
            self.simu.start()

    def begin_match ( self , team1 , team2 , state ):
        self.last_step = 0 # Step of the last round
        self.criterion = 0 # Criterion to maximize ( here , number of goals )
        self.cpt_trials = 0 # Counter for trials
        self.param_grid = iter ( ParameterGrid ( self.params )) # Iterator for the g
        self.cur_param = next ( self.param_grid , None ) # Current parameter
        if self.cur_param is None :
            raise ValueError('no␣parameter␣given.')
        self.res = dict () # Dictionary of results
    
    def begin_round ( self , team1 , team2 , state ):
        ball = Vector2D.create_random( low =0 , high =1)
        ball.y=ball.y*settings.GAME_HEIGHT
        ball.x=ball.x*settings.GAME_WIDTH*(3/5)+settings.GAME_WIDTH*(3/5)
        self.simu.state.states[(1 , 0)].vitesse = Vector2D () # Player accelerati
        self.simu.state.ball.position = ball.copy() # Ball position
        self.last_step = self.simu.step
        self.simu.state.states[(1 , 0)].position=self.simu.state.ball.position
        # Last step of the game
        # Set the current value for the current parameters
        for key , value in self.cur_param.items():
            setattr ( self.strategy , key , value )

    def end_round ( self , team1 , team2 , state ):
        # A round ends when there is a goal of if max step is achieved
        if state.goal > 0:
            self.criterion += 1 # Increment criterion
        self.cpt_trials += 1
            # Increment number of trials
        print ( self.cur_param , end = "         " )
        print ( " Crit :    {}        Cpt :  {} " . format ( self.criterion , self.cpt_trials ))
        if self.cpt_trials >= self.trials :
            # Save the result
            self.res[ tuple ( self.cur_param.items ())] = self.criterion * 1. / self.trials
            # Reset parameters

            self.criterion = 0
            self.cpt_trials = 0

            # Next parameter value
            self.cur_param = next ( self.param_grid , None )
            if self.cur_param is None :
                self.simu.end_match ()

    def update_round ( self , team1 , team2 , state ):
        # Stop the round if it is too long
        if state.step > self.last_step + self.max_round_step :
            self.simu.end_round ()


    def get_res ( self ):
        return self.res
    
    def get_best ( self ):
        return max ( self.res , key = self.res.get )
    


class SupState(object):

	def __init__(self,state,idteam,idplayer) :
		self.state = state
		self.key = (idteam, idplayer)
		self.but_adv = Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT/2) if self.key[0] == 1 else Vector2D(0, settings.GAME_HEIGHT/2)
		self.my_but = Vector2D(0, settings.GAME_HEIGHT/2) if self.key[0] == 1 else Vector2D(settings.GAME_WIDTH, settings.GAME_HEIGHT/2)
		#recup joueur
		self.all_players = self.state.players
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		if len(self.co_players)>=1 :
			self.co_player = self.co_players[0]
			self.co_player_pos = self.state.player_state(self.co_player[0],self.co_player[1]).position
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		self.adv_players_pos = [self.state.player_state(p[0],p[1]).position for p in self.adv_players]
		#variable pour avoir le sens pour pouvoir l'utiliser lors de changement ...
		self.sens = 1 if self.key[0] == 1 else -1

    #si le joueur peut tirer METHODEEEEEEEEEEEE
		self.my_position = self.state.player_state(self.key[0], self.key[1]).position
		#self.v_ball = self.state.ball.vitesse
    	#a revoir sans pitié
         # |self.adv_on_right = 1 if self.state.player_state(self.adv_players[0][0], self.adv_players[0][1]).position.y > self.my_position.y else -1
		self.my_v = self.state.player_state(self.key[0], self.key[1]).vitesse
	
#    @property
	def proche_ball(self):
		me_ball = self.predict_ball().distance(self.my_position)
		for p in self.co_players:
			pos_p = self.state.player_state(p[0], p[1]).position
			if me_ball > pos_p.distance(self.predict_ball()) :
				return False
		return True
    
    
	@property
	def have_ball(self):
		return self.my_position.distance(self.ball_position) < 1


	def ball_position(self):
		return self.state.ball.position
    
	def ball_dir(self):
		return self.state.ball.direction

	def can_shoot(self,position = None,ballpos = None):
		if position is None :
			position = self.my_position
		if ballpos is None :
			ballpos = self.ball_position()
		if position.distance(ballpos) < (settings.PLAYER_RADIUS + settings.BALL_RADIUS):
			return True
		return False


	def v_ball(self):
            return self.state.ball.vitesse

	def eclatement(self):
            l1=[] 
            l2=[] 
            l3=[] 
            l4=[] 
            l5=[] 
            l6=[] 
            l7=[] 
            l8=[] 
            l9=[]
            l10=[]
            l11=[]
            l12=[]
            l13=[]
            l14=[]
            l15=[]
            l16=[]
            for player in self.all_players:
                if player.position.x<settings.GAME_WIDTH//4:
                    if player.position.y<settings.GAME_HEIGHT//4:
                        l1.add(player)
                    elif player.position.y<settings.GAME_HEIGHT//2:
                        l5.add(player)
                    elif player.position.y<3*settings.GAME_HEIGHT//4:
                        l9.add(player)
                    else:
                        l12.add(player)
                elif player.position.x<settings.GAME_WIDTH//2:
                    if player.position.y<settings.GAME_HEIGHT//4:
                        l2.add(player)
                    elif player.position.y<settings.GAME_HEIGHT//2:
                        l6.add(player)
                    elif player.position.y<3*settings.GAME_HEIGHT//4:
                        l10.add(player)
                    else:
                        l14.add(player)                           
                elif player.position.x<3*settings.GAME_WIDTH//4:
                    if player.position.y<settings.GAME_HEIGHT//4:
                        l.add(player) #############a9lin dayi
                    elif player.position.y<settings.GAME_HEIGHT//2:
                        l10.add(player)
                    elif player.position.y<3*settings.GAME_HEIGHT//4:
                        l11.add(player)
                    else:
                        l12.add(player)   
                else:
                    if player.position.y<settings.GAME_HEIGHT//4:
                        l13.add(player)
                    elif player.position.y<settings.GAME_HEIGHT//2:
                        l14.add(player)
                    elif player.position.y<3*settings.GAME_HEIGHT//4:
                        l15.add(player)
                    else:
                        l16.add(player)              
                                    #a completer
             
                return [[l1,l2,l3,l4],[l5]]




	def autor_attaq(self):     
         return (self.predict_ball().x<2*settings.GAME_WIDTH/3 and self.sens==-1)or(self.predict_ball().x>settings.GAME_WIDTH/3 and self.sens==1)


	"""def bien_pos(self):
         if self.sens==1:
             empl=Vector2D(settings.GAME_WIDTH/4,5*settings.GAME_HEIGHT/6)
             if self.my_position.x - self.co_player_pos.x > 50 and self.my_position.x > 75 :
                 print("          ",self.co_player_pos.x)
                 return SoccerAction(acceleration=Vector2D(self.co_player_pos.x+50,5*settings.GAME_HEIGHT/6)-self.my_position)
             return SoccerAction(acceleration=empl-self.my_position)
         else:
             empl=Vector2D(3*settings.GAME_WIDTH/4,5*settings.GAME_HEIGHT/6)
             if self.co_player_pos.x - self.my_position.x > 50 and self.my_position.x > 75:
                 print(self.co_player_pos.x)
                 return SoccerAction(acceleration=Vector2D(self.co_player_pos.x-50,5*settings.GAME_HEIGHT/6)-self.my_position)
             return SoccerAction(acceleration=empl-self.my_position)         """
             
	def bien_pos(self):
		if self.sens==-1:
			empl=Vector2D(self.co_player_pos.x-60,5*settings.GAME_HEIGHT/6)
			return SoccerAction(acceleration=empl-self.my_position)
		else:
			empl=Vector2D(self.co_player_pos.x+60,5*settings.GAME_HEIGHT/6)
			return SoccerAction(acceleration=empl-self.my_position)


	def coeq_proche(self):
		return [p for p in self.co_players if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < (settings.GAME_WIDTH/2)] #A revoir et werna mlih ^-^

	def my_vit(self):
		return self.state.player_state(self.key[0], self.key[1]).vitesse

	def near_ball(self):
		if self.my_position.distance(self.ball_position) < settings.BALL_RADIUS:
			return True
		return False


	def dist_ball(self):
		return self.my_position.distance(self.ball_position())


	def dist_but_adv(self):
		return self.my_position.distance(self.but_adv)


	def dist_my_but(self):
		return self.my_position.distance(self.my_but)


	def pos_adv_nearby(self):
     		return min([(self.player.distance(player),player) for player in self.adv_players])[1]


	def dist_adv_nearby(self):
		return min([(self.player.distance(player),player) for player in self.adv_players])[0]
    
	def dist_my_wall(self):
		if self.my_position.y>settings.GAME_HEIGHT/2:
			return settings.GAME_HEIGHT - self.my_position.y
		return self.my_position.y

	def dist_adv_corner(self):
		if self.sens ==1 :
			return settings.GAME_WIDTH - self.my_position.x
		return self.my_position.x

	@property
	def coeq_libre(self) :
		if len(self.coeq_proche) == 0 :
			return [0, 0]
		elif len(self.coeq_proche) == 1 :
			return self.coeq_proche[0]
		else :
			p = self.coeq_proche[0]
			d = self.adv_nearby(self.state.player_state(p[0], p[1]).position) #position de p
			x = self.state.player_state(p[0], p[1]).position.distance(self.state.player_state(d[0], d[1]).position)
			pp = self.coeq_proche[0]
			for p in self.coeq_proche[1:] :
				#position de l'adv le plus proche de du coeq le plus proche
				a = self.adv_nearby(self.state.player_state(p[0], p[1]).position)
				ap = self.state.player_state(a[0], a[1]).position
				d = self.state.player_state(p[0], p[1]).position.distance(ap)
				if x < d :
					x = d
					pp = p
		return pp


	def aller_ball(self) :
		#les cas ou je suis proche de la balle et elle va vite?
		k = (self.v_ball()*3+(self.ball_position() - self.my_position))
		joue = SoccerAction(acceleration = k)
		if self.dist_ball() > 11:
			return joue
		elif self.dist_ball() > 4:
			return SoccerAction(acceleration=(self.ball_position() - self.my_position)/2)
		else :
			return SoccerAction(acceleration=(self.ball_position() - self.my_position).normalize())

	def can_shoot_lonely(self) :
		for p in self.adv_players_pos:
			if self.can_shoot(p):
				return False
		return True



	def predict_ball(self):
		if self.dist_ball() < 2*(settings.PLAYER_RADIUS + settings.BALL_RADIUS):
			return self.ball_position()+self.v_ball()
		norm_base = self.v_ball().norm
		norm_tour = self.v_ball().norm - settings.ballBrakeSquare * self.v_ball().norm ** 2 - settings.ballBrakeConstant * self.v_ball().norm
		norm_fin = norm_base *2 - norm_tour
		ball_pos_fin = self.ball_position() + (self.v_ball().normalize() * norm_fin)
		return ball_pos_fin
    
	def shoot_goal(self):
		if(self.dist_but_adv()<40): #j'ai l'autorisation pour tirer
			return SoccerAction(shoot=(self.but_adv-self.my_position).norm_max(4)) #je tire
		if self.adv_closer_dist() < 20:
			return SoccerAction(shoot=(self.but_adv - self.my_position).norm_max(30))
		return SoccerAction(shoot=(self.but_adv-self.my_position).norm_max(1.6))
    


    
    
	def someone_there(self):
		for p in self.adv_players_pos:
			if self.my_position.x*self.sens < p.x*self.sens:
				return True
		return False
    
    
    
    
	def adv_closer_dist(self):
		tmp=100
		for p in self.adv_players_pos :
			if self.my_position.distance(p) < tmp and self.my_position.x*self.sens < p.x*self.sens:
				tmp =self.my_position.distance(p)
		return tmp
    
	def def_bonne_pos(self,x=None):
		if x is None:            
			x=4*settings.GAME_WIDTH/5 if self.sens==-1 else settings.GAME_WIDTH/5
            
		a=((self.ball_position().y-self.my_but.y)/(self.ball_position().x-self.my_but.x))
		b=(self.my_but.y-a*(self.my_but.x))
		y=a*x+b
		return Vector2D(x,y)
    
    
    
    
