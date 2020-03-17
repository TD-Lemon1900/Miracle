# 给定m和r，使用拟人拟物法解不等圆packing问题

import numpy as np
import random
from matplotlib import pyplot as plt
import seaborn
import heapq


class circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.nei = 0

    def show(self):
        plot_circle(self.x, self.y, self.r)


def plot_circle(xx, yy, r):
    theta = np.arange(0, 2 * np.pi, 0.01)
    x = xx + r * np.cos(theta)
    y = yy + r * np.sin(theta)
    plt.plot(x, y)


def dis(x1, x2, y1,y2):             # 计算两点间的距离
    dis = ((x1 - x2)**2+(y1 - y2)**2)**0.5
    return dis


def find_min_nei(circles):           # 找到圆集合中邻居最少的元素
    min = 10
    nei_num = 0
    for i in range(len(circles)):
        nei = 0
        for j in range(len(circles)):
            if i == j: continue
            if circles[i].r + circles[j].r - dis(circles[i].x, circles[j].x, circles[i].y, circles[j].y) == 0:
                nei = nei +1
        if abs(circles[i].x)+ circles[i].r >= 1:
            nei = nei +1
        if abs(circles[i].y) + circles[i].r >= 1:
            nei = nei +1
        if nei < min:
            min = nei
            nei_num = i
    return nei_num


def expand(circles):               # 保证各个圆与边界与其他圆相切
    for i in range(len(circles)):
        bool = 1
        min = 3
        for j in range(len(circles)):
            if i == j : continue
            if circles[i].r + circles[j].r - dis(circles[i].x, circles[j].x, circles[i].y, circles[j].y)>=0:
                bool = 0
            else:
                if -(circles[i].r + circles[j].r - dis(circles[i].x, circles[j].x, circles[i].y, circles[j].y)) < min:
                    min = -(circles[i].r + circles[j].r - dis(circles[i].x, circles[j].x, circles[i].y, circles[j].y))
        if abs(circles[i].x)+ circles[i].r >= 1:
            bool = 0
        else:
            if 1-abs(circles[i].x) - circles[i].r < min:
                min = 1-abs(circles[i].x) - circles[i].r
        if abs(circles[i].y) + circles[i].r >= 1:
            bool = 0
        else:
            if 1-abs(circles[i].y) - circles[i].r < min:
                min = 1-abs(circles[i].y) - circles[i].r
        if bool ==1:
            circles[i].r = circles[i].r + min


def area(circles):
    area=0
    for i in range(len(circles)):
        area = area + np.pi*(circles[i].r**2)
    return area


def nosmall_step(circles, UU):                # 拟人法，防止陷入最小值陷阱
    UU = np.sum(UU, axis=0)
    for i in range(len(circles)):
        UU[i] = UU[i]/(circles[i].r**2)
    UU = list(UU)
    max_list = list(map(UU.index, heapq.nlargest(5, UU)))
    circles[max_list[0]].x = circles[max_list[0]].r-1
    circles[max_list[0]].y = 1-circles[max_list[0]].r
    circles[max_list[1]].x = 1-circles[max_list[1]].r
    circles[max_list[1]].y = 1 - circles[max_list[1]].r
    circles[max_list[2]].x = 1 - circles[max_list[2]].r
    circles[max_list[2]].y = circles[max_list[2]].r - 1
    circles[max_list[3]].x = circles[max_list[3]].r - 1
    circles[max_list[3]].y = circles[max_list[3]].r - 1
    circles[max_list[4]].x = 0
    circles[max_list[4]].y = 0


def  update(circles, step):            # 更新函数，梯度下降使系统势能最小
    U = [[0 for i in range(m)] for i in range(m)]
    UW = 0
    move_vector = [0., 0.]
    for i in range(len(circles)):
        if circles[i].x + circles[i].r > 1:
            L = circles[i].r - 1 + circles[i].x
            UW = UW + L ** 2
            force = [0, -1]
            if L < 0.001:
                L = L * 100
            move_vector[0] = move_vector[0] + L * force[0]
            move_vector[1] = move_vector[1] + L * force[1]
        if circles[i].x - circles[i].r < -1:
            L = circles[i].r - 1 - circles[i].x
            UW = UW + L ** 2
            force = [0, 1]
            if L < 0.001:
                L = L * 100
            move_vector[0] = move_vector[0] + L * force[0]
            move_vector[1] = move_vector[1] + L * force[1]
        if circles[i].y + circles[i].r > 1:
            L = circles[i].r - 1 + circles[i].y
            UW = UW + L ** 2
            force = [-1, 0]
            if L < 0.001:
                L = L * 100
            move_vector[0] = move_vector[0] + L * force[0]
            move_vector[1] = move_vector[1] + L * force[1]
        if circles[i].y - circles[i].r < -1:
            L = circles[i].r - 1 - circles[i].y
            UW = UW+ L ** 2
            force = [1, 0]
            if L < 0.01:
                L = L * 10
            move_vector[0] = move_vector[0] + L * force[0]
            move_vector[1] = move_vector[1] + L * force[1]
        for j in range(len(circles)):
            if i == j: continue
            L = circles[i].r + circles[j].r - dis(circles[i].x, circles[j].x, circles[i].y, circles[j].y)
            if L > 0:
                U[i][j] = U[i][j] + L**2
                force = [circles[i].x - circles[j].x, circles[i].y - circles[j].y]
                if force[0] != 0:
                    force[0] =  force[0]/np.linalg.norm(force, ord=2)
                if force[1] != 0:
                    force[1] = force[1] / np.linalg.norm(force, ord=2)
                if L < 0.001:
                    L = L*100
                move_vector[0] = move_vector[0] + L*force[0]
                move_vector[1] = move_vector[1] + L*force[1]
        circles[i].x = circles[i].x + step * move_vector[0]
        circles[i].y = circles[i].y + step * move_vector[1]
        if circles[i].x + circles[i].r > 1: circles[i].x = 1 - circles[i].r
        if circles[i].x - circles[i].r <-1: circles[i].x = circles[i].r - 1
        if circles[i].y + circles[i].r > 1: circles[i].y = 1 - circles[i].r
        if circles[i].y - circles[i].r <-1: circles[i].y = circles[i].r - 1
    return U, UW


if __name__ == '__main__':
    m = 13
    r = [1, 0.17, 0.17, 0.17, 0.17, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085]
    circles = []
    S = 4
    step = 0.1                           # 拟物法步长
    times = 1                           # 要优化的次数
    for i in range(0,m):                 # 随机初始化一组半径r
        x = random.randint(-100, 100) / 100
        y = random.randint(-100, 100) / 100
        circles = circles + [circle(x, y, r[i])]
    for i in range(0, times):
        step = 0.1
        # circles[find_min_nei(circles)].r = circles[find_min_nei(circles)].r + 0.005
        U, UW= update(circles, step)
        # expand(circles)
        U1 = U
        UW1 = UW
        while (np.sum(U)!= 0):
            U, UW = update(circles, step)
            # for j in range(len(circles)):
            #     circles[j].show()
            # if np.sum(U)<0.01:
            #     plt.xlim(-1, 1)
            #     plt.ylim(-1, 1)
            #     plt.show()
            if np.sum(U) + UW>= np.sum(U1) + UW1:
                step = step * 0.8
            if step<0.01:
                print("随机")
                nosmall_step(circles, U)
                step = 0.1
            U1 = U
            UW1 = UW
            print("第%d次优化，U的值为%f"%(i, np.sum(U)))
    for i in range(len(circles)):
        circles[i].show()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.show()