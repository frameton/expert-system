from tools import colors


def search_end_negative_series(line, start):
    count = start
    series_len = 0
    while count < len(line):
        if line[count] != '!':
            break
        series_len += 1
        count += 1
    
    return series_len, count


def sort_negative_symbol(line):
    count = 0
    start = 0
    end = 0

    line = line.strip()
    line = line.replace(" ", "")
    line = line.replace("\n", "")
    line = list(line)

    while count < len(line):
        if line[count] == '!':
            start = count
            series_len, end = search_end_negative_series(line, start)
            if (series_len % 2) == 0:
                while start < end:
                    line[start] = ' '
                    start += 1
            else:
                while start < (end - 1):
                    line[start] = ' '
                    start += 1
        count += 1
    
    line = ''.join(line)
    return line