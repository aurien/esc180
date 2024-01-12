def is_bounded(board, y_end, x_end, length, d_y, d_x):
  start = ""
  end = ""
  if (y_end + d_y) >= len(board) or (x_end + d_x) >= len(board) or (
      y_end + d_y) < 0 or (x_end + d_x) < 0:
    end = "closed"

  if y_end - length * d_y >= len(board) or (x_end - length * d_x) >= len(
      board) or (y_end - length * d_y) < 0 or (x_end - length * d_x) < 0:
    start = "closed"

  if start != "closed":
    #check start to see if blocked by colour
    if board[y_end - (length) * d_y][x_end - (length) * d_x] != " ":
      start = "closed"
  if end != "closed":
    #check end to see if blocked
    if board[y_end + d_y][x_end + d_x] != " ":
      end = "closed"

  if start == "closed" and end == "closed":
    return "CLOSED"
  elif start != "closed" and end != "closed":
    return "OPEN"
  else:
    return "SEMIOPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count = 0
  semi_open_seq_count = 0
  x = x_start - d_x
  y = y_start - d_y
  length_counter = 0
  for i in range(len(board)):
#    print ("\n",i)
    x += d_x
    y += d_y
#    print ("Coordinate:", x, y)
    if board[y][x] == col:
      length_counter += 1
#      print ("1.0 length counter:", length_counter)
      if y == y_start+((len(board)-1)*d_y) and x == x_start+((len(board)-1)*(d_x)):
        if length_counter == length:
          type = is_bounded(board, y, x, length, d_y, d_x)
          if type == "OPEN":
            open_seq_count += 1
          elif type == "SEMIOPEN":
            semi_open_seq_count += 1
          else:
            continue
    elif board[y][x] != col:
      if length_counter == length:
        type = is_bounded(board, y - d_y, x - d_x, length, d_y, d_x)
        if type == "OPEN":
          open_seq_count += 1
        elif type == "SEMIOPEN":
          semi_open_seq_count += 1
        else:
          continue
      length_counter = 0
  return (open_seq_count, semi_open_seq_count)

def detect_rows(board, col, length):
  open_seq_count, semi_open_seq_count = 0, 0
  #horizontal and vertical
  for i in range(len(board)):
    #open
    open_seq_count += detect_row(board, col, i, 0,
                                 length, 0, 1)[0] + detect_row(
                                   board, col, 0, i, length, 1, 0)[0]
    #semiopen
    semi_open_seq_count += detect_row(board, col, i, 0, length, 0,
                                      1)[1] + detect_row(
                                        board, col, 0, i, length, 1, 0)[1]
 #diagonals
  for j in range(len(board) - length):
    print (j)
    open_seq_count += detect_row(
      board, col, j, 0, length, 1, 1)[0] + detect_row(
        board, col, 0, j, length, 1, 1)[0] + detect_row(
          board, col,
          len(board) - 1 - j,
          len(board) - 1, length, -1, -1)[0] + detect_row(
            board, col,
            len(board) - 1,
            len(board) - 1 - j, length, -1, -1)[0]

    semi_open_seq_count += detect_row(
      board, col, j, 0, length, 1, 1)[1] + detect_row(
        board, col, 0, j, length, 1, 1)[1] + detect_row(
          board, col,
          len(board) - 1 - j,
          len(board) - 1, length, -1, -1)[1] + detect_row(
            board, col,
            len(board) - 1,
            len(board) - 1 - j, length, -1, -1)[1]
  #total counter
  return (open_seq_count, semi_open_seq_count)


board1 = [["b", " ", "b", "b", "w"],
         ["b", "b", " ", "b", "b"],
         ["b", "w", " ", "b", "b"],
         [" ", "b", "w", "b", "b"],
         ["w", "w", "b", "b", "b"]]
#a = print (detect_row(board1, "b", 0, 0, 2, 1, 0)) #(0,0)
#b = print (detect_row(board1, "b", 0, 0, 2, 1, 1)) #(0,2)
#c = print (detect_row(board1, "b", 0, 0, 2, 0, 1)) #(0,1)

board2 = [["b", " ", "b", "b", "b", " ", "b", "w"],
          ["b", "b", " ", "b", "b", " ", "b", "w"],
          [" ", "w", " ", "w", "w", " ", " ", " "],
          [" ", "b", "w", "b", "b", "b", "b", "w"],
          ["w", " ", " ", "b", " ", "b", "b", "w"],
          [" ", "w", "w", "w", " ", "w", "b", "w"],
          ["w", "w", "b", "b", " ", "w", "b", "w"],
          ["w", "w", "b", "b", " ", "w", " ", "w"]]
#d = print (detect_row(board2, "b", 1, 0, 2, 0, 1)) #(1,1)
#e = print (detect_row(board2, "w", 2, 0, 2, 0, 1)) #(1,0)
backwards = print (detect_row(board2, "b", 7, 7, 2, -1, -1)[0]) #(0,1)

board3 = [["b", "b", "b", "b", "b", " ", "b", "w"],
          [" ", "w", " ", "b", " ", " ", "b", " "],
          [" ", " ", " ", "b", "w", " ", " ", " "],
          [" ", "b", "b", "b", "b", "b", " ", "b"],
          ["w", " ", " ", "b", " ", "b", "b", " "],
          [" ", " ", "w", " ", " ", "w", "b", "w"],
          ["w", " ", "b", "b", " ", "w", "b", "w"],
          ["w", " ", "b", "b", " ", "w", " ", "w"]]

          #(1,2)
test = print (detect_rows(board3, "b", 5))

print ((1,2) + (3,4))




