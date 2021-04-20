def ask_mode():  # sequential or multi-thread
    print('how do you want to run?\n1 - Sequential\n2 - Multithread')
    mode = input('Enter choice: ')
    while mode != '1' and mode != '2':
        mode = input('Not valid. Try again: ')
    return mode


def ask_products():
    queries = []
    query = input('which product? (leave blank to end): ')
    if not query:
        print('please enter at least one product.')
        quit()
    while query:
        queries.append(query)
        if len(queries) > 7:  # max 8 queries allowed
            break
        query = input('other products? (leave blank to end): ')
    return queries
