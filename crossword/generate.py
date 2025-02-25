import sys,random
import math

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
        for var in self.crossword.variables:
            for w in self.crossword.words:
                if len(w) != var.length:
                    self.domains[var].remove(w)
        return None

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
<<<<<<< HEAD
        constraint_satisfied = False
        overlaps = self.crossword.overlaps[x,y]
        if overlaps != None:
            for val_x in self.domains[x].copy():
                for val_y in self.domains[y]:
                    if val_x[overlaps[0]] == val_y[overlaps[1]]:
                        constraint_satisfied = True
                if not constraint_satisfied :
                    self.domains[x].remove(val_x)
                    revised = True
=======
        if not self.crossword.overlaps[x,y] is None:
            i,j = self.crossword.overlaps[x,y]
            for val_x in self.domains[x].copy():
                do_not_remove = False
                for val_y in self.domains[y]:
                    if val_x[i] == val_y[j]:
                        do_not_remove = True
                if do_not_remove == False:
                    self.domains[x].remove(val_x)
                    revised = True

>>>>>>> c08e12da0e21e3895c2fc344852dd136b487fed8
        return revised



    def ac3_dirty_job(self,arcs):
        while arcs:
            (X, Y) = arcs.pop()
            if self.revise(X, Y):
                if self.domains[X] is None:
                    return False
                for Z in self.crossword.neighbors(X) - {Y}:
                    arcs.append((Z, X))
        return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            all_arcs = []
            for var_1 in self.domains:
                for var_2 in self.domains:
                    if var_1 != var_2:
                        all_arcs.append((var_1, var_2))
            return self.ac3_dirty_job(all_arcs)
        else:
            return self.ac3_dirty_job(arcs)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment.keys() or assignment[v] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            #Length test
            if var.length != len(assignment.get(var,'')):
                return False

            for var2 in assignment:
                if var != var2:
                    # Distinct words test
                    if assignment[var] == assignment[var2]:
                        return False
                    overlaps = self.crossword.overlaps[var,var2]
                    #Overlap test
                    if overlaps != None:
                        if assignment[var][overlaps[0]] != assignment[var2][overlaps[1]]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
<<<<<<< HEAD

        for neighbor in self.crossword.neighbors(var):
            i,j = self.crossword.overlaps[var,neighbor]

            affect_list = list()

            for value in self.domains[var]:
                values_affected = 0
                for neighbor_val in self.domains[neighbor]:
                    if value[i] != neighbor_val[j]:
                        values_affected += 1
                affect_list.append([value,values_affected])

        values_affected_sorted = sorted([item[1] for item in affect_list])

        result = list()

        for item in values_affected_sorted:
            for elem in affect_list:
                if elem[1] == item and not elem[0] in result:
                    result.append(elem[0])

        return result

=======
        #Mapping each value of var to how many choices we  delete in neighbour's values (n)
        deleted_choices = dict.fromkeys(self.domains[var], 0) #Assuming no domain is empty

        for val in deleted_choices:
            for neighbour in self.crossword.neighbors(var) :
                if neighbour not in assignment:
                    for val_n in self.domains[neighbour]:
                        if not self.consistent({var:val, neighbour:val_n}):
                            print("ao")
                            deleted_choices[val] += 1
        print(deleted_choices)

        return list(deleted_choices)
>>>>>>> c08e12da0e21e3895c2fc344852dd136b487fed8

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        degree = 0
        value = math.inf

        for key in self.domains.keys():
            if key not in assignment:
                if value > len(self.domains[key]):
                    value = len(self.domains[key])
                    variable = key
                    if self.crossword.neighbors(key) == None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(key))
                elif value == len(self.domains[key]):
                    if self.crossword.neighbors != None:
                        if degree < len(self.crossword.neighbors(key)):
                            variable = key
                            value = len(self.domains[key])
                            degree = len(self.crossword.neighbors(key))
                    else:
                        variable = key
                        degree = 0
                        value = len(self.domains[key])
        return variable


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is None:
                    assignment[var] = None
                else:
                    return result
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
