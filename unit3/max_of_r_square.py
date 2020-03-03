#为找到是的r^2最大的x，y，首先遍历整个可行域，步长为0.01
#每一种情况r都要取此点到边界的距离中的最小值
#计算每种情况的r，找到最大值并记录

import numpy as np
max_r_square = 0
for x_m in np.arange(-1,1,1/100):            #遍历x
    for y_m in np.arange(-1,1,1/100):           #遍历y
        r = min(1 - x_m, x_m + 1, 1 - y_m , y_m + 1)         #找到到边界的最小值
        r_square = r**2                          #计算r^2
        if r_square > max_r_square:              #记录结果
            max_r_square = r_square
            x_m_result = x_m
            y_m_result = y_m
print("max of r square:", max_r_square, "\n", "value of x_m and y_m: (%d, %d)"%(x_m_result, y_m_result))   #输出结果
