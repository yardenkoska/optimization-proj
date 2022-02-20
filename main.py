from branch_and_bound import branch_and_bound_main
from cutting_planes import cutting_planes_main
import time

CP_NODES = ["0", "1", "2", "3" ]
CP_MATRIX = { ("0", "0"): 0, ("0", "1"): 10, ("0", "2"): 15, ("0", "3"): 20,
      ("1", "0"): 10, ("1", "1"): 0, ("1", "2"): 35, ("1", "3"): 25,
      ("2", "0"): 15, ("2", "1"): 35, ("2", "2"): 0, ("2", "3"): 30,
      ("3", "0"): 20, ("3", "1"): 25, ("3", "2"): 30, ("3", "3"): 0,
 }
BB_NODES = 4
BB_MATRIX = [[0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]]


if __name__ == '__main__':
    begin_cp = time.time()
    print('Cutting Planes:')
    cutting_planes_main(CP_NODES, CP_MATRIX)
    end_cp = time.time()

    print('#############################################################################################\n')

    begin_bb = time.time()
    print('Branch and Bound:')
    branch_and_bound_main(BB_NODES, BB_MATRIX)
    end_bb = time.time()

    print('#############################################################################################\n')
    print(f'runtime intervals:\nbranch and bound: {end_bb - begin_bb} \ncutting planes: {end_cp - begin_cp}\n')
    print('############################## IRRELEVANT ##############################')
