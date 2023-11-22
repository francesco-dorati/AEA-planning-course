import numpy as np

def bresenham(p1, p2):
  if p1[0] < p2[0]:
    x1, y1 = p1
    x2, y2 = p2
  else:
    x1, y1 = p2
    x2, y2 = p1

  cells = []

  m = (y2 - y1) / (x2 - x1)

  if m > 0:
    x = x1
    y = y1

    while x < x2:
      fy = int(np.floor(y))
      d = int(np.floor(y+m)) - fy

      if d > 0:
        cells.append((x, fy))
        for i in range(1, d+1):
            cells.append((x, fy+i)) if (fy+i < y2) else None

      x += 1
      y += m

  elif m < 0: 
    x = x1
    y = y1-1

    while x < x2:
      fy = int(np.ceil(y)) 
      d = abs(int(np.ceil(y+m)) - fy)

      if d > 0:
        cells.append((x, fy))
        for i in range(1, d+1):
          cells.append((x, fy-i)) if (fy-i >= y2) else None

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