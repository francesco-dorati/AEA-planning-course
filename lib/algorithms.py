import numpy as np

def bresenham(p1, p2):
  cells = []

  x1, y1 = min([p1, p2])
  x2, y2 = max([p1, p2])
  
  if p1 == p2:
    return [p1]
  
  elif x1 == x2:
    y = min([y2, y1])
    d = abs(y2 - y1)
    for i in range(d):
      cells.append((x1, y+i))
    return cells
  
  elif y1 == y2:
    x = min([x2, x1])
    d = abs(x2 - x1)
    for i in range(d):
      cells.append((x+i, y1))
    return cells
  

  m = (y2 - y1) / (x2 - x1)

  if m > 0:
    x = x1
    y = y1

    while x < x2:
      fy = int(np.floor(y))
      d = int(np.floor(y+m)) - fy

      cells.append((x, fy))
      if d > 0:
        for i in range(1, d+1):
            cells.append((x, fy+i)) #if (fy+i <= y2) else None

      x += 1
      y += m

  elif m < 0: 
    x = x1
    y = y1-1

    while x < x2:
      fy = int(np.ceil(y)) 
      d = abs(int(np.ceil(y+m)) - fy)

      cells.append((x, fy))
      if d > 0:
        for i in range(1, d+1):
          cells.append((x, fy-i)) #if (fy-i >= y2) else None

      x += 1
      y += m


  return cells


def collinearity(p1, p2, p3, epsilon=1e-2):
  # 2D
  if len(p1) == 2:
    p1 = (p1[0], p1[1], 1)
    p2 = (p2[0], p2[1], 1)
    p3 = (p3[0], p3[1], 1)

  mat = np.vstack((p1, p2, p3))
  det = np.linalg.det(mat)

  if abs(det) < epsilon:
    return True
  
  return False