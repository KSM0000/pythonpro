from PyQt5 import QtCore, QtGui, QtWidgets
import random
import sys
import time


# ui의 이름이 TTT_0임. 사실상 아래 모듈호출은 필요가 없기때문에 주석처리함.
# import TTT_0

# -----------------------------------------------------------------------------------
# 이 코드는 ui를 py로 변환한뒤 ui 클래스내에 기능 함수를 다 집어넣은 코드로써 상당히 비효율적임.
# 내부에 틱택토가 어떻게 작동되는지는 back_data 변수에 저장되며 1은 컴퓨터 2는 사람 0은 공백임.
# 1번쨰로 weight_mind_defence() 2번쨰로 defence_code() 3번째로 attack_code() 순으로 작동.
# 1번째 함수는 수동으로 전략을 추가하기 위한 함수.
# 2번쨰는 가로, 세로, 대각선을 검사하여 조건에 공격,방어를 하는 함수.
# 3번쨰는 미니맥스를 활용하여 최선의 수를 놓는 공격함수.
# 필요에 따라 미니맥스를 좀더 개선해야할 필요가 있음. (해당코드는 미니맥스와 궁합이 좋지않음.)
#
# pyqt5에 의해 생성된 대표적인 오브젝트 이름은 아래와 같다.
# TTT0 ~ TTT8 : 유저가 원하는 위치를 입력받기위한 버튼 오브젝트 이름
# logbox : 입력부 옆에 나오는 상황 전달용 메세지박스
# GameStartButton : 게임을 시작하기위한 이벤트 버튼
# GameResetButton : 게임을 초기화 하기위한 이벤트 버튼
# ExitButton : 도망쳐
# PA , CA :Player Action , Computer Action을 내맘대로 줄여적은 선공 확인용 선택버튼
#
# 중요한 핵심 변수는 아래와 같다. (모두 Ui_MainWindow 클래스 내에 귀속되어있기때문에 self는 생략하고 표기한다.)
# user_turn = 사용자 턴이 아닐때 입력을 방지하는 역할과 컴퓨터 턴일때 컴퓨터가 작동되게 하기위한 bool형 변수
# User_start , Computer_start : 누가 선공인지를 표기하는 bool형 변수.
# First_Starter_counter , Second_Starter_counter = 3x3 기준 선공은 5 후공은 4의 카운터를 가지며 횟수 추적용 int 변수
# end_counter : End_Check 함수를 지뢰마냥 깔아뒀기때문에 중복으로 작동되는것을 방지하기위한 카운터용 bool형 변수
# best_move : 미니맥스에서 판단한 최적의 경로를 저장하기위한 tuple형 변수.
# back_data : 모든 내부적 틱택토의 데이터를 저장하기위한 리스트형 변수.
# + 1은 컴퓨터 2는 사람 0은 공백임.
# dexarg(지역변수) : int형 데이터들을 str로 변환하기위한 str 변수.
# worked_counter (지역변수) : 혹시 모를 중복작동을 방지함과 동시에 함수가 작동됨을 확인하고 뒤에 다른 함수들을 작동을 금하게 하기위한 bool형 변수.
# first_mind_def , second_def : 위에 지역변수들이 return 되면서 바뀐 이름. 앞에 함수가 작동되면 뒤에 함수들이 작동안되게 하는 역할을 수행함. bool형 변수.
# com_count , count (지역변수) : count는 다른 지역변수에도 많이 사용되어 혼동될수있지만 defence 함수기준으로 유저 , 컴퓨터가 특정기준에 몇개를 그었는지를 카운팅 하기위한 int형 변수.
#
# 중요한 핵심 함수는 아래와 같다. (이번도 self는 생략한다.)
# Exit_B : 탈출용 함수.
# user_var : 코더가 직접 추가한 전역 변수를 모아둔곳이며 필요에 따라 초기화용으로도 이용하는 함수.
# Start : 시작버튼을 눌렀을때 작동되는 함수이며 GameStartButton와 이벤트로 연결되어있다.
# End_Check : 게임에 승패가 결정되었는지 확인하는 함수. 유저턴, 컴퓨터턴과 관련된 함수마다 들어가있다.
# full : End_Check 또는 minimax 함수에서 사용하기위한 함수이며 모든 보드가 꽉 찼는지 확인하는 함수이다.
# Reset : 리셋을 누를때 작동되는 함수이며 GameResetButton와 이벤트로 연결되어있다.
# processing : 컴퓨터가 틱택토 게임을 어떻게 진행할것인지를 결정하는 함수.
# get_winner : 누가 이겼는지 확인하는 코드이며 minimax와 End_Check 함수에 사용됨.
# minimax : 컴퓨터가 행동하는 3순위에 있는 코드이며 최대한 유리한곳(스코어가 높은곳)에 두는 함수
# attack_code : minimax의 함수를 실행하고 얻은 결과값을 실행하기위한 함수
# defence_code : 컴퓨터가 행동하는 2순위에 있는 코드이며 특정 조건에 따라 공격 또는 방어를 하기위한 함수.
# weight_mind_defence : 컴퓨터가 행동하는 1순위에 있는 코드이며 코더가 원하는 조건에 따라 해당위치에 두게 만드는 함수.
# counter : 누가 얼마나 뒀는지 확인하기위한 함수.
# checking : TTT 버튼들과 이벤트로 연결되어있으며 누를때마다 받는 함수인자를 통해 back_data 변수에 기록과 TTT 버튼의 텍스트를 수정하는 함수로 인자를 전달하는 역할을 하는 함수. (유저턴 중복검사도 여기서 한번 거친다.)
# TTT_User_button_SetText : TTT 버튼을 유저가 누를경우 TTT 버튼의 텍스트를 수정하는 함수이며 위에 checking과 연결되어있다.
# TTT_Com_button_SetText: 컴퓨터가 해당 위치에 뒀을경우 TTT 버튼의 텍스트를 수정하는 함수이며 weight_mind_defence , defence_code , attack_code 함수와 연결되어있다.
# TTT_Clear : Reset 함수와 연결해서 사용하기위한 버튼이며 TTT 버튼의 텍스트를 공백으로 만드는 함수이다.
# setupUi : PyQt5의 ui를 그려주고 오브젝트를 선언하기위한 자동으로 생성된 함수.
# retranslateUi : 오브젝트 이름 등..을 설정해주는 자동으로 생성된 함수.
# -----------------------------------------------------------------------------------

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(382, 397)
        MainWindow.setMinimumSize(QtCore.QSize(382, 397))
        MainWindow.setMaximumSize(QtCore.QSize(382, 397))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TTT0 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT0.setGeometry(QtCore.QRect(10, 10, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.TTT0.setFont(font)
        self.TTT0.setText("")
        self.TTT0.setFlat(True)
        self.TTT0.setObjectName("TTT0")
        self.TTT3 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT3.setGeometry(QtCore.QRect(10, 100, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT3.setFont(font)
        self.TTT3.setText("")
        self.TTT3.setFlat(True)
        self.TTT3.setObjectName("TTT3")
        self.TTT6 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT6.setGeometry(QtCore.QRect(10, 190, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT6.setFont(font)
        self.TTT6.setText("")
        self.TTT6.setFlat(True)
        self.TTT6.setObjectName("TTT6")
        self.TTT4 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT4.setGeometry(QtCore.QRect(100, 100, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT4.setFont(font)
        self.TTT4.setText("")
        self.TTT4.setFlat(True)
        self.TTT4.setObjectName("TTT4")
        self.TTT7 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT7.setGeometry(QtCore.QRect(100, 190, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT7.setFont(font)
        self.TTT7.setText("")
        self.TTT7.setFlat(True)
        self.TTT7.setObjectName("TTT7")
        self.TTT1 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT1.setGeometry(QtCore.QRect(100, 10, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT1.setFont(font)
        self.TTT1.setText("")
        self.TTT1.setFlat(True)
        self.TTT1.setObjectName("TTT1")
        self.TTT5 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT5.setGeometry(QtCore.QRect(190, 100, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT5.setFont(font)
        self.TTT5.setText("")
        self.TTT5.setFlat(True)
        self.TTT5.setObjectName("TTT5")
        self.TTT8 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT8.setGeometry(QtCore.QRect(190, 190, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.TTT8.setFont(font)
        self.TTT8.setText("")
        self.TTT8.setFlat(True)
        self.TTT8.setObjectName("TTT8")
        self.TTT2 = QtWidgets.QPushButton(self.centralwidget)
        self.TTT2.setGeometry(QtCore.QRect(190, 10, 75, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.TTT2.setFont(font)
        self.TTT2.setText("")
        self.TTT2.setFlat(True)
        self.TTT2.setObjectName("TTT2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 170, 261, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 80, 261, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(171, 10, 20, 251))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(80, 10, 20, 251))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.PA = QtWidgets.QRadioButton(self.centralwidget)
        self.PA.setGeometry(QtCore.QRect(10, 270, 121, 31))
        self.PA.setObjectName("PA")
        self.CA = QtWidgets.QRadioButton(self.centralwidget)
        self.CA.setGeometry(QtCore.QRect(10, 300, 121, 31))
        self.CA.setObjectName("CA")
        self.GameStartButton = QtWidgets.QPushButton(self.centralwidget)
        self.GameStartButton.setGeometry(QtCore.QRect(10, 330, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.GameStartButton.setFont(font)
        self.GameStartButton.setObjectName("GameStartButton")
        self.GameResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.GameResetButton.setGeometry(QtCore.QRect(120, 330, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.GameResetButton.setFont(font)
        self.GameResetButton.setObjectName("GameResetButton")
        self.logbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.logbox.setGeometry(QtCore.QRect(270, 10, 101, 311))
        self.logbox.setObjectName("logbox")
        self.ExitButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(270, 330, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ExitButton.setFont(font)
        self.ExitButton.setObjectName("ExitButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # 사실상 이 위에 코드들은 ui를 py로 변환하면서 생긴 인터페이스 코드라 볼수있다.
        # 버튼 이벤트
        self.user_var()
        self.GameStartButton.clicked.connect(self.Start)
        self.GameResetButton.clicked.connect(self.Reset)
        self.ExitButton.clicked.connect(self.Exit_B)
        # 람다함수를 통해 해당 함수를 실행함과 동시에 인자를 전달.
        # 왜 람다함수를 사용하는가? connect에서 람다를 거치지않은 함수인자를 넣을경우 오류가 발생.
        # 람다를 통해 임시적으로 함수를 만든뒤에 람다를 거쳐 함수를 인자를 전달하며 호출시키는 방식으로 해결함.
        self.TTT0.clicked.connect(lambda: self.checking('0 0'))
        self.TTT1.clicked.connect(lambda: self.checking('0 1'))
        self.TTT2.clicked.connect(lambda: self.checking('0 2'))
        self.TTT3.clicked.connect(lambda: self.checking('1 0'))
        self.TTT4.clicked.connect(lambda: self.checking('1 1'))
        self.TTT5.clicked.connect(lambda: self.checking('1 2'))
        self.TTT6.clicked.connect(lambda: self.checking('2 0'))
        self.TTT7.clicked.connect(lambda: self.checking('2 1'))
        self.TTT8.clicked.connect(lambda: self.checking('2 2'))

    def Exit_B(self):
        sys.exit()

    def user_var(self):
        # Pyqt5에서 생성된 변수가 아닌 사용자가 직접 만든 변수는 여기에 추가할것.
        # 그렇다고 지역변수를 넣으면 큰일남. 지역변수는 넣지말것.
        # 누가 먼저 시작할지 결정하는 bool 변수
        self.User_start = False
        self.Computer_start = False
        # 누가 선공이냐에 따라 아래 카운터 값을 결정하기위한 변수
        self.user_counter = 0
        self.computer_counter = 0
        # 시작하고난뒤에 종료될때까지의 카운터. (3x3 틱텍토는 총합 9칸이므로 선공5 후공4번의 턴을 가진다.)
        self.First_Starter_counter = 5
        self.Second_Starter_counter = 4
        # 유저턴이 아닐때 입력되는것을 방지하기위한 변수
        self.user_turn = False  # 이거 없으면 컴퓨터 치트씀
        self.back_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 내부에 틱택토가 어떻게 작동되는지 기록하기위함
        self.best_move = None  # 이건 미니맥스용
        self.end_counter = False  # 게임종료가 한번 선언되면 중복으로 종료메세지가 안뜨게 하기위한 카운터.
        self.logbox.append("원하시는 매치를 고르신다음 Start를 눌러주세요.")

    def Start(self, number):
        if self.User_start == True or self.Computer_start == True:
            self.logbox.append("이미 게임이 시작되었습니다.")
            return

        if self.PA.isChecked() == True:
            self.User_start = True
            self.user_counter = self.First_Starter_counter
            self.computer_counter = self.Second_Starter_counter

        elif self.CA.isChecked() == True:
            self.Computer_start = True
            self.computer_counter = self.First_Starter_counter
            self.user_counter = self.Second_Starter_counter
        self.logbox.append("게임을 시작합니다.")
        # 컴퓨터 시작일때는 가운데를 먹는 플레이로 고정시킴.
        # 가운데로 고정한 이유가 경우의수가 많기때문.
        if self.Computer_start == True and self.First_Starter_counter == 5:
            self.TTT4.setText("x")
            self.back_data[1][1] = 1
            self.counter(1)
            self.user_turn = True

        elif self.User_start == True and self.First_Starter_counter == 5:
            self.user_turn = True

    def End_Check(self):
        val = self.get_winner()  # 승자 확인용
        full = self.full()  # 무승부 확인용
        for z in range(0, 3):
            if full == 1 and self.end_counter == False:
                self.logbox.append("게임이 종료되었습니다.")
                self.logbox.append("무승부")
                self.end_counter = True
            elif val != 0 and self.end_counter == False:
                self.logbox.append("게임이 종료되었습니다.")
                self.logbox.append("{} 승리".format(val))
                self.user_turn = None
                self.end_counter = True

    def full(self):
        if self.back_data[0].count(0) == 0 and self.back_data[1].count(0) == 0 and self.back_data[2].count(0) == 0:
            return 1

    def Reset(self):
        self.logbox.clear()
        self.user_var()
        self.TTT_Clear()

    def processing(self):
        # 주석처리된 코드들은 필요성이 없거나 비효율적이라 주석처리함.
        """
        if self.user_turn == False and self.back_data[1][1] == 0 and self.computer_counter == 4:
            self.back_data[1][1] = 1
            self.TTT4.setText("X")
            self.user_turn = True

        elif self.user_turn == False and self.back_data[1][1] != 0 and self.computer_counter == 4:
            while True:
                f=random.randrange(0,4)
                if f == 0 and self.back_data[0][0] == 0:
                    self.back_data[0][0] = 1
                    self.TTT_Com_button_SetText("0 0")
                    self.counter(1)
                    break
                elif f == 1 and self.back_data[0][2] == 0:
                    self.back_data[0][2] = 1
                    self.TTT_Com_button_SetText("0 2")
                    self.counter(1)
                    break
                elif f == 2 and self.back_data[2][0] == 0:
                    self.back_data[2][0] = 1
                    self.TTT_Com_button_SetText("2 0")
                    self.counter(1)
                    break
                elif f == 3 and self.back_data[2][2] == 0:
                    self.back_data[2][2] = 1
                    self.TTT_Com_button_SetText("2 2")
                    self.counter(1)
                    break
            self.user_turn = True
"""
        # 유저턴인지 꼭 확인코드를 넣어야한다. 안넣으면 혼자 치트씀.
        if self.user_turn == False:
            first_mind_def = self.weight_mind_defence()
            if first_mind_def == False:
                Second_Def = self.defence_code()
                if Second_Def == False:
                    self.attack_code()
            self.user_turn = True
            self.End_Check()
            # 아래코드는 디펜스코드와 공격코드를 어떻게 연결해야할지 첫번쨰로 구상했던 코드.
            """
            worked=False
            worked=self.defence_code()
            print(worked)
            if worked == True:
                self.user_turn = True
            else:
                self.attack_code()
                self.user_turn = True
            self.End_Check()
            """

    # 미니맥스를 사용하기위한 승리 조건표 , 승자확인용으로도 사용된다.
    def get_winner(self):
        # 가로, 세로는 반복문을 돌림. 대각선은 깡으로 2가지 경우의수를 나타냄.
        for i in range(0, 3):
            # 가로 방향
            if self.back_data[i][0] != 0 and self.back_data[i][0] == self.back_data[i][1] == self.back_data[i][2]:
                return self.back_data[i][0]
            # 세로 방향
            if self.back_data[0][i] != 0 and self.back_data[0][i] == self.back_data[1][i] == self.back_data[2][i]:
                return self.back_data[0][i]
        # 대각선
        if self.back_data[0][0] != 0 and self.back_data[0][0] == self.back_data[1][1] == self.back_data[2][2]:
            return self.back_data[0][0]
        if self.back_data[0][2] != 0 and self.back_data[0][2] == self.back_data[1][1] == self.back_data[2][0]:
            return self.back_data[0][2]
        return 0

    def minimax(self, board, depth, is_max):
        # 보드의 승자가 있거나 비었으면 점수를 반환
        winner = self.get_winner()
        if winner == '1':
            return -10 + depth
        elif winner == '2':
            return 10 - depth
        elif self.full == 1:
            return 0

        # 내차례(맥스)면 놓고 아니면 (미니)가 놓는 방식.
        if is_max == True:
            best_score = -float('inf')
            for i in range(0, 3):
                for j in range(0, 3):
                    if board[i][j] == 0:
                        board[i][j] = 1
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = 0
                        if score > best_score:
                            best_score = score
                            self.best_move = (i, j)
            return best_score
        else:
            best_score = float('inf')
            for i in range(0, 3):
                for j in range(0, 3):
                    if board[i][j] == 0:
                        board[i][j] = 2
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = 0
                        if score < best_score:
                            best_score = score
                            self.best_move = (i, j)
            return best_score

    # 공격코드 미니맥스를 채용함.
    def attack_code(self):
        best = self.minimax(self.back_data, 0, True)
        self.back_data[self.best_move[0]][self.best_move[1]] += 1
        dexarg = str(self.best_move[0]) + " " + str(self.best_move[1])
        self.TTT_Com_button_SetText(dexarg)
        self.counter(1)

    # 디펜스 코드 , 만약 한 라인에 자신의 흔적이 2개이상이면 공격하게 되어있다.
    def defence_code(self):
        worked_counter = False
        # 가로줄 검사후 디펜스
        for z in range(0, 3):
            if self.back_data[z].count(1) >= 2 and self.back_data[z].count(2) == 0:
                for i in range(0, 3):
                    if self.back_data[z][i] == 0 and worked_counter == False:
                        self.back_data[z][i] = 1
                        dexarg = str(z) + " " + str(i)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
            if self.back_data[z].count(2) >= 2 and self.back_data[z].count(1) == 0:
                for i in range(0, 3):
                    if self.back_data[z][i] == 0 and worked_counter == False:
                        self.back_data[z][i] = 1
                        dexarg = str(z) + " " + str(i)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
        # 세로줄 검사후 디펜스
        for x in range(0, 3):
            count = 0
            com_count = 0
            for i in range(0, 3):
                if self.back_data[i][x] == 2:
                    count += 1
                elif self.back_data[i][x] == 1:
                    com_count += 1
                if count == 0 and com_count >= 2:
                    for i in range(0, 3):
                        if self.back_data[i][x] == 0 and worked_counter == False:
                            self.back_data[i][x] = 1
                            dexarg = str(i) + " " + str(x)
                            self.TTT_Com_button_SetText(dexarg)
                            worked_counter = True
                            break
                if count >= 2 and com_count == 0:
                    for i in range(0, 3):
                        if self.back_data[i][x] == 0 and worked_counter == False:
                            self.back_data[i][x] = 1
                            dexarg = str(i) + " " + str(x)
                            self.TTT_Com_button_SetText(dexarg)
                            worked_counter = True
                            break
        # 대각선 검사후 디펜스
        calc_weight = 2
        count = 0
        com_count = 0
        for x in range(0, 3):
            if self.back_data[x][calc_weight - x] == 2:
                count += 1
            elif self.back_data[x][calc_weight - x] == 1:
                com_count += 1
            if com_count >= 2 and count == 0:
                for x in range(0, 3):
                    calc_weight = 2
                    if self.back_data[x][calc_weight - x] == 0 and worked_counter == False:
                        self.back_data[x][calc_weight - x] = 1
                        dexarg = str(x) + " " + str(calc_weight - x)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
            if count >= 2 and com_count == 0:
                for x in range(0, 3):
                    calc_weight = 2
                    if self.back_data[x][calc_weight - x] == 0 and worked_counter == False:
                        self.back_data[x][calc_weight - x] = 1
                        dexarg = str(x) + " " + str(calc_weight - x)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
        count = 0
        com_count = 0
        for x in range(0, 3):
            if self.back_data[x][x] == 2:
                count += 1
            elif self.back_data[x][x] == 1:
                com_count += 1
            if com_count >= 2 and count == 0:
                for x in range(0, 3):
                    if self.back_data[x][x] == 0 and worked_counter == False:
                        self.back_data[x][x] = 1
                        dexarg = str(x) + " " + str(x)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
            if count >= 2 and com_count == 0:
                for x in range(0, 3):
                    if self.back_data[x][x] == 0 and worked_counter == False:
                        self.back_data[x][x] = 1
                        dexarg = str(x) + " " + str(x)
                        self.TTT_Com_button_SetText(dexarg)
                        worked_counter = True
                        break
        # 만약 디펜스 코드가 발생하지않을경우 반환후 공격코드(미니맥스)로 전환
        if worked_counter == False:
            return False
        else:
            return True

    def counter(self, number):
        # 무승부를 위한 코드. 각각 기회횟수가 0이되면 종료된다.
        # 사실상 버려진 코드에 가깝다.
        if self.user_counter == 0:
            self.End_Check()
        elif self.computer_counter == 0:
            self.End_Check()

        if number == 0:
            self.user_counter -= 1
        elif number == 1:
            self.computer_counter -= 1

    # 디펜스 코드나 미니맥스코드를 거친뒤에도 뚫린 전략은 여기서 수동으로 추가해준다.
    # 무조건 맨 마지막에는 자기가 놓을 자리를 추가함으로써 무한적으로 반복되는 현상을 제거한다.
    # 코드의 흐름상 무조건적으로 첫번째 위치의 전략이 우선시 된다.
    def weight_mind_defence(self):
        worked_counter = False
        if self.back_data[1][1] == 0:
            self.back_data[1][1] = 1
            self.TTT_Com_button_SetText("1 1")
            worked_counter = True
        elif self.back_data[0][0] == 1 and self.back_data[1][1] == 2 and self.back_data[2][2] == 2 and \
                self.back_data[0][2] == 0:
            self.back_data[0][2] = 1
            self.TTT_Com_button_SetText("0 2")
            worked_counter = True
        elif self.back_data[0][0] == 2 and self.back_data[1][1] == 1 and self.back_data[0][1] == 0:
            self.back_data[0][1] = 1
            self.TTT_Com_button_SetText("0 1")
            worked_counter = True
        elif self.back_data[0][0] == 1 and self.back_data[2][1] == 2 and self.back_data[0][2] == 2 and \
                self.back_data[1][1] == 0:
            self.back_data[1][1] = 1
            self.TTT_Com_button_SetText("1 1")
            worked_counter = True
        elif self.back_data[0][0] == 2 and self.back_data[0][1] == 1 and self.back_data[0][2] == 2 and \
                self.back_data[1][1] == 0:
            self.back_data[1][1] = 1
            self.TTT_Com_button_SetText("1 1")
            worked_counter = True
        return worked_counter

    def checking(self, clicked_number):
        list_num1, list_num2 = map(int, clicked_number.split())
        if self.user_turn == True and self.back_data[list_num1][list_num2] == 0:
            self.back_data[list_num1][list_num2] = 2
            self.TTT_User_button_SetText(clicked_number)
            self.counter(0)
            self.user_turn = False
            self.End_Check()
            self.processing()

    def TTT_User_button_SetText(self, clicked_number):
        if clicked_number == "0 0":
            self.TTT0.setText("O")
        elif clicked_number == "0 1":
            self.TTT1.setText("O")
        elif clicked_number == "0 2":
            self.TTT2.setText("O")
        elif clicked_number == "1 0":
            self.TTT3.setText("O")
        elif clicked_number == "1 1":
            self.TTT4.setText("O")
        elif clicked_number == "1 2":
            self.TTT5.setText("O")
        elif clicked_number == "2 0":
            self.TTT6.setText("O")
        elif clicked_number == "2 1":
            self.TTT7.setText("O")
        elif clicked_number == "2 2":
            self.TTT8.setText("O")

    def TTT_Com_button_SetText(self, clicked_number):
        if clicked_number == "0 0":
            self.TTT0.setText("X")
        elif clicked_number == "0 1":
            self.TTT1.setText("X")
        elif clicked_number == "0 2":
            self.TTT2.setText("X")
        elif clicked_number == "1 0":
            self.TTT3.setText("X")
        elif clicked_number == "1 1":
            self.TTT4.setText("X")
        elif clicked_number == "1 2":
            self.TTT5.setText("X")
        elif clicked_number == "2 0":
            self.TTT6.setText("X")
        elif clicked_number == "2 1":
            self.TTT7.setText("X")
        elif clicked_number == "2 2":
            self.TTT8.setText("X")

    def TTT_Clear(self):
        self.TTT0.setText(" ")
        self.TTT1.setText(" ")
        self.TTT2.setText(" ")
        self.TTT3.setText(" ")
        self.TTT4.setText(" ")
        self.TTT5.setText(" ")
        self.TTT6.setText(" ")
        self.TTT7.setText(" ")
        self.TTT8.setText(" ")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tic-Tac-Toe"))
        self.PA.setText(_translate("MainWindow", "플레이어 선공"))
        self.CA.setText(_translate("MainWindow", "컴퓨터 선공"))
        self.GameStartButton.setText(_translate("MainWindow", "시작"))
        self.GameResetButton.setText(_translate("MainWindow", "리셋"))
        self.ExitButton.setText(_translate("MainWindow", "종료"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())