class Grid:
    cols_headings = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    rows_headings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self,ships=None,miss_list=None):
        self.ships = ships
        self.miss_list = miss_list
        pass

    def create_grid(self):
        pass

    def create_rows(self,rows_headings, cols_headings, ships, miss_list):
        pass

    def create_col_headings(self,cols_headings):
        pass