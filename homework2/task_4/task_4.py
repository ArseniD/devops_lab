if __name__ == '__main__':

    # Get list of data from INPUT.TXT
    data_list = [line.strip().split() for line in open('INPUT.TXT')][1]

    # Convert from string to list of integers and sort it
    int_list = [int(x) for x in data_list]

    # Get sum of positive elem in list
    sum_pos_elem = sum(filter(lambda a: a > 0, int_list))

    # Get min and max index in list
    min_ind = int_list.index(min(int_list))
    max_ind = int_list.index(max(int_list))

    # Form a new list based on the min and max indices
    if min_ind > max_ind:
        del int_list[min_ind:]
        del int_list[:max_ind+1]
    else:
        del int_list[:min_ind+1]
        del int_list[max_ind-1:]

    # Multiply each item in a new list
    multi_elem = reduce(lambda x, y: x * y, int_list)

    # Form and send a new data to the OUTPUT.TXT
    with open('OUTPUT.TXT', 'w') as file:
        file.write('{0} {1}'.format(sum_pos_elem, multi_elem))
