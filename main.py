import pygame, random, time, eztext

WIDTH = 450
HEIGHT = 800

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARK_GREEN = (0,100,0)
GREEN = (0,255,0)
GREY = (195,195,195)
BLUE = (8,27,105)

class gs(): #game state
	main_menu  = 1
	game_exit = 2
	game_play = 3
	game_names = 4
	game_names2 = 5
	how_to_img = 6
	winner_stat = 7
	
class Space_box():
	def __init__(self, screen, rect_x, rect_y, file_name):
		
		self.image = pygame.image.load(file_name)
		self.rect = self.image.get_rect()
		self.rect.x = rect_x
		self.rect.y = rect_y
		
	def draw(self, screen):
		screen.blit(self.image, [self.rect.x, self.rect.y])
		
class Menu_button():
	def __init__(self, screen, rect_x, rect_y, file_name, file_name2):
		
		self.file_name = file_name
		self.file_name2 = file_name2
		
		self.image = pygame.image.load(self.file_name)
		self.rect = self.image.get_rect()
		self.rect.x = rect_x
		self.rect.y = rect_y
		
	def draw(self, screen):
		screen.blit(self.image, [self.rect.x, self.rect.y])
		
	def highlight(self):
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			self.image = pygame.image.load(self.file_name2)
		else:
			self.image = pygame.image.load(self.file_name)
			
class Counter_piece():
	
	current_dice = random.randint(1,4)
	turn_counter = 2
	error_message = " "
	game_winner = None

	def __init__(self, screen, png_file, rect_x, rect_y):
		
		self.image = pygame.image.load(png_file).convert()
		self.rect = self.image.get_rect()
		self.rect.x = rect_x
		self.rect.y = rect_y
		self.current_space = 1
		
	def forward(self, second_counter, movement):
		
		if movement <= 11: #if the current dice roll + the counter position is less than 1
			
			if (movement != second_counter.current_space) or (movement in [1,5,11]): #Need to look at
				Counter_piece.turn_counter += 1 #add one to the turn counter, (will change go)
				self.current_space += Counter_piece.current_dice 
				self.rect.y = self.rect.y - 61*Counter_piece.current_dice 
				Counter_piece.current_dice = random.randint(1,4) 
				
			elif movement == second_counter.current_space:
				if movement is not [1,5,11]:
					Counter_piece.error_message = "can't do that, try your other counter"
					
		elif (movement > 11) and (self.current_space != 11):
			Counter_piece.turn_counter += 1
			self.rect.y = self.rect.y - 61*(11-self.current_space)
			self.current_space = 11
			Counter_piece.current_dice = random.randint(1,4) 
		else:
			Counter_piece.error_message = "can't do that, try your other counter"
		
	def backward(self, second_counter, movement):
		
		if self.current_space != 1:
			
			if (self.current_space - 1 != second_counter.current_space) or (self.current_space - 1 in [1,5,11]):
				Counter_piece.turn_counter += 1
				self.current_space -= 1
				self.rect.y = self.rect.y - 61*-1
				Counter_piece.current_dice = random.randint(1,4)
				
			elif self.current_space - 1 == second_counter.current_space:
				if movement is not [1,5,11]:
					Counter_piece.error_message = "can't do that, try your other counter"
		
		elif (self.current_space == 1) and (second_counter.current_space != 1):
			Counter_piece.error_message = "can't do that, try your other counter"
		elif (self.current_space == 1) and (second_counter.current_space == 1):
			Counter_piece.error_message = "can't do that, rolled dice again"
			Counter_piece.current_dice = random.randint(1,4)
				
	def update(self, second_counter, rival_counter1, rival_counter2, number, player_name):
		
		movement = self.current_space + Counter_piece.current_dice #equal to player position + current dice roll

		if Counter_piece.turn_counter % 2 == number: #if remainder is 0 or 1 (if O it's multiple of 2, and if 1 it's an odd number)
					if self.rect.collidepoint(pygame.mouse.get_pos()): #if this sprite instance is clicked
						Counter_piece.error_message = " " #set error message to nothing
						
						if Counter_piece.current_dice == 4:
							self.backward(second_counter, movement)
						elif Counter_piece.current_dice != 4:
							self.forward(second_counter, movement)		
							
						if self.current_space == rival_counter1.current_space: #if counter is equal to opponent counter
							if self.current_space not in [1,5,11]: #if not safe space
								rival_counter1.current_space = 1
								rival_counter1.rect.y = 630
								
						elif self.current_space == rival_counter2.current_space: #if counter is equal to opponent counter
							if self.current_space not in [1,5,11]: #if not safe space
								rival_counter2.current_space = 1
								rival_counter2.rect.y = 630
								
						if (self.current_space == 11) and (second_counter.current_space == 11):
							Counter_piece.game_winner = player_name #was hard
							print(player_name + " won") #need to finish
							Counter_piece.error_message = " "
							
							
	def draw(self, screen):
		screen.blit(self.image, [self.rect.x, self.rect.y])

