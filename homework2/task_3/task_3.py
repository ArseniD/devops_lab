"""
Get data from INPUT.TXT file, form list of mutual and not mutual friends
and write it to the OUTPUT.TXT file

"""

if __name__ == '__main__':

    # Get list of data from INPUT.TXT
    list_data = [line.strip() for line in open('INPUT.TXT')]

    # Get list of n and m indexes
    ind_pos = [i for i, x in enumerate(list_data) if x.isdigit()]

    # Get list of current friends
    list_friends = list_data[ind_pos[0] + 1:ind_pos[1]]
    str_friend_result = 'Friends: ' + \
        ', '.join(e for e in sorted(list_friends))

    # Get list of mutual and not mutual friends
    list_other = list_data[ind_pos[1] + 1:]

    # # Get list of mutual friends
    list_mutual = set(list_friends).intersection(list_other)
    str_mutual_result = 'Mutual Friends: ' + \
        ', '.join(e for e in sorted(list_mutual))

    # # Get list of not mutual friends
    list_nomutual = list(set(list_other) - list_mutual)
    str_nomutual_result = 'Also Friend of: ' + \
        ', '.join(e for e in sorted(list_nomutual))

    # Form and send a new data to the OUTPUT.TXT
    with open('OUTPUT.TXT', 'w') as output_file:
        output_file.write('{0}\n{1}\n{2}'.format(
            str_friend_result, str_mutual_result, str_nomutual_result))
