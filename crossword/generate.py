import sys,random

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for value in self.domains[var].copy():
                if len(value) != var.length:
                    self.domains[var].remove(value)  

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #As explained in lecture by Brian...
        revised = False
        overlap = self.crossword.overlaps[x,y]
        #Otherwise they're already arc consistent (every value in X's domain is acceptable and there's no arc)
        if overlap != None:
            for x_val in self.domains[x].copy():
                for y_val in self.domains[y]:
                    #Also check if it is already been removed
                    if not (x_val[overlap[0]] == y_val[overlap[1]]) and (x_val in self.domains[x]) :
                        self.domains[x].remove(x_val)
                        revised = True
        return revised

    def ac3_dirtyJob(self,queue):
        while len(queue) > 0:
            (X,Y) = queue.pop()
            if self.revise(X,Y):
                if len(self.domains[X]) == 0:
                    return False
                    for Z in self.crossword.neighbors(X) - {Y}:
                        queue.append((Z,X))
            return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        result = False

        #Begins with all arcs in the problem
        if arcs == None:
            arc_queue = list()
            for X in self.crossword.variables:
                neighbours = self.crossword.neighbors(X)
                if len(neighbours)>0:
                    for var in neighbours:
                        overlaps = self.crossword.overlaps[X, var]
                        if overlaps != None:
                            arc_queue.append((X,var))
            result = self.ac3_dirtyJob(arc_queue)
        #Use arcs as initial list of arcs
        else:
            result = self.ac3_dirtyJob(arcs)
        return result



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return not 0 in [len(assignment.get(var,default = '')) for var in self.crossword.variables] 
    
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #Control variables
        c1 = c2 = c3 = 0
        
        for var in assignment:    
            #Length test
            if var.length != len(assignment.get(var,default='')):
                c1 = 1
            #Distinct values test
            if assignment.get(var) in list(assignment.values().copy()).remove(assignment.get(var)):
                c2 = 1
            #Neighbour test
            if len(self.crossword.neighbors(var))>0:
                for n in self.crossword.neighbors(var):
                    if self.crossword.overlaps[var, n] != None:
                        (i,j) = self.crossword.overlaps[var, n]
                        if assignment.get(var,default=(1+i)*"_")[i] != assignment.get(n,default=(j+1)*'*')[j]:
                            c3 = 1
        #Final check
        if 1 in (c1,c2,c3):
            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #TODO Later implement correctly
        return sorted(list(self.domains[var]))


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #TODO Later implement correctly
        for var in self.crossword.variables:
            if var not in assignment:
                return var  


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        #Select an Unassigned var X
        X = self.select_unassigned_variable(assignment)
        
        #Loop over X's domain in a selected order
        for currentValue in self.order_domain_values(X, assignment): 

            #check if current value is consistent with assignment
            

            #add var: current value to assignment 

            #Keep track of possible inferences

            #if inferences not failure add them to the assignment

            #recursivly call backtrak with the new assignment

            #if the recursive call is not a failure return it

            #otherwhise (if value not consistent) remove inferences and var:current value to assignment
        
        #return failure
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
