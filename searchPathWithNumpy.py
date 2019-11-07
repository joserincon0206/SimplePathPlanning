import numpy as np
import cv2



#This is a little path planning algorithm using numpy, and opencv.


gridNP = np.array([[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]])

gridNPColor = np.zeros((5, 6, 3))
hasObstacle = gridNP == 1


gridNPColor[hasObstacle] = (0, 0, 255)


cv2.namedWindow('worldMap', cv2.WINDOW_NORMAL)
cv2.resizeWindow('worldMap', (1500, 1200))
cv2.imshow('worldMap', gridNPColor)
cv2.waitKey(1)

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

print(goal)

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']
out = cv2.VideoWriter('pathPlanning.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (6, 5), True)



def search(grid, init, goal, cost, gridNPColor):

    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid[1]))]
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid[1]))]
    closed[init[0]][init[1]] = 1
    x = init[0]
    y = init[1]
    g = 0
    openNodes = [[g, x, y]]
    found = False
    resign = False

    while found is False and resign is False:
        if len(openNodes) == 0:
            resign = True
            print('fail')

        else:
            openNodes.sort()
            openNodes.reverse()
            next = openNodes.pop()

            x = next[1]
            y = next[2]
            g = next[0]
            gridNPColor[x, y, :] = (0,255, 0)
            cv2.imshow('worldMap', gridNPColor)
            out.write(gridNPColor)
            cv2.waitKey(200)
            if x == goal[0] and y == goal[1]:
                found = True
                print(next)
            else:

                for i in range(len(delta)):

                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]

                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                       if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                           g2 = g + cost
                           openNodes.append([g2, x2, y2])
                           closed[x2][y2] = 1
                           action[x2][y2] = i

    x = goal[0]
    y = goal[1]
    path = []
    while x != init[0] or y!=init[1]:
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        path.append([x, y])


        x = x2
        y = y2
    path.reverse()
    gridNPColor[0, 0, :] = (255, 255, 0)
    cv2.imshow('worldMap', gridNPColor)
    out.write(gridNPColor)
    cv2.waitKey(200)
    for i in range(len(path)):
        [x, y] = path[i]
        gridNPColor[x, y, :] = (255, 255, 0)
        out.write(gridNPColor)

        cv2.imshow('worldMap', gridNPColor)
        cv2.waitKey(200)
    return next


def main():
    hey = search(grid, init, goal, cost, gridNPColor)
    jose = 0


if __name__ == '__main__':
    main()

