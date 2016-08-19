def sql_comment_block(input, width=120):
    delineator = '='
    line_start = '/* ' + delineator * (width - 3) + '\n'
    line_end = '\n' + delineator * (width - 3) + ' */'

    if type(input) is str:
        output_block = [input.center(width)]
    elif type(input) is list:
        output_block = reduce(lambda x, y: x + [y.center(width)], input, [])
    else:
        raise TypeError, 'Only accepts list and string types'

    output_block.insert(0, line_start)
    output_block.append(line_end)
    output_block.append('\n')

    for line in output_block:
        print line

    return output_block
