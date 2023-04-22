import pygame


class GUIState():
    def __init__(self, width=450, height=500, scale=1, size=5):
        pygame.init()
        self.width = width
        self.height = height
        self.scale = scale
        self.size = size

        # Ressourses
        self.isle = pygame.image.load("resources/isle.png")
        self.red_pawn = pygame.image.load("resources/pawn_red.png")
        self.green_pawn = pygame.image.load("resources/pawn_green.png")
        self.h_bridge = pygame.image.load("resources/bridge_h.png")
        self.v_bridge = pygame.image.load("resources/bridge_v.png")

        self.screen = pygame.display.set_mode((width, height))

    def display_state(self,state,display_current_player=True):
        self.screen.fill(0)
        # Draw the isles
        for i in range(self.size):
            for j in range(self.size):
                self.screen.blit(self.isle, (i * 100, j * 100))

        # Draw the horizontal bridges
        for i in range(self.size - 1):
            for j in range(self.size):
                if state.h_bridges[j][i]:
                    self.screen.blit(self.h_bridge, (i * 100 + 50, j * 100))

        # Draw the vertical bridges
        for i in range(self.size):
            for j in range(self.size - 1):
                if state.v_bridges[j][i]:
                    self.screen.blit(self.v_bridge, (i * 100, j * 100 + 50))

        # Draw the pawns
        for i in range(self.size - 2):
            self.screen.blit(self.green_pawn, (100 * state.cur_pos[0][i][0], 100 * state.cur_pos[0][i][1]))
            self.screen.blit(self.red_pawn, (100 * state.cur_pos[1][i][0], 100 * state.cur_pos[1][i][1]))

        if display_current_player:
            # Draw who's turn it is
            font1 = pygame.font.Font("freesansbold.ttf", 16)
            text1 = font1.render("Current player:", True, (255, 255, 255), "black")
            textRect1 = text1.get_rect()
            textRect1.center = (self.size * 50 - 45, self.size * 100 - 30)
            self.screen.blit(text1, textRect1)

            font2 = pygame.font.Font("freesansbold.ttf", 25)
            if state.cur_player == 0:
                text2 = font2.render("    ", True, "green", "green")
            else:
                text2 = font2.render("    ", True, "red", "red")
            textRect2 = text2.get_rect()
            textRect2.center = (self.size * 50 + 35, self.size * 100 - 30)
            self.screen.blit(text2, textRect2)

    def display_winner(self,state):
        quit = False
        # Game finished: display the winner
        clock = pygame.time.Clock()
        while not quit:
            clock.tick(30)
            # Draw board
            self.screen.fill(0)
            self.display_state(state,display_current_player=False)

            # Print the winner
            font = pygame.font.Font("freesansbold.ttf", 24)

            if state.get_winner() == 0:
                text = font.render(" Green wins! ", True, "green", "black")
            elif state.get_winner() == 1:
                text = font.render(" Red wins! ", True, "red", "black")
            else:
                text = font.render(" Tie! ", True, "white", "black")

            textRect = text.get_rect()
            textRect.center = ((self.size*2-1)*25, self.size * 100 - 30)
            self.screen.blit(text, textRect)

            # Print if time-out or invalid action
            if state.timeout_player != None:
                font2 = pygame.font.Font("freesansbold.ttf", 12)
                text2 = font2.render("The opponent timed out", True, (255, 255, 255), "black")
                textRect2 = text2.get_rect()
                textRect2.center = ((self.size*2-1)*25, self.size * 100 - 30)
                self.screen.blit(text2, textRect2)
            elif state.invalid_player != None:
                font2 = pygame.font.Font("freesansbold.ttf", 12)
                text2 = font2.render("The opponent made an invalid move", True, (255, 255, 255), "black")
                textRect2 = text2.get_rect()
                textRect2.center = ((self.size*2-1)*25, self.size * 100 - 10)
                self.screen.blit(text2, textRect2)

            # Update screen
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit = True

    def show_timer(self, times_left):
        font = pygame.font.Font("freesansbold.ttf", 12)
        text = font.render("        ", True, "green", "green")
        textRect = text.get_rect()
        textRect.center = (self.size * 100 - 140, self.size * 100 - 40)
        self.screen.blit(text, textRect)

        font = pygame.font.Font("freesansbold.ttf", 12)
        text = font.render("  " + str(int(times_left[0])) + " sec  ", True, (255, 255, 255), (34, 34, 34))
        textRect = text.get_rect()
        textRect.center = (self.size * 100 - 100, self.size * 100 - 40)
        self.screen.blit(text, textRect)


        font = pygame.font.Font("freesansbold.ttf", 12)
        text = font.render("        ", True, "red", "red")
        textRect = text.get_rect()
        textRect.center = (self.size * 100 - 140, self.size * 100 - 20)
        self.screen.blit(text, textRect)

        text = font.render("  " + str(int(times_left[1])) + " sec  ", True, (255, 255, 255), (34, 34, 34))
        textRect = text.get_rect()
        textRect.center = (self.size * 100 - 100, self.size * 100 - 20)
        self.screen.blit(text, textRect)