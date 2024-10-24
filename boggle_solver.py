#NAME: Anverly Jones SID:@03087240
class Boggle:
    def __init__(self, grid, dictionary):
        
        self.grid = grid
        self.dictionary = set(word.upper() for word in dictionary)
        self.solutions = set()
        self.rows = len(grid)
        self.cols = len(grid[0])
        

    def is_valid_grid(self):
      if not self.grid:
        return False
      if (len(self.grid) != len(self.grid[0])):
        return False 
        # Scan the entire grid to check for standalone Q, U, S, or T
      for row in self.grid:
          for tile in row:
            current = tile.upper()
            if current == "Q" :
              return False  # Q and U must always be together (as "QU")
            if current == "S" :
              return False  # S and T must always be together (as "ST")
      return True  # Grid is valid if no invalid letters are found

    def DepthForSearch(self, word, i, j, path, index):
      # Ensure that index is within the bounds of the word
      if index >= len(word):
          return

      if not (0 <= i < self.rows and 0 <= j < self.cols) or (i, j) in path:
          return
      #print("before i = " , i,"bj = ", j)

      current = self.grid[i][j].upper()
      #print("after i = " , i, "aj = ", j)
      # Handle "QU" as a special case
      if current == "QU":
          if index + 2 <= len(word) and word[index:index + 2] == "QU":
              path.add((i, j))
              if index + 2 == len(word):
                self.solutions.add(word)
              else:
                self.SearchNext(word, i, j, path, index + 2)
              path.remove((i, j))
          return

      # Handle "ST" as a special case
      if current == "ST":
          if index + 2 <= len(word) and word[index:index + 2] == "ST":
              path.add((i, j))
              if index + 2 == len(word):
                self.solutions.add(word)
              else:
                self.SearchNext(word, i, j, path, index + 2)
              path.remove((i, j))
          return

      # Reject "Q" without "U", or "S" without "T"
      if current == "Q" and (index + 1 >= len(word) or word[index + 1] != "U"):
          return
      if current == "S" and (index + 1 >= len(word) or word[index + 1] != "T"):
          return

      # Ensure that current character matches the word's character at index
      if current != word[index]:
          return

      # Add the current position to the path
      path.add((i, j))

      # If the last character of the word has been reached
      if index + 1 == len(word):
          self.solutions.add(word)
      else:
          # Continue searching in the next adjacent positions
          self.SearchNext(word, i, j, path, index + 1)

      # Remove the current position from the path
      path.remove((i, j))


    def SearchNext(self, word, i, j, path, index):
        for x, y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            ni, nj = i + x, j + y
            self.DepthForSearch(word, ni, nj, path, index)

    def getSolution(self):
      # Validate the grid before starting the search
        if self.is_valid_grid(): 
          for word in self.dictionary:
              if len(word) >= 3:
                  for i in range(self.rows):
                      for j in range(self.cols):
                          self.DepthForSearch(word, i, j, set(), 0)
        return sorted(self.solutions)

# Example usage of the updated Boggle class
def main():
    grid = [["A", "B", "Y", "R"],
            ["E", "N", "P", "H"],
            ["G", "Z", "QU", "R", "I","L"],
            ["O", "N", "M", "A", "ST"]]
    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry",
                  "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", 
                  "arty", "rhr", "not", "quar"]
    try:
        mygame = Boggle(grid, dictionary)
        print(mygame.getSolution())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
