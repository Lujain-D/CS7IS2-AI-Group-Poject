
#import fileinput
import time
import tracemalloc
cnt=0
def print_sudoku(s):
  
    for row in range(9):
        for col in range(9):
            print(s[row][col], end=' ')
            if col+1 == 3 or col+1 == 6:
                print(" | ", end=' ')
        if row+1 == 3 or row+1 == 6:
            print("\n" + "-"*25, end=' ')
        print()
    print()

def test_cell(s, row, col):

    #print("row:",row)
    #print("col:",col);
    used = [0]*10
    used[0] = 1
    block_row = row // 3
    block_col = col // 3

    # Row and Column
    for m in range(9):
        used[s[m][col]] = 1;
        used[s[row][m]] = 1;
      
    # Square
    for m in range(3):
        for n in range(3):
            used[s[m + block_row*3][n + block_col*3]] = 1

    return used

def initial_try(s):
    
    stuck = False

    while not stuck:
        stuck = True
        # Iterate through the Sudoku puzzle
        for row in range(9):
            for col in range(9):
                used = test_cell(s, row, col)
                # More than one possibility
                if used.count(0) != 1:
                    continue

                for m in range(1, 10):
                    # If current cell is empty and there is only one possibility
                    # then fill in the current cell
                    if s[row][col] == 0 and used[m] == 0:
                        s[row][col] = m
                        stuck = False
                        break

def DFS_solve(s, row, col):
    global cnt
    if row == 8 and col == 8:
        used = test_cell(s, row, col)
        if 0 in used:
            s[row][col] = used.index(0)
        return True

    if col == 9:
        row = row+1
        col = 0

    if s[row][col] == 0:
        used = test_cell(s, row, col)
        for i in range(1, 10):
            if used[i] == 0:
                s[row][col] = i
                cnt += 1
                if DFS_solve(s, row, col+1):
                    return True

        # Reached here? Then we tried 1-9 without success
        s[row][col] = 0
        return False

    return DFS_solve(s, row, col+1)

def main():
    
    
    start = time.time()
    num_puzzles = 0
    avgSteps=0
    avgMemory=0
    s = []
    text = ""

    #for line in fileinput.input():
        #line = ' '.join(line.split())
        #text += line
    
    #file = open("testDataNormal.txt","r")
    file = open("testData.txt","r")
    for line in file:
        line = ' '.join(line.split())
        text += line
        
    file.close()
    
    while len(text) > 0:
        l = []

        # Get a row of numbers
        while len(l) < 9:
            if text[0].isdigit():
                l.append(int(text[0]))
            text = text[1:]

        # Insert that row into the Sudoku grid
        s.append(l)

        if len(s) == 9:
            num_puzzles += 1
            print("Puzzle Number {:d}".format(num_puzzles))
            print("Original:")
            print_sudoku(s)
            
            initial_try(s)
            #print("After initial try:")
            #print_sudoku(s)
            for line in s:
                if 0 in line:
                    start1 = time.time()
                    tracemalloc.start()
                    DFS_solve(s, 0, 0)
                    current, peak = tracemalloc.get_traced_memory()
                    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
                    avgMemory +=peak
                    break

            print("Solution:")
            print_sudoku(s)
            print("{:.2f} seconds to solve {} puzzle".format(time.time() - start1, num_puzzles))
            global cnt
            print("Total steps taken to solve:",cnt)
            avgSteps += cnt
            cnt=0
            print("="*30)
            s = []
            tracemalloc.stop()
            
    
    print("{:.2f} seconds to solve {} puzzles".format(time.time() - start, num_puzzles))
    avgSteps = avgSteps/50
    avgMemory =(avgMemory/50)/ 10**6
    print("Average step count is {:.2f}".format(avgSteps))
    print("Average Memory usage is {:.6f}MB".format(avgMemory))
   

if __name__ == "__main__":
    main()
