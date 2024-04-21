def tic():
    maps = [1,2,3,
            4,5,6,
            7,8,9]

    # Инициализация победных линий
    victories = [[0,1,2],
                 [3,4,5],
                 [6,7,8],
                 [0,3,6],
                 [1,4,7],
                 [2,5,8],
                 [0,4,8],
                 [2,4,6]]

    # Вывод карты на экран
    def print_maps():
        print(maps[0], end = " ")
        print(maps[1], end = " ")
        print(maps[2])

        print(maps[3], end = " ")
        print(maps[4], end = " ")
        print(maps[5])

        print(maps[6], end = " ")
        print(maps[7], end = " ")
        print(maps[8])

    # Сделать ход в ячейку
    def step_maps(step,symbol):
        ind = maps.index(step)
        maps[ind] = symbol

    # Получить текущий результат игры
    def get_result():
        win = ""

        for i in victories:
            if maps[i[0]] == "X" and maps[i[1]] == "X" and maps[i[2]] == "X":
                win = "X"
            if maps[i[0]] == "O" and maps[i[1]] == "O" and maps[i[2]] == "O":
                win = "O"

        return win

    #Искусственный интеллект: поиск линии с нужным количеством X и O на победных линиях
    def check_line(sum_O,sum_X):

        step = ""
        for line in victories:
            o = 0
            x = 0

            for j in range(0,3):
                if maps[line[j]] == "O":
                    o = o + 1
                if maps[line[j]] == "X":
                    x = x + 1

            if o == sum_O and x == sum_X:
                for j in range(0,3):
                    if maps[line[j]] != "O" and maps[line[j]] != "X":
                        step = maps[line[j]]

        return step

    #Искусственный интеллект: выбор хода
    def AI():

        step = ""

        # 1) если на какой либо из победных линий 2 свои фигуры и 0 чужих - ставим
        step = check_line(2,0)

        # 2) если на какой либо из победных линий 2 чужие фигуры и 0 своих - ставим
        if step == "":
            step = check_line(0,2)

        # 3) если 1 фигура своя и 0 чужих - ставим
        if step == "":
            step = check_line(1,0)

        # 4) центр пуст, то занимаем центр
        if step == "":
            if maps[4] != "X" and maps[4] != "O":
                step = 5

        # 5) если центр занят, то занимаем первую ячейку
        if step == "":
            if maps[0] != "X" and maps[0] != "O":
                step = 1

        return step

    # Основная программа
    game_over = False
    human = True

    while game_over == False:

        # 1. Показываем карту
        print_maps()

        # 2. Спросим у играющего куда делать ход
        if human == True:
            symbol = "X"
            step = int(input("Человек, ваш ход: "))
        else:
            print("Компьютер делает ход: ")
            symbol = "O"
            step = AI()

        # 3. Если компьютер нашел куда сделать ход, то играем. Если нет, то ничья.
        if step != "":
            step_maps(step,symbol) # делаем ход в указанную ячейку
            win = get_result() # определим победителя
            if win != "":
                game_over = True
            else:
                game_over = False
        else:
            print("Ничья!")
            game_over = True
            win = "дружба"

        human = not(human)

    # Игра окончена. Покажем карту. Объявим победителя.
    print_maps()
    print("Победил", win)
