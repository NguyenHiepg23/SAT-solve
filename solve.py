import itertools
from pysat.solvers import Glucose3

solver = Glucose3()             
input_file = "input.txt"        # Input file

with open(input_file, "r") as file:
    h, w = map(int, file.readline().split(" "))
    matrix = []; [matrix.append(line.split(" ")) for line in file.read().split("\n")]
       
pos_var = lambda i, j: i * h + j + 1            # Variables for solver
nei_pos_m = list(itertools.product([-1, 0, 1], repeat=2))       

# Add clasue for solve
for i in range(h): 
    for j in range(w): 
        if matrix[i][j].isnumeric():
            value = int(matrix[i][j])           
            neighbors = []
            
            # Get the neighbor (adjacency -.-)
            [neighbors.append(pos_var(i + px, j + py)) for px, py in nei_pos_m if 0 <= i + px < h and 0 <= j + py < w]
                    
            # Get all possible cases of mine possition
            mines_pos_can_happ = list(itertools.combinations(neighbors, value))      
                      
            for mp in mines_pos_can_happ:
                have_mine = list(mp)
                d_have_mine = list(set(neighbors).difference(set(have_mine)))
            
                # Generate constraints
                clauses = []
                [clauses.append(have_mine.copy() + [dhm]) for dhm in d_have_mine]
                [clauses.append([-m for m in d_have_mine.copy()] + [-hm]) for hm in have_mine] 

                # Add constraints to solver
                [solver.add_clause(cl) for cl in clauses]

# Solve!               
if solver.solve():
    f_matrix = solver.get_model() 
    
    # Final matrix
    ff_matrix = []
    row = []

    for i in f_matrix:
        row.append(i)
        if len(row) == w:
            ff_matrix.append(row)
            row = []
            
    # Export to HTML file       
    html_str_fr = \
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Final Matrix</title>
        <style>
            table {
                border-collapse: collapse;
                margin: auto;
                margin-top: 10%;
            }

            td {
                width: 50px;
                height: 50px;
            }

            .green {
                background-color: green;
            }

            .red {
                background-color: red;
            }
            
            tr {
                display: flex;
            }
            
            tr * {
                flex: 1;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-weight: 900;
                font-size: 20px;
                font-family: monospace;
            }
        </style>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <table >
            <tbody>
                --board--    
            </tbody>
        </table>
    </body>
    </html>
    """
    
    boxes = ""
    for i in range(h):
        boxes += "<tr>"
        
        for j in range(w):
            if ff_matrix[i][j] < 0: 
                if not matrix[i][j].isnumeric(): boxes += '<td class="green"></td>'         
                else: boxes += '<td class="green">{}</td>'.format(matrix[i][j]) 
            else: 
                if not matrix[i][j].isnumeric(): boxes += '<td class="red"></td>'         
                else: boxes += '<td class="red">{}</td>'.format(matrix[i][j]) 
        
        boxes += "</tr>"
           
    with open("final_matrix.html", "w") as file:
        file.write(html_str_fr.replace("--board--", boxes))
         
else: print("No solution!")
