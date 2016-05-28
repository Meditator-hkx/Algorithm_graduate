class FL_Matrix:
    def __init__(self, fnum = 10, lnum = 9):
        self.FlowNumber = fnum
        self.LinkNumber = lnum
        self.matrix = []
        # Initiate a matrix as below:
        for i in range(fnum):
            self.col = []
            for j in range(lnum):
                self.col.append(0)
            self.matrix.append(self.col)

    def printMatrixInfo(self, str):
        print '\n' + str + ', the F-L matrix is shown as below:\n--------------------------------------------------'
        for i in range(self.FlowNumber):
            for j in range(self.LinkNumber):
                print self.matrix[i][j],
            print '\n'