from tools import colors


def display_error(col, error_str, count, line):
    str_count = str(count)
    str_col = str(col)
    if col == -1:
        print(line, f"{colors.clr.fg.lightred}\u2717{colors.clr.reset}")
        for elt in line:
            print(f"{colors.clr.fg.red}^{colors.clr.reset}", end="")
        print("")
        print(colors.clr.fg.red, f"Parsing error: [line: {str_count}] {error_str}", colors.clr.reset)
    elif col == -2:
        for elt in line:
            if elt == ')' or elt == '(':
                print(f"{colors.clr.bg.red}{elt}{colors.clr.reset}", end="")
            else:
                print(f"{elt}", end="")
        print("", f"{colors.clr.fg.lightred}\u2717{colors.clr.reset}")
        for elt in line:
            if elt == ')' or elt == '(':
                print(f"{colors.clr.fg.red}^{colors.clr.reset}", end="")
            else:
                print(" ", end="")
        print("")
        print(colors.clr.fg.red, f"Parsing error: [line: {str_count}] {error_str}", colors.clr.reset)
    else:
        ind = 0
        for elt in line:
            if ind == col:
                print(f"{colors.clr.bg.red}{elt}{colors.clr.reset}", end="")
            else:
                print(f"{elt}", end="")
            ind += 1
        print(f" {colors.clr.fg.lightred}\u2717{colors.clr.reset}")
        ind = 0
        for elt in line:
            if ind == col:
                print(f"{colors.clr.fg.red}^{colors.clr.reset}", end="")
            else:
                print(" ", end="")
            ind += 1
        print("")
        print(colors.clr.fg.red, f"Parsing error:[line: {str_count}][col: {str_col}] {error_str}", colors.clr.reset)
    return 1