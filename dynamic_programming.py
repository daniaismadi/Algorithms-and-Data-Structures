def longest_oscillation(L):
    """
    Return the length of the longest oscillation in list L, and the indices
    in L at which it occurs.

    :precondition:          L contains only integers.
    :param L:               (list) A list of integers L- the list can contain
                            duplicates or be empty.

    :time complexity:       Best and Worst Case: O(N), where N is the length
                            of the input list. It takes O(N) time to
                            create the memo table, then it takes O(N) time
                            to complete the memoisation. Backtracking
                            to find the solution will also take O(N) time.
                            Reversing the final solution list will take O(N)
                            time using the built-in Python reverse function.
                            Best and worst case are the same since none of the
                            loops exit early.

    :space complexity:      O(N), where N is the length of the input list.
                            This is because auxiliary space complexity
                            is O(N) and the size of input list is O(N) which
                            gives a total space complexity of O(N).

    :aux space complexity:  O(N), where N is the length of the input list.
                            The memo table (for memoisation) and the
                            oscillation list (list that contains the solutions)
                            takes O(N) space each which gives a total
                            auxiliary space complexity of O(2N) which is O(N).

    :return:                (tuple) The first element of the tuple is a number,
                            which represents the length of the oscillation and
                            the second element is a list which contains the
                            indices of the elements in L which make up the
                            oscillation.
    """
    # handle boundary cases
    if L is None:
        return 0, []
    if len(L) < 1:
        return 0, []
    if len(L) < 2:
        return 1, [0]

    # create memo
    # time complexity: O(N)
    # aux space complexity: O(N)
    memo = [0] * (len(L) + 1)
    memo[0], memo[1] = 0, 1

    # true if sequence is currently ascending, false otherwise
    ascending = L[0] > L[1]

    # update memo table
    # time complexity: O(N)
    for i in range(2, len(memo)):
        if ascending and L[i-1] < L[i-2]:
            # end of ascending sequence
            # we are currently at a peak so add 1 to the length of the
            # oscillation
            memo[i] = 1 + memo[i-1]
            ascending = False
        elif not ascending and L[i-1] > L[i-2]:
            # end of descending sequence
            # we are currently at a valley so add 1 to the length of the
            # oscillation
            memo[i] = 1 + memo[i-1]
            ascending = True
        else:
            # continuation of ascending or descending sequence
            memo[i] = memo[i-1]

    # backtracking to find solution
    # index list of oscillation sequence, add the last coordinate in L because
    # the last coordinate is always either a valley or a peak
    # aux space complexity: O(N)
    oscillation = [len(L)-1]

    # time complexity: O(N)
    for i in range(len(memo)-2, 0, -1):
        if memo[i+1] != memo[i]:
            oscillation.append(i-1)

    # reverse oscillation list
    # time complexity: O(N)
    oscillation.reverse()

    # return oscillation length and solutions
    return memo[-1], oscillation


def longest_walk(M):
    """
    Return the length of the longest increasing walk in matrix M, and the
    coordinates of the elements in that walk, in order.

    :precondition:          inner lists in M contains only integers
    :param M:               (list(list)) A list of n lists with each inner list
                            being length m- can contain duplicates and can be
                            empty

    :time complexity:       Best Case:
                            O(nm), where n is the length of the input list, M,
                            and m is the length of each inner list in the
                            input list, M. This is the same as the worst case
                            since none of the loops exit early, see below.

                            Worst Case:
                            O(nm), where n is the length of the input list, M,
                            and m is the length of each inner list in the
                            input list, M. Creating the memo matrix takes O(nm)
                            time and creating the decision matrix also
                            takes O(nm) time. Updating the memo and decision
                            matrix takes O(nm) time. Within this nested for
                            loop, we call _longest_walk_aux() which will
                            run at most O(nm) times to fill up the memo matrix.
                            Once the memo matrix is filled, every subsequent
                            call to _longest_walk_aux() is O(1). Therefore,
                            the total cost of this entire nested for loop and
                            updating the memo and decision matrix is
                            O(nm + nm) which gives us a complexity of O(nm).
                            Finding the length of the longest walk requires
                            us to traverse through each position in the memo
                            matrix which takes O(nm) time. Finding the
                            coordinates that belong to this longest walk
                            requires us to traverse through the decision
                            matrix which takes at most O(nm) time if the
                            walk goes through all the elements in M. Thus,
                            this gives us a total time complexity of O(nm).

    :space complexity:      O(nm), where n is the length of the input list, M,
                            and m is the length of each inner list in the
                            input list, M. This is because the input matrix M
                            takes O(nm) space and the aux space complexity of
                            this function is O(nm). This gives us a total
                            space complexity of O(2nm) which is O(nm).

    :aux space complexity:  O(nm), where n is the length of the input list, M,
                            and m is the length of each inner list in the
                            input list, M. The memo array takes O(nm) space.
                            The decision array takes O(nm) space.
                            _longest_walk_aux() has a aux space of O(nm)
                            due to its recursive nature. The path list
                            takes at most O(nm) space. Thus, this gives
                            us a total aux space complexity of O(4nm) which is
                            O(mm).

    :return:                (tuple) The first element of the tuple is a number
                            representing the length of the longest walk in M
                            and the second element in the tuple is a list of
                            2-element tuples which represent the (row, column)
                            coordinates of the elements M, which make up the
                            longest increasing walk, in the same order
                            as they would be traversed during that walk.
    """
    # handle boundary cases
    if M is None:
        return 0, []
    if len(M) < 1:
        return 0, []
    if len(M[0]) < 1:
        return 0, []

    # create memo matrix which will hold the lengths of the longest possible
    # walks from each position in M
    # time complexity: O(nm)
    # aux space complexity: O(nm)
    memo = [[]] * (len(M))
    for i in range(len(memo)):
        memo[i] = [None] * len(M[i])

    # create a decision matrix to keep track of possible solutions
    # time complexity: O(nm)
    # aux space complexity: O(nm)
    decision = [[]] * len(M)
    for i in range(len(decision)):
        decision[i] = [None] * len(M[i])

    # update memo and decision matrices with solutions
    # time complexity: O(nm + nm) -> O(nm)
    for i in range(len(memo)):
        for j in range(len(memo[i])):
            # time complexity: O(nm) at most
            # aux space complexity: O(nm)
            val = _longest_walk_aux(M, memo, i, j)
            memo[i][j] = 1 + val[0]
            decision[i][j] = val[1]

    # declare a variable for the length of the longest walk in the
    # entire matrix
    max_path_length = 0
    # declare a variable for the coordinates of the next element in this
    # longest walk
    max_path_index = 0, 0

    # find the longest walk in the entire memo matrix
    # time complexity: O(nm)
    for i in range(len(memo)):
        for j in range(len(memo[i])):
            if memo[i][j] > max_path_length:
                # update longest walk length and coordinates when appropriate
                max_path_length = memo[i][j]
                max_path_index = i, j

    i = max_path_index[0]
    j = max_path_index[1]
    # declare a path array to keep track of the coordinates in the longest walk
    path = [(i, j)]

    # use the decision matrix to find the all coordinates that belong
    # to the longest walk
    while memo[i][j] > 1:
        # if memo[i][j] < 1, this means it is the end of the walk
        pos = decision[i][j]
        path.append(pos)
        # update i and j indexes
        i = pos[0]
        j = pos[1]

    return max_path_length, path


