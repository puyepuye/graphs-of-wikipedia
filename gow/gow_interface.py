import pygame
import sys
from visualize_template import *
from graph_object import *

def run_pygame_window():
    pygame.init()
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Clickable Button in Pygame')

    # Define colors and font
    BUTTON_NORMAL = (100, 200, 100)
    BUTTON_HOVER = (100, 255, 100)
    WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
    font = pygame.font.SysFont(None, 40)

    # Create input boxes above the button
    input_box_1 = pygame.Rect(window_width // 2 - 250, window_height // 2 - 200, 500, 40)
    input_box_2 = pygame.Rect(window_width // 2 - 250, window_height // 2 - 125, 500, 40)
    input_text_1, input_text_2 = '', ''
    active_box_1, active_box_2 = False, False
    fun_fact_display = False

    # Create a button
    button_font = pygame.font.SysFont(None, 30)
    button_rect = pygame.Rect(window_width // 2 - 125, window_height // 2 - 75, 250, 50)
    button_text = button_font.render('Find paths!', True, BLACK)

    # Cursor logic
    cursor_color = BLACK
    cursor = pygame.Rect(input_box_1.topleft, (2, input_box_1.height-10))
    cursor_visible = True
    last_cursor_switch_time = pygame.time.get_ticks()
    cursor_switch_interval = 500

    # To Text
    pygame.font.init()  # you have to call this at the start,


    # Fun Fact Text box
    rect_width = 300
    rect_height = 40
    border_radius = 20
    circle_radius = rect_height // 2

    # Calculate positions
    rect_x = (window_width // 2) - (rect_width // 2) - circle_radius  # Subtract circle radius to offset for the circle
    rect_y = (window_height // 2) - (rect_height // 2)

    # Create the rectangle and circle for the text box
    text_box_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    circle_center = (rect_x, rect_y + circle_radius)

    # Main loop
    running = True
    while running:
        display_text = ""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_1.collidepoint(event.pos):
                    active_box_1, active_box_2 = True, False
                    cursor.topleft = (input_box_1.x + font.size(input_text_1)[0] + 5, input_box_1.y + 5)
                elif input_box_2.collidepoint(event.pos):
                    active_box_1, active_box_2 = False, True
                    cursor.topleft = (input_box_2.x + font.size(input_text_2)[0] + 5, input_box_2.y + 5)
                elif button_rect.collidepoint(event.pos):
                    print(f'Clicked with text 1: {input_text_1} and text 2: {input_text_2}')
                    g_g, g_d = load_gow_json('../database/mini_graph.json')
                    s1, s2, s3, s4, s5 = summary(g_d, input_text_1, input_text_2)
                    visualize_paths(g_g, g_d, input_text_1, input_text_2)
                    fun_fact_display = True

                    # Draw the text content in the text box
                    # You need to define display_text somewhere above, e.g., display_text = "Some text"
                    my_font = pygame.font.SysFont('Arial', 20)
                    text_surface = my_font.render('to', False, (0, 0, 0))
                    window.blit(text_surface, (0, 0))


                else:
                    active_box_1, active_box_2 = False, False

                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                if active_box_1 or active_box_2:
                    # Determine which box is active and assign the input text accordingly
                    input_text = input_text_1 if active_box_1 else input_text_2

                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                    # Update the input text for the active box
                    if active_box_1:
                        input_text_1 = input_text
                    else:
                        input_text_2 = input_text

                    # Adjust cursor position after text update
                    if active_box_1:
                        cursor.x = input_box_1.x + font.size(input_text_1)[0] + 5
                    else:
                        cursor.x = input_box_2.x + font.size(input_text_2)[0] + 5

        pygame.display.flip()

        # Cursor blink logic
        current_time = pygame.time.get_ticks()
        if current_time - last_cursor_switch_time >= cursor_switch_interval:
            cursor_visible = not cursor_visible
            last_cursor_switch_time = current_time

        border_radius_input_box = 10

        # Drawing input boxes with rounded corners in the main loop
        window.fill(WHITE)

        # Draw input boxes with rounded corners
        pygame.draw.rect(window, BLACK, input_box_1, 2, border_radius=border_radius_input_box)
        pygame.draw.rect(window, BLACK, input_box_2, 2, border_radius=border_radius_input_box)
        text_surface_1 = font.render(input_text_1, True, BLACK)
        window.blit(text_surface_1,
                    (input_box_1.x + 5, input_box_1.y + (input_box_1.height - text_surface_1.get_height()) // 2))
        text_surface_2 = font.render(input_text_2, True, BLACK)
        window.blit(text_surface_2,
                    (input_box_2.x + 5, input_box_2.y + (input_box_2.height - text_surface_2.get_height()) // 2))

        my_font = pygame.font.SysFont('Arial', 20)
        text_surface = my_font.render('to', False, (0, 0, 0))
        window.blit(text_surface, (395, 145))

        # Draw the cursor if the box is active and the cursor is visible
        if (active_box_1 or active_box_2) and cursor_visible:
            pygame.draw.rect(window, cursor_color, cursor)

        if button_rect.collidepoint(mouse_pos):
            button_color = BUTTON_HOVER
        else:
            button_color = BUTTON_NORMAL

        pygame.draw.rect(window, button_color, button_rect, border_radius=20)
        window.blit(button_text, button_text.get_rect(center=button_rect.center))

        if fun_fact_display:
            # Draw the textbox
            pygame.draw.rect(window, BLACK, text_box_rect, 10, border_radius)
            pygame.draw.circle(window, BLACK, circle_center, circle_radius)
            # Render the display text
            text_surface = font.render(s1, True, BLACK)
            text_x = text_box_rect.x + circle_radius + 10  # Adjust as needed
            text_y = text_box_rect.y + (text_box_rect.height - text_surface.get_height()) // 2
            window.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_pygame_window()
