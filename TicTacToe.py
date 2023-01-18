import secrets
import itertools


# 定义函数
def gameBoard(curr_board, player=0, row=0, col=0, just_display=False):
    try:
        if not just_display:
            print(f"{player}选手落子")
            # 1. 投子
            curr_board[row][col] = player

            # 2. 显示/刷新面板
            print('   ', end='')
            for i in range(board_size):
                print(i, end='  ')
            print()
            for row_num, row in enumerate(curr_board):
                print(row_num, row)
    except IndexError:  # 捕获特定异常（实际不会触发）
        print(f"Did you attempt to choose a row or column outside the range of 0 to {board_size - 1}? (IndexError)")
    except Exception as e:  # 捕获所有异常（实际不会触发）
        print(str(e))
    return curr_board


# 1. 初始化
playing = True
player = (1, 2)
# 初始化游戏面板
# 增加棋盘的伸缩度
while playing:
    board_size = int(input("What size of the board? "))
    board = [[0] * board_size for _ in range(board_size)]  # 初始化棋盘
    # 随机选择先手
    curr_player = secrets.choice(player)
    print(f"current player: {curr_player}")
    # 询问落子位置
    row_choice = input("which row? ")
    while row_choice not in [str(i) for i in range(board_size)]:
        row_choice = input(f"Which row? [0 - {board_size - 1}]: ")
    col_choice = input("which column? ")
    while col_choice not in [str(i) for i in range(board_size)]:
        col_choice = input(f"Which column? [0 - {board_size - 1}]: ")
    row_choice = int(row_choice)
    col_choice = int(col_choice)
    # 玩家落子
    board = gameBoard(board, player=curr_player, row=row_choice, col=col_choice)
    # 切换玩家
    curr_player = 3 - curr_player

    # 如何算赢
    def isWin(curr_board):
        def all_same(l):
            """
            判断列表l中的所有元素是否相等，且不为0
            返回值：相等且不为0，True；否则false
            """
            flag = False

            if l[0] != 0 and l.count(l[0]) == len(row):
                flag = True

            return flag

        # 1. 行方向出现赢家
        for row in curr_board:
            if all_same(row):
                print(f"Player {row[0]} is the winner! -")
                return True
        # 2. 列方向出现赢家
        for col in range(board_size):
            check = []
            for row in curr_board:
                check.append(row[col])
            if all_same(check):
                print(f"Player {check[0]} is the winner! |")
                return True
        # 3. 主对角线出现赢家
        diags = []
        for idx in range(board_size):
            diags.append(curr_board[idx][idx])

        if all_same(diags):
            print(f"Player {diags[0]} is the winner! \\")
            return True
        # 4. 副对角线出现赢家
        diags = []
        """
            row_idx = idx
            col_idx = board_size - idx
        """
        for idx, reverse_idx in enumerate(reversed(range(board_size))):
            diags.append(curr_board[idx][reverse_idx])
        if all_same(diags):
            print(f"Player {diags[0]} is the winner! /")
            return True
        return False

    # 是否再来一局
    def if_restart():
        global playing
        play_again = input("Would you like to play again? [Yes or No]: ")
        if play_again.lower() == "yes":
            print("Restart!")
        elif play_again.lower() == "no":
            print("Goodbye!")
            playing = False
        else:
            print("Not a valid answer, sorry.")
            playing = False

    # 选手投子
    won = isWin(board)
    while not won:
        print(f"current player: {curr_player}")

        # 解决重复落子问题
        valid = False
        while not valid:
            row_choice = input("Which row?")
            while row_choice not in [str(i) for i in range(board_size)]:
                row_choice = input(f"Which row? [0 - {board_size - 1}]: ")

            col_choice = input("Which column?")
            while col_choice not in [str(i) for i in range(board_size)]:
                col_choice = input(f"Which column? [0 - {board_size - 1}]: ")

            row_choice = int(row_choice)
            col_choice = int(col_choice)
            if board[row_choice][col_choice] == 0:  # 若此处为0，说明还未有人在此处落子，选择合法
                valid = True

        # 落子，更新棋盘
        board = gameBoard(board, player=curr_player, row=row_choice, col=col_choice)

        # 判断是否出现赢家
        won = isWin(board)
        if won:
            print("Game Over!")
            if_restart()
            break
        else:
            # 判断棋盘是否落满棋子
            grids = []
            for x in board:
                grids.extend(x)
            if 0 not in grids:
                print("All the grids were occupied. Game over!")
                if_restart()
                break

        # 轮换玩家
        curr_player = 3 - curr_player