def _longest_walk_aux(M, memo, i, j):
    """
    Return the length of the longest walk that starts at memo[i][j] and the
    (row, column) coordinates of the next element in this walk. This is
    the recursive auxiliary function for longest_walk().

    :param M:               (list(list)) A list of n lists with each inner list
                            being length m- can contain duplicates and can be
                            empty. This is the same input list as longest_walk()
                            function and contains all the required data to
                            calculate the possible walks and decide on the
                            largest one.

    :param memo:            (list(list)) A list of n lists with each inner
                            list being length m.
    :param i:               (int) The row coordinate in M we are currently
                            analysing.
    :param j:               (int) The column coordinate in M we are currently
                            analysing.

    :time complexity:       Best Case: O(1). This occurs when the
                            elements that are surrounding memo[i][j] in memo
                            are not None, i.e., the memo has
                            already been filled with solutions (memoisation has
                            been completed for these positions).
                            Then, go through the for loop which runs 8 times to
                            find the maximum walk length out of the 8 possible
                            directions you can go (up, down, left, right, up
                            left, up right, down left, down right) and then
                            just immediately return value of the appropriate
                            position in memo for the length of the longest walk
                            and then the coordinates of the next element in
                            this longest walk to put in the decision array. This
                            gives a time complexity of O(8) which is O(1).

                            Worst Case: O(nm), where n is the length of the
                            input list, M, and m is the length of each inner
                            list in the input list, M. This occurs when
                            all the elements in memo are None and it is
                            possible to create a walk from M[i][j] that includes
                            all other elements in M. This function will then
                            recursively call itself nm times to fill up
                            the entire memo matrix (complete the memoisation).
                            It is important to note that once all the elements
                            in memo are filled (not None), every subsequent
                            call to this function will be O(1). Although
                            there is a for loop, this for loop always
                            runs 8 times- thus is O(1) complexity and does
                            not affect our total worst case complexity of O(nm).

    :space complexity:      O(nm), where n is the length of the
                            input list, M, and m is the length of each inner
                            list in the input list, M. This is because the
                            aux space complexity is O(nm) and the size
                            of each input list is also O(nm), giving
                            a total space complexity of O(nm).

    :aux space complexity:  O(nm), where n is the length of the
                            input list, M, and m is the length of each inner
                            list in the input list, M. This is because at its
                            worst case, the function will recursive call itself
                            O(nm) times- to fill up the entire memo matrix,
                            thus the recursion call stack will be O(nm).

    :return:                (tuple) The first element of the tuple is an
                            integer which represents the length of the longest
                            walk that starts at memo[i][j]. The second element
                            of the tuple is another tuple that represents
                            the (row, column) coordinates of the next element
                            in this walk.
    """

    # max_path is the length of the longest possible walk that starts at
    # M[i][j]
    max_path = 0
    # max_path_index is the coordinates of the next element in the longest
    # walk that starts from M[i][j] or (0,0) if this is the last element
    # in this walk
    max_path_index = 0, 0

    # combination of coordinates to represent 8 possible movements
    # up, down, left, right, up left, up right, down left, down right
    combos = ((i-1, j), (i+1, j), (i, j-1), (i, j+1),
              (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1))

    # for loop will run 8 times
    for combo in combos:
        row, col = combo[0], combo[1]
        try:
            # ensure coordinates are within the bounds of the matrix,
            # otherwise raise an assertion error because this move
            # is not possible
            assert 0 <= row < len(M)
            assert 0 <= col < len(M[row])

            if M[row][col] > M[i][j]:
                if memo[row][col] is None:
                    # calculate longest walk from this position if not
                    # already calculated
                    memo[row][col] = 1 + _longest_walk_aux(M, memo, row, col)[0]
                if memo[row][col] > max_path:
                    # update max_path and max_path index if appropriate
                    max_path = memo[row][col]
                    max_path_index = combo
        except AssertionError:
            pass

    return max_path, max_path_index

