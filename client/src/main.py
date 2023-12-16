import curses

# Global state
current_state = "start_screen"
authenticated = False

def draw_textbox(stdscr, prompt_string):
    curses.echo() 
    stdscr.addstr(prompt_string)
    input = stdscr.getstr().decode()
    curses.noecho()
    return input

def draw_menu(stdscr):
    global current_state, authenticated
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Loop where k is the last character pressed
    while (k != ord('q')):  # Press 'q' to exit
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if current_state == "start_screen":
            menu = ["1. Sign In", "2. Sign Up"] if not authenticated else ["1. Sign Out", "2. Send Mail", "3. See Mails"]
            for idx, row in enumerate(menu):
                x = width//2 - len(row)//2
                y = height//2 - len(menu)//2 + idx
                stdscr.addstr(y, x, row)

            if k == ord('1'):
                current_state = "auth"
            elif k == ord('2') and not authenticated:
                current_state = "register"
            elif k == ord('2') and authenticated:
                current_state = "send_mail"
            elif k == ord('3'):
                current_state = "see_mails"

        elif current_state == "auth":
            username = draw_textbox(stdscr, "Username: ")
            password = draw_textbox(stdscr, "Password: ")
            # Here, handle authentication
            authenticated = True  # Assuming authentication success
            current_state = "start_screen"

        elif current_state == "register":
            # Handle registration process
            # After successful registration, set authenticated = True
            current_state = "start_screen"

        elif current_state == "send_mail":
            # Handle sending mail
            current_state = "start_screen"

        elif current_state == "see_mails":
            # Handle displaying mails
            stdscr.getch() # Wait for any key press
            current_state = "start_screen"

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

# Initialize curses
def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
