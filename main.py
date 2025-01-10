import tkinter as tk
from turtle import TurtleScreen, RawTurtle
import random
from tkinter import messagebox  # 메시지 박스를 사용하기 위해 추가

# 프로그램을 만들면서 위치 수정을 쉽게 하기 위해서 기준 위치 등을 상수로 선언
BASE_X = -234
BASE_Y = -210
OFFSET_X = 2
CANVAS_WIDTH = 500  # 캔버스의 너비

# 여러 크기의 막대기를 그릴 막대기 클래스
class Bar(RawTurtle):
    def __init__(self, _canvas, _size, _bar_width, height_increase):
        super().__init__(_canvas)
        self.size = _size
        self.height_increase = height_increase
        self.penup()
        self.shape("square")
        self.turtlesize(1 + self.height_increase * _size, 0.4)  # 막대의 너비를 이전 상태로 설정하고 높이를 0.4로 설정
        self.set_color()

    def set_color(self):
        # 크기에 따라 색상 설정 (예: 크기가 클수록 빨간색, 작을수록 파란색)
        color_value = self.size / 39  # 0에서 1 사이의 값으로 변환
        self.color(color_value, 0, 1 - color_value)  # RGB 색상 설정 (0~1 범위)

    def set_position(self, position):
        # y좌표를 조정하여 막대의 높이 차이를 설정
        self.goto(BASE_X + (OFFSET_X + 10) * position, BASE_Y + (self.height_increase * 10) * self.size)  # 높이 차이를 설정

# 시각화 프로그램을 위한 클래스
class Visualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("정렬 알고리즘 시각화")
        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=500)
        self.canvas.pack()
        self.screen = TurtleScreen(self.canvas)
        self.bars = []
        self.shuffled = False  # 초기 상태를 False로 설정

        # 막대 개수를 입력할 수 있는 필드 추가
        self.num_bars_var = tk.IntVar(value=10)  # 기본값 설정
        tk.Label(self.root, text="막대 개수 (최대 40):").pack()
        tk.Entry(self.root, textvariable=self.num_bars_var).pack()

        # 높이 증가 값을 조정할 수 있는 슬라이더 추가
        self.height_increase_var = tk.DoubleVar(value=0.4)  # 기본값 설정
        tk.Label(self.root, text="막대 높이 증가 값:").pack()
        height_slider = tk.Scale(self.root, variable=self.height_increase_var, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        height_slider.pack()

        # 생성 버튼 추가
        self.create_bars_button = tk.Button(self.root, text="막대 생성", command=self.create_bars)
        self.create_bars_button.pack(pady=10)  # 버튼에 여백 추가

        # 정렬 알고리즘 선택을 위한 라디오 버튼 추가
        self.algorithm_var = tk.StringVar(value="bubble")  # 기본값 설정
        self.create_radio_buttons()

        # 섞기 버튼 추가
        self.create_shuffle_button()

        # 정렬 시작 버튼 추가
        self.create_sort_button()

    def create_bars(self):
        # 이전 막대 삭제
        for bar in self.bars:
            bar.hideturtle()  # 막대를 숨김
        self.bars.clear()  # 막대 리스트 초기화

        num_bars = self.num_bars_var.get()  # 입력된 막대 개수 가져오기

        # 막대 개수 제한 및 예외 처리
        if num_bars < 1 or num_bars > 40:
            messagebox.showwarning("경고", "막대 개수는 1에서 40 사이여야 합니다.")
            return

        bar_width = CANVAS_WIDTH / (num_bars + 1)  # 막대의 너비 계산
        height_increase = self.height_increase_var.get()  # 슬라이더에서 높이 증가 값 가져오기
        self.bars = [Bar(self.screen, i, bar_width, height_increase) for i in range(num_bars)]  # 리스트 컴프리헨션 사용
        for i, bar in enumerate(self.bars):
            bar.set_position(i)  # 정렬된 상태로 위치 설정

    def shuffle_bars(self):
        random.shuffle(self.bars)
        for i, bar in enumerate(self.bars):
            bar.set_position(i)

    def sort_bars(self):
        algorithm = self.algorithm_var.get()
        if algorithm == "bubble":
            self.bubble_sort()
        elif algorithm == "selection":
            self.selection_sort()
        # 다른 정렬 알고리즘 추가 가능

    def bubble_sort(self):
        n = len(self.bars)
        for i in range(n):
            for j in range(0, n-i-1):
                # 현재 비교 중인 막대기의 색상 변경
                self.bars[j].color("yellow")  # 현재 막대기 색상 변경
                self.bars[j+1].color("yellow")  # 다음 막대기 색상 변경

                if self.bars[j].size > self.bars[j+1].size:
                    # 막대기 위치 교환
                    self.bars[j], self.bars[j+1] = self.bars[j+1], self.bars[j]
                    self.update_bar_positions()
                    self.root.update()  # 화면 업데이트
                    self.root.after(30)  # 지연 시간 (속도 증가)

                # 색상 복원
                self.restore_colors(j, j+1)  # 원래 색상으로 복원

    def selection_sort(self):
        n = len(self.bars)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                # 현재 비교 중인 막대기의 색상 변경
                self.bars[j].color("yellow")  # 현재 막대기 색상 변경
                self.bars[min_idx].color("yellow")  # 최소 막대기 색상 변경

                if self.bars[j].size < self.bars[min_idx].size:
                    min_idx = j

                # 색상 복원
                self.restore_colors(j, min_idx)  # 원래 색상으로 복원

            # 막대기 위치 교환
            self.bars[i], self.bars[min_idx] = self.bars[min_idx], self.bars[i]
            self.update_bar_positions()
            self.root.update()  # 화면 업데이트
            self.root.after(30)  # 지연 시간 (속도 증가)

    def restore_colors(self, index1, index2):
        # 색상 복원
        self.bars[index1].set_color()  # 원래 색상으로 복원
        self.bars[index2].set_color()  # 원래 색상으로 복원

    def create_radio_buttons(self):
        tk.Label(self.root, text="정렬 알고리즘 선택:").pack()
        tk.Radiobutton(self.root, text="버블 정렬", variable=self.algorithm_var, value="bubble").pack(anchor=tk.W)
        tk.Radiobutton(self.root, text="선택 정렬", variable=self.algorithm_var, value="selection").pack(anchor=tk.W)

    def create_shuffle_button(self):
        shuffle_button = tk.Button(self.root, text="막대 섞기", command=self.shuffle_bars)
        shuffle_button.pack(pady=10)  # 버튼에 여백 추가

    def create_sort_button(self):
        sort_button = tk.Button(self.root, text="정렬 시작", command=self.sort_bars)
        sort_button.pack(pady=10)  # 버튼에 여백 추가

    def update_bar_positions(self):
        for i, bar in enumerate(self.bars):
            bar.set_position(i)

    def run(self):
        self.root.mainloop()

# 프로그램 실행
if __name__ == "__main__":
    visualizer = Visualizer()
    visualizer.run()
