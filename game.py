import curses
import time
import sys
import random

curses.initscr()

curses.noecho()
curses.cbreak(True)
curses.curs_set(False)

win = curses.newwin(20, 40, 2, 2)
win.keypad(True)

win.clear()
win.border(0)
win.nodelay(False)    

while True:
    snake = [[1, 1], [2, 1], [3, 1]]
    food = [[10, 10]]

    key = curses.KEY_RIGHT

    with open("highscores.txt", "r") as file:
        highscore = int(file.read().strip("\n"))

    win.addstr(8, 17, "SNAKE", curses.A_BOLD)
    win.addstr(10, 9, "PRESS ANY KEY TO BEGIN", curses.A_REVERSE)
    win.refresh()
    
    anykey = win.getch()
    if anykey == 27:
        curses.echo()
        curses.cbreak(False)
        curses.curs_set(True)
        curses.endwin()
        
        break

    win.hline(8, 17, " ", 5)
    win.hline(10, 9, " ", 22)

    win.nodelay(True)

    paused = False

    win.hline(19, 17, " ", 6)
    win.addstr(19, 18, "PLAY")

    while True:
        if snake[-1] in snake[:-1]:
            break

        user_input = win.getch()
        if user_input == 27:
            break

        if user_input == 32:
            if paused == True:
                paused = False
                win.hline(19, 17, " ", 6)
                win.addstr(19, 18, "PLAY")
            else:
                paused = True
                win.addstr(19, 17, "PAUSED")

        win.addstr(0, 1, "Score: " + str((len(snake) - 3) * 10))

        timeout = 0.1 - (len(snake) / 500)

        if (len(snake) - 3) * 10 > highscore: highscore = (len(snake) - 3) * 10
        win.addstr(0, 20, "Highscore: " + str(highscore))

        if not paused:
            if (user_input == curses.KEY_RIGHT and key != curses.KEY_LEFT) or (user_input == curses.KEY_LEFT and key != curses.KEY_RIGHT) or (user_input == curses.KEY_UP and key != curses.KEY_DOWN) or (user_input == curses.KEY_DOWN and key != curses.KEY_UP):
                key = user_input

            if key == curses.KEY_RIGHT:
                snake.append([snake[-1][0] + 1, snake[-1][1]])

            if key == curses.KEY_LEFT:
                snake.append([snake[-1][0] - 1, snake[-1][1]])
            
            if key == curses.KEY_UP:
                snake.append([snake[-1][0], snake[-1][1] - 1])
            
            if key == curses.KEY_DOWN:
                snake.append([snake[-1][0], snake[-1][1] + 1])

            if snake[-1][0] > 38:
                snake[-1][0] = 1
            
            if snake[-1][0] < 1:
                snake[-1][0] = 38

            if snake[-1][1] > 18:
                snake[-1][1] = 1
            
            if snake[-1][1] < 1:
                snake[-1][1] = 18

            if snake[-1] not in food:
                win.addch(snake[0][1], snake[0][0], " ")
                snake.pop(0)
            
            else:
                food.pop()
                food.append([random.randint(1, 38), random.randint(1, 18)])

            for segment in snake:
                win.addch(segment[1], segment[0], "O")

            for f in food:
                win.addch(f[1], f[0], "#")

            win.refresh()
        time.sleep(timeout)

    with open("highscores.txt", "w+") as file:
        file.write(str(highscore))

    win.clear()
    win.border(0)
    win.nodelay(False)

    win.addstr(8, 15, "YOU DIED!", curses.A_BOLD)
    win.addstr(10, 14, "SCORE: " + str((len(snake) - 3) * 10))
    win.addstr(11, 12, "HIGHSCORE: " + str(highscore))
    
    if (len(snake) - 3) * 10 == highscore:
        win.addstr(13, 12, "NEW HIGHSCORE!", curses.A_REVERSE)

    win.refresh()
    time.sleep(4)

    win.hline(8, 15, " ", 9)
    win.hline(10, 14, " ", 24)
    win.hline(11, 12, " ", 26)
    win.hline(13, 12, " ", 26)