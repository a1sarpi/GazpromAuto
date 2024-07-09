def replace_scientific_notation_with_latex(input_string):
    scientific_notation_pattern = r'(-?\d+\.\d+)e(-?\d+)'
    replaced_string = re.sub(scientific_notation_pattern, r'\1 \\cdot 10^{\2}', input_string)
    return replaced_string

def print_matrix(matrix, rounding_way=lambda x: round(x, 5)):
    if len(matrix.shape) == 2:
        print("$\\begin{pmatrix}")
        if(matrix.shape[0] > 10):
            indecies = [0, 1, 2, 100, -1]
            for i in indecies:
                row = ''
                if(i == 100):
                    row = '&'.join(['\dots' if index != 100 else '\ddots' for index in indecies]) + '\\\\'
                    print(row)
                    continue
                for j in indecies:
                    if(j == 100):
                        row += '\dots &'
                        continue
                    kek_str = str(rounding_way(matrix[i][j])) if abs(matrix[i][j]) > 1e-15 else '0'
                    row += kek_str + ' & '
                row = row[:-2]
                row += '\\\\'
                print(row)
        else:
            for i in range(matrix.shape[0]):
                row = ''
                for j in range(matrix.shape[1]):
                    kek = matrix[i][j]
                    if kek > 0:
                        row += str(kek) + ' & '
                    else:
                        row += str(kek) + ' & '
                row = row[:-2]
                row += '\\\\'
                print(row)
        print("\\end{pmatrix} $")
    elif len(matrix.shape) == 1:
        if(matrix.shape[0] > 10):
            print(f"[ {rounding_way(matrix[0])}, {rounding_way(matrix[1])}, {rounding_way(matrix[2])}, \dots, {rounding_way(matrix[-1])} \\big>")
            return
        row = ''
        for i in range(matrix.shape[0]):
            kek = matrix[i]
            if kek > 0:
                row += str(round(kek, 5)).rstrip('0').rstrip('.') + ' \\\\ '
            else:
                row += str(round(kek, 4)).rstrip('0').rstrip('.') + ' \\\\ '
        print(row)
