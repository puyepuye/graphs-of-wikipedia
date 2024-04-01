import pygame
import sys
from visualize_helper import *
from graph_object import *


def run_pygame_window():
    pygame.init()
    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Graph Of Wikipedia')

    # Logo
    # Load the logo image
    # logo_image = pygame.image.load('path_to_logo_image.png')  # Replace with your logo image path
    # logo_size = (100, 100)  # Desired dimensions (width, height) of the logo
    # logo_image = pygame.transform.scale(logo_image, logo_size)
    # logo_rect = logo_image.get_rect(center=(window_width // 2, logo_size[1] // 2))

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
    not_found = False
    no_vertex = False
    toggle1, toggle2 = True, False
    # Create a button
    button_font = pygame.font.SysFont(None, 30)
    button_rect = pygame.Rect(window_width // 2 - 125, window_height // 2 - 40, 250, 50)
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
    BLACK = (0, 0, 0)
    DARK_GREEN = (0, 100, 0)
    rect_width = 700  # Adjusted for wider rectangle
    rect_height = 40
    border_radius = 20
    circle_radius = rect_height // 1.7
    border_thickness = 2  # Thinner border
    check1 = (180, 238)
    check2 = (450, 238)
    check_r = 9
    bound = 50

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
                    not_found, fun_fact_display, no_vertex = False, False, False
                    active_box_1, active_box_2 = True, False
                    cursor.topleft = (input_box_1.x + font.size(input_text_1)[0] + 5, input_box_1.y + 5)
                elif input_box_2.collidepoint(event.pos):
                    not_found, fun_fact_display, no_vertex = False, False, False
                    active_box_1, active_box_2 = False, True
                    cursor.topleft = (input_box_2.x + font.size(input_text_2)[0] + 5, input_box_2.y + 5)
                elif button_rect.collidepoint(event.pos):
                    print(f'Clicked with text 1: {input_text_1} and text 2: {input_text_2}')
                    g_g, g_d = load_gow_json('../database/big_graph.json')
                    if input_text_1 in g_d and input_text_2 in g_d:
                        if BFS_path(g_d, input_text_1, input_text_2) != []:
                            all_paths = visualize_paths(g_g, g_d, input_text_1, input_text_2, bound)
                            summary_dict = summary(g_d, input_text_1, input_text_2, all_paths)
                            if bound is not None:
                                summary_dict.pop('num_of_paths')
                            else:
                                summary_dict.pop('all_num_of_paths')
                            fact = [v for v in summary_dict.values()]
                            fun_fact_display = True
                        else:
                            not_found = True
                    else:
                        no_vertex = True

                    # Draw the text content in the text box
                    # You need to define display_text somewhere above, e.g., display_text = "Some text"
                    my_font = pygame.font.SysFont('Arial', 20)
                    text_surface = my_font.render('to', False, (0, 0, 0))
                    window.blit(text_surface, (0, 0))
                elif pygame.math.Vector2(mouse_pos).distance_to(pygame.math.Vector2(check1)) <= check_r:
                    toggle1 = True
                    toggle2 = False
                    bound = 50
                elif pygame.math.Vector2(mouse_pos).distance_to(pygame.math.Vector2(check2)) <= check_r:
                    toggle2 = True
                    toggle1 = False
                    bound = None
                else:
                    active_box_1, active_box_2 = False, False

                pygame.display.flip()
            elif event.type == pygame.KEYDOWN:
                not_found, fun_fact_display, no_vertex = False, False, False
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

        check_font = pygame.font.SysFont('Arial', 12)
        # Checkbox 1
        pygame.draw.circle(window, (200, 200, 200), check1, check_r)
        pygame.draw.circle(window, BLACK, check1, check_r, 1)
        check_text1 = check_font.render("Show top 50 paths (faster)", True, BLACK)
        window.blit(check_text1, (check1[0] + check_r + 10, check1[1] - check_text1.get_height() // 2))
        # Checkbox 2
        pygame.draw.circle(window, (200, 200, 200), check2, check_r)
        pygame.draw.circle(window, BLACK, check2, check_r, 1)
        check_text2 = check_font.render("Show all paths", True, BLACK)
        window.blit(check_text2, (check2[0] + check_r + 10, check2[1] - check_text2.get_height() // 2))

        if toggle1:
            pygame.draw.circle(window, BLACK, check1, check_r)
        if toggle2:
            pygame.draw.circle(window, BLACK, check2, check_r)

        # Draw the cursor if the box is active and the cursor is visible
        if (active_box_1 or active_box_2) and cursor_visible:
            pygame.draw.rect(window, cursor_color, cursor)

        if button_rect.collidepoint(mouse_pos):
            button_color = BUTTON_HOVER
        else:
            button_color = BUTTON_NORMAL

        pygame.draw.rect(window, button_color, button_rect, border_radius=20)
        window.blit(button_text, button_text.get_rect(center=button_rect.center))
        start_y = (window_height // 2) - (5 * rect_height) // 9 + 50

        if no_vertex:
            twenty_font = pygame.font.Font(None, 20)  # Using Pygame's default font
            text_surface = twenty_font.render(f'Input Page not found in graph', True, RED)
            window.blit(text_surface, (window_width//2 - 90, 60))

        if not_found:
            twenty_font = pygame.font.Font(None, 20)  # Using Pygame's default font
            text_surface = twenty_font.render(f'Path not found', True, RED)
            window.blit(text_surface, (window_width//2 - 45, 60))

        if fun_fact_display:
            # fun_fact_icons = ["facts_icon/1.png"]
            for i in range(len(fact)):
                rect_x = (window_width // 2) - 200 - circle_radius * 2 - 100 # Adjusted for circle to start more on the left
                rect_y = start_y + i * (rect_height + 10)  # 10 pixels space between each fact box

                # Create the rectangle for the text box
                text_box_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                circle_center = (rect_x + 10, rect_y + circle_radius - 2.5)

                # Draw the textbox
                pygame.draw.rect(window, DARK_GREEN, text_box_rect, border_thickness, border_radius)
                pygame.draw.circle(window, DARK_GREEN, circle_center, circle_radius)  # Dark green circle
                  # Adjust this value to change the font size
                twenty_font = pygame.font.Font(None, 25)  # Using Pygame's default font

                # Render the display text
                text_surface = twenty_font.render(fact[i], True, BLACK)
                text_x = text_box_rect.x + circle_radius * 2 - 5  # Adjusted to position text with the new circle position
                text_y = text_box_rect.y + (text_box_rect.height - text_surface.get_height()) // 2
                window.blit(text_surface, (text_x, text_y))
                bg = pygame.image.load(f'facts_icon/{i+1}.png')
                bg = pygame.transform.scale(bg, (circle_radius * 2, circle_radius * 2))
                window.blit(bg, (circle_center[0] - circle_radius, circle_center[1] - circle_radius))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_pygame_window()