def main():
	
	pygame.init()
	
	game_state = gs.main_menu
	
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode([WIDTH,HEIGHT])
	pygame.display.set_caption("AQADo")
	
	icon = pygame.image.load("icon.png")
	pygame.display.set_icon(icon)
	
	spaces = []
	spaces2 = []
	safe_space = []
	menu_buttons = []
	game_counters = []
	
	space_box_y = 15
	
	for i in range(11):
		spaces.append(Space_box(screen, 63, space_box_y, "space2.png"))
		spaces2.append(Space_box(screen, 8, space_box_y, "space3.png"))
		space_box_y += 61
		
	sprites_safe1 = Space_box(screen, 67, spaces[0].rect.y + 4, "space_safe.png")
	sprites_safe2 = Space_box(screen, 67, spaces[6].rect.y + 4, "space_safe.png")
	sprites_safe3 = Space_box(screen, 67, spaces[10].rect.y + 4, "space_safe.png")

	logo = Menu_button(screen, 5, 20, "logo.png", "logo1.png")
	edit_names = Menu_button(screen, 82, 200, "button1.png", "button11.png")
	play_game = Menu_button(screen, 82, 300, "button2.png", "button22.png")
	how_to = Menu_button(screen, 82, 400, "button4.png", "button44.png")
	exit_game = Menu_button(screen, 82, 500, "button3.png", "button33.png")
	
	green_counter1 = Counter_piece(screen, "counter1.png", 85, 630)
	green_counter2 = Counter_piece(screen, "counter1.png", 140, 630)
	grey_counter1 = Counter_piece(screen, "counter2.png", 300, 630)
	grey_counter2 = Counter_piece(screen, "counter2.png", 355, 630)
	
	menu_buttons.append(edit_names)
	menu_buttons.append(play_game)
	menu_buttons.append(exit_game)
	menu_buttons.append(how_to)
	menu_buttons.append(logo)
	
	safe_space.append(sprites_safe1)
	safe_space.append(sprites_safe2)
	safe_space.append(sprites_safe3)
	
	game_counters.append(green_counter1)
	game_counters.append(green_counter2)
	game_counters.append(grey_counter1)
	game_counters.append(grey_counter2)
	
	txtbx = eztext.Input(maxlength=45, color=(0,0,0), prompt='Player 1\'s name: ')
	txtbx2 = eztext.Input(maxlength=45, color=(0,0,0), prompt='Player 2\'s name: ')
	
	txtbx.set_pos(25,335)
	txtbx2.set_pos(25,335)
	
	myfont = pygame.font.SysFont("monospace", 25)
	myfont2 = pygame.font.SysFont("monospace", 15)
	myfont3 = pygame.font.SysFont(None, 25)
	
	player1_name = "Player 1"
	player2_name = "Player 2"
	
	pygame.mixer.music.load("music.mp3")
	pygame.mixer.music.play(-1)

	while game_state != 2:
		
		events = pygame.event.get()
		
		for event in events:
			if event.type == pygame.QUIT:
				 game_state = 2

			if event.type == pygame.MOUSEBUTTONUP:
				
				green_counter1.update(green_counter2, grey_counter1, grey_counter2, 0, player1_name)
				green_counter2.update(green_counter1, grey_counter1, grey_counter2, 0, player1_name)
				grey_counter1.update(grey_counter2, green_counter1, green_counter2, 1, player2_name)
				grey_counter2.update(grey_counter1, green_counter1, green_counter2, 1, player2_name)
						
		screen.fill(BLUE)
			
		if Counter_piece.turn_counter % 2 == 0: #if player 1's turn
			player_turn = player1_name #player_turn variable = player 1's name
		elif Counter_piece.turn_counter % 2 == 1: #if player 2's turn
			player_turn = player2_name #player_turn variable = player 2's name
		
		if game_state == 3: #if 'play game' is clicked
			
			splash = pygame.image.load("background_img.png")
			screen.blit(splash, [0,0])
			
			file_name1 = "dice" + str(Counter_piece.current_dice) + ".png"
			
			for box, rectangle in zip(spaces, spaces2):
				box.draw(screen)
				rectangle.draw(screen)
				
			for space in safe_space:
				space.draw(screen)
				
			for counter in game_counters:
				counter.draw(screen)
				
			label = myfont.render(player_turn + " rolled a " + str(Counter_piece.current_dice), 1, BLACK)
			stuck_msg = myfont2.render(Counter_piece.error_message, 1, BLACK)
			image = pygame.image.load(file_name1)
			
			screen.blit(image, [40,spaces[10].rect.y + 80])
			screen.blit(label, [110,spaces[10].rect.y + 96])
			screen.blit(stuck_msg, [105,spaces[10].rect.y + 120])
			
			for i in range(1,12):
				num = myfont3.render(str(i), 1, BLACK)
				screen.blit(num, [spaces2[-i].rect.x + 22, spaces2[-i].rect.y + 3 + 19])
				
			if Counter_piece.game_winner != None: #if person wins game
				game_state = 7
				
		elif game_state == 4: #if entering player names

			splash = pygame.image.load("background_img1.png")
			screen.blit(splash, [0,0])
			
			main_menu = False
			txtbx.update(events)
			txtbx.draw(screen) #display name input text
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if len(txtbx.value) == 0: #if no text is entered
						pass #don't proceed 
					else: 
						player1_name = txtbx.value
						game_state = 5
						

		elif game_state == 5: #if player 2's entering name

			screen.blit(splash, [0,0])
			txtbx2.update(events)
			txtbx2.draw(screen)
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if len(txtbx2.value) == 0:
						pass
					else:
						player2_name = txtbx2.value
						game_state = 1

		if game_state == 1:

			splash = pygame.image.load("background_img3.png")
			screen.blit(splash, [0,0])
			
			for objects in menu_buttons:
				objects.draw(screen)
				objects.highlight()

			if event.type == pygame.MOUSEBUTTONUP:
				if play_game.rect.collidepoint(pygame.mouse.get_pos()):
					game_state = 3
				elif exit_game.rect.collidepoint(pygame.mouse.get_pos()):
					game_state = 2	
				elif edit_names.rect.collidepoint(pygame.mouse.get_pos()):
					txtbx.value = "" #when edit names clicked, change them back to nothing (bug fix)
					txtbx2.value = ""
					game_state = 4
				elif how_to.rect.collidepoint(pygame.mouse.get_pos()):
					game_state = 6

			#reset game info
			green_counter1.current_space = 1
			green_counter2.current_space = 1
			grey_counter1.current_space = 1
			grey_counter2.current_space = 1
			
			green_counter1.rect.y = 630
			green_counter2.rect.y = 630
			grey_counter1.rect.y = 630
			grey_counter2.rect.y = 630
			
			Counter_piece.turn_counter = 2
			Counter_piece.game_winner = None
			
		if game_state == 6:
			splash = pygame.image.load("help_img.png")
			screen.blit(splash, [0,0])
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					game_state = 1
					
		if game_state == 7:
			
			winner_msg = myfont.render(Counter_piece.game_winner + " Wins!", 1, BLACK) #winner name display
			splash1 = pygame.image.load("background_img2.png")
			screen.blit(splash1, [0,0])
			screen.blit(winner_msg, [135,150])
		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					game_state = 1
			
					
		pygame.display.update()
		 
		clock.tick(30)
	
if __name__ == '__main__':
	main()   
