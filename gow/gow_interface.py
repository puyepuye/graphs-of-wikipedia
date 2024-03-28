import pygame
import sys
import graph_object

def run_pygame_window():
    # Initialize Pygame
    pygame.init()

    # Set up the window
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Graphs of Wikipedia Project')

    # Define colors
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    BLACK = (0, 0, 0)

    # Define font
    button_font = pygame.font.SysFont(None, 24)

    # Set up the buttons and graph area
    input_button_1 = pygame.Rect(50, 50, 150, 40)
    input_button_2 = pygame.Rect(50, 100, 150, 40)
    search_button = pygame.Rect(210, 50, 100, 90)
    graph_area = pygame.Rect(50, 150, 700, 400)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Add more event handling here if needed

        # Fill the screen with a white background
        window.fill(WHITE)

        # Draw the buttons
        pygame.draw.rect(window, GREY, input_button_1)
        pygame.draw.rect(window, GREY, input_button_2)
        pygame.draw.rect(window, GREY, search_button)

        # Draw the graph area
        pygame.draw.rect(window, BLACK, graph_area, 2)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_pygame_window()
