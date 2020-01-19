# -*- coding: utf-8 -*-

import numpy as np
import cv2

rect = np.float32([[-400, -300, 0],
                   [400, -300, 0],
                   [-400, 300, 0],
                   [400, 300, 0]])
print(rect)


camera = 1111.11
center = [400, 300]
pos = np.array([400, 300, 10])
scl = np.array([80, 80, 0])
rotY = np.radians(0)
rotX = np.radians(60)
rotZ = np.radians(45)

# 拡大
rect *= scl / 100.0

# 計算のために列ベクトル化する
p0 = rect[0].reshape(-1, 1)
p1 = rect[1].reshape(-1, 1)
p2 = rect[2].reshape(-1, 1)
p3 = rect[3].reshape(-1, 1)

# 回転
ry = np.matrix([[np.cos(rotY), 0, np.sin(rotY)],
                [0, 1, 0],
                [-np.sin(rotY), 0, np.cos(rotY)]])
rx = np.matrix([[1, 0, 0],
                [0, np.cos(rotX), -np.sin(rotX)],
                [0, np.sin(rotX), np.cos(rotX)]])
rz = np.matrix([[np.cos(rotZ), -np.sin(rotZ), 0],
                [np.sin(rotZ), np.cos(rotZ), 0],
                [0, 0, 1]])
p0 = (rz * (rx * (ry * p0)))
p1 = (rz * (rx * (ry * p1)))
p2 = (rz * (rx * (ry * p2)))
p3 = (rz * (rx * (ry * p3)))

# 移動
# 位置を列ベクトル化して足す
p0 += pos.reshape(-1, 1)
p1 += pos.reshape(-1, 1)
p2 += pos.reshape(-1, 1)
p3 += pos.reshape(-1, 1)

# 透視投影
# カメラとのZ座標の差を取得する
len0 = camera + p0[2]
len1 = camera + p1[2]
len2 = camera + p2[2]
len3 = camera + p3[2]
# X方向の傾きを取得して投影面上のX座標に書き換える
dx0 = (p0[0] - center[0]) / len0
dx1 = (p1[0] - center[0]) / len1
dx2 = (p2[0] - center[0]) / len2
dx3 = (p3[0] - center[0]) / len3
p0[0] = dx0 * camera + center[0]
p1[0] = dx1 * camera + center[0]
p2[0] = dx2 * camera + center[0]
p3[0] = dx3 * camera + center[0]
# Y方向の傾きを取得して投影面上のY座標に書き換える
dy0 = (p0[1] - center[1]) / len0
dy1 = (p1[1] - center[1]) / len1
dy2 = (p2[1] - center[1]) / len2
dy3 = (p3[1] - center[1]) / len3
p0[1] = dy0 * camera + center[1]
p1[1] = dy1 * camera + center[1]
p2[1] = dy2 * camera + center[1]
p3[1] = dy3 * camera + center[1]
# 2DになるのでZ座標は0固定
p0[2] = 0
p1[2] = 0
p2[2] = 0
p3[2] = 0
print(rect)

# 元絵の4点
pt_bef = np.float32([[0, 0],
                     [800, 0],
                     [0, 600],
                     [800, 600]])
# 変換先の4点
pt_aft = np.float32([[p0[0, 0], p0[1, 0]],
                     [p1[0, 0], p1[1, 0]],
                     [p2[0, 0], p2[1, 0]],
                     [p3[0, 0], p3[1, 0]]])
print(pt_bef)
print(pt_aft)
# 元絵と変換先の変換行列を作る
M = cv2.getPerspectiveTransform(pt_bef, pt_aft)
image = cv2.imread('./grad.png')
print(M)
trans = cv2.warpPerspective(image, M, (800, 600))
cv2.imwrite('grad_out.png', trans)

if __name__ == '__main__':
    pass
