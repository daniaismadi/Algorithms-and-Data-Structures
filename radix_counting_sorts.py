import random
import timeit
import csv


def radix_sort(num_list, b):
    """
    Performs radix sort on num_list (a list of integers) with base b.

    :param num_list:        (list) The list of numbers to sort.
    :param b:               (int) The base to sort the numbers to.
    :time complexity:       Best Case: O((N + b)M), where N is the total
                            number of integers in the input list, b is the
                            base, M is the number of digits in the largest
                            number in the input list, when represented in base
                            b. This is the same as the worst case, see below.

                            Worst Case: O((N + b)M), where N is the total
                            number of integers in the input list, b is the base,
                            M is the number of digits in the largest number in
                            the input list, when represented in base b. This
                            occurs when there are more than two numbers in list.
                            Initialising final_array takes O(N) time. The outer
                            while loop will iterate a maximum of M times
                            since you have to sort through each digit
                            for each number. Initialising count_array takes O(b)
                            time, updating count_array takes O(N) time,
                            and updating final_array takes O(N + b) time
                            because outer for ;oop will iterate b times but the
                            inner for loop will iterate at most N times
                            throughout the entire execution of the outer loop.
                            Thus, the total worst case runtime is O((N + b)M).

    :space complexity:      O(N + b), where N is the length of num_list and
                            b is the base given. Auxiliary space complexity
                            is O(N + b) and input space is O(N). Thus,
                            space complexity is O(N + b).

    :aux space complexity:  O(N + b), where N is the length of num_list
                            and b is the base given. This is because
                            final_array (the array to return) takes O(N) space
                            since it has a size of N and count_array takes
                            O(b) space as it is initialised to a list of size
                            b at most. Thus, the auxiliary space complexity
                            is O(N + b).

    :return:                (list) the sorted num_list, final_array
    """

    # check boundary cases, an empty list and a list with one number are
    # already sorted
    if len(num_list) < 2:
        return num_list

    # initialise final_array, the array to return
    final_array = [None] * len(num_list)
    for i in range(len(num_list)):
        final_array[i] = num_list[i]
    done = False
    col = 0

    while not done:

        # initialise count_array with separate chaining
        # complexity: O(b)
        count_array = [None] * (b + 1)
        for i in range(len(count_array)):
            count_array[i] = []

        # update count_array with separate chaining
        # complexity: O(N)
        max_integer_div = 0
        for item in final_array:
            curr = (item // b ** col)
            if curr > max_integer_div:
                max_integer_div = curr
            curr_digit = curr % b
            count_array[curr_digit].append(item)

        # check if you should break out of loop
        # i.e. check if you are done checking all the columns
        if max_integer_div == 0:
            done = True
            break

        # update final_array
        # complexity: O(b + N), outer loop will iterate b times and inner
        # loop will iterate at most N times.
        index = 0
        for i in range(len(count_array)):
            item_pos = 0
            frequency = len(count_array[i])
            for j in range(frequency):
                final_array[index] = count_array[i][item_pos]
                index += 1
                item_pos += 1

        # update col variable to check next column
        col += 1

    return final_array


def time_radix_sort():
    """
    Returns a list of tuples with (base, time) after timing radix sort on random
    sequence of numbers with different bases. Writes the tuples into a csv
    file called 'output_test.csv'.

    :time complexity:       Best and Worst Case: O(1). The function does not
                            depend on an input size.

    :space complexity:      O(1). The function does not use an input and
                            has O(1) auxiliary space.
    :aux space complexity:  O(1). The function uses constant auxiliary space.

    :return                 (list) a list of tuples noting the (base, time)

    """
    base_list = []
    # for i in range(1, 24):
    #     base_list.append(2**i)

    for i in range(1, 24):
        base_list.append(10**i)

    # Open csv file
    with open('output_test.csv', 'w', newline='') as csv_file:

        # Initialise writer for csv.
        writer = csv.writer(csv_file)
        time_list = []
        for base in base_list:
            # initialise a new row to write
            row_to_write = [base]
            # call random.seed() to ensure a proper distribution of numbers
            random.seed(99)
            # create test data
            test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]
            # start timer
            start = timeit.default_timer()
            radix_sort(test_data, base)
            # end timer
            time = timeit.default_timer()-start

            # append to time_list and row_to_write
            time_list.append((base, time))
            row_to_write.append(time)

            # Print row_to_write into the csv file.
            writer.writerow(row_to_write)

    return time_list


def find_rotations(string_list, p):
    """
    Return a list of strings that also appear in string_list after it has been
    rotated p times (rotated left if p is positive and rotated right if p is
    negative).


    :precondition:          Each string in string_list is unique. Strings in
                            the list will only contain lowercase alphabet
                            character (a-z).

    :param string_list:     (list)  a list of strings
    :param p:               (int)   number of left rotations if p is positive
                            or right rotations is p is negative

    :time complexity:       Best Case and Worst Case: O(NM), where N is the
                            number of strings in string_list and M is the
                            maximum number of characters in a string, amongst
                            all strings in string_list. This is because
                            going each string in the list, rotating it
                            p times and appending it back to the list takes
                            O(NM) time. Furthermore, after pre-processing
                            and sorting the list, we need to find the duplicates
                            in temp_array to find the desired strings and
                            this function _find_duplicates() takes O(NM) time
                            due to the comparison cost. Furthermore,
                            we take the desired strings and rotate it back p
                            times as we want the final output to be
                            the same as the strings in the original list, not
                            the rotated strings, and this costs at most
                            O(NM) time. Therefore, the worst case time
                            complexity is O(NM) time. The best case time
                            complexity is O(NM) time still because going
                            through the input list and rotating the strings
                            always has to be done and this is always O(NM) time.

    :space complexity:      O(N+M), where N is the number of strings in
                            string_list and M is the number of characters in a
                            string, amongst all the strings in string_list.
                            Auxiliary space complexity is O(N+M) and input
                            list size is O(N), thus total space
                            complexity is O(N+M).

    :aux space complexity:  O(N+M), where N is the number of strings in
                            string_list and M is the number of characters in
                            a string, amongst all the strings in string_list.
                            This is because we create two new temporary arrays
                            (temp_array and final_array) that are at most
                            O(N) size. Furthermore, auxiliary space of external
                            functions called such as  _p_rotation() and
                            _pre_process() have an auxiliary space of O(M) while
                            _find_duplicates() has an auxiliary space of O(N).
                            Thus, total auxiliary space is O(N+M).

    :return:                (list) a new list of strings whose rotations
                            also appear in string_list
    """

    # create temporary array to store string_list values so we do not modify
    # the input list
    # complexity: O(N)
    # aux space: O(N)
    temp_array = [""] * len(string_list)
    for i in range(len(string_list)):
        temp_array[i] = string_list[i]

    # for string in string_list, rotate string and append to string_list
    # complexity: O(NM)
    # aux space of _p_rotation: O(M)
    n = len(temp_array)
    for i in range(n):
        temp_array.append(_p_rotation(temp_array[i], p))

    # pre-process string_list according to length of string
    # complexity worst case: O(N + M)
    # aux space: O(M)
    temp_array = _pre_process(temp_array)

    # radix sort on entire list, temp_array
    # complexity: O(N + M)
    # aux space: O(1)
    temp_array = _radix_sort_alphabet(temp_array)

    # remove duplicates and store in final_array
    # complexity worst case: O(NM)
    # aux space: O(N)
    final_array = _find_duplicates(temp_array)

    # for string in final_array, undo the p-rotation to get the original
    # string
    # complexity worst and best case: O(NM)
    # aux space: O(M)
    for i in range(len(final_array)):
        final_array[i] = _p_rotation(final_array[i], p*-1)

    # return final_array
    return final_array


def _p_rotation(string, p):
    """
    Return string rotated left p times if p is positive or right p times if p
    is negative.

    :param string:  (str) the string to rotate
    :param p:       (int) the number of left or right rotations

    :time complexity:   Best Case: O(M). This occurs when the length
                        of the string is less than two since a string with
                        one character or less will always be the same regardless
                        of how many times it is rotated, thus the function
                        returns early if this is the case.

                        Worst Case: O(M), where M is the length of the
                        string. This is because to split the string into a list
                        of characters, it takes O(M) time and then to rotate the
                        strings it takes O(2p) time, where p is the number of
                        rotations. p has been manipulated to always be less than
                        M, therefore the total time complexity is O(M + 2p)
                        which is less than O(M + 2M) which can be simplified
                        to O(M).

    :space complexity:      O(M), where M is the length of the string. This is
                            because input size is M and we use an auxiliary
                            space of O(M) since we use an additional list
                            of size M.
    :aux space complexity:  O(M), where M is the length of the string. This is
                            because we split the string into a list of size
                            M.

    :return:        (str) the rotated string
    """

    # handle empty string and string with one letter
    if len(string) < 2:
        return string

    # split string into list
    # O(M) complexity
    word = [char for char in string]
    length = len(string)

    # find equivalent of negative p (right rotations) in positive p (left
    # rotations)
    if p < 0:
        p += ((abs(p) // length) + 1) * length

    # to make sure p is always less than len(string)
    p = abs(p) % length

    # complexity: O(p)
    word.extend(word[:p])

    # complexity: O(p)
    return "".join(word[p:])


def _pre_process(string_list):
    """
    Sort string_list in place according to the length of the strings
    in string_list whilst maintaining relative ordering. This modifies
    the input list.

    :param string_list:     (list) the list of strings to sort

    :time complexity:       Best Case: O(N + M), where N is the length
                            of the string_list and M is the length of the
                            longest string in string_list. This is the
                            same as the worst case, see below.

                            Worst Case: O(N + M), where N is the length of
                            string_list and M is the length of the longest
                            string in string_list. This occurs with all
                            inputs that have two or more elements. Finding
                            the length of the longest string in string_list
                            takes O(N) time. Initialising count_array
                            takes O(M) time, updating count_array with
                            the strings takes O(N) time and finally,
                            updating string_list takes O(M + N) time since
                            the outer for loop iterates M times and the inner
                            for loop executes N times throughout the entire
                            execution of the outer loop.

    :space complexity:      O(N + M), where N is the length of string_list and
                            M is the length of the longest string in
                            string_list. The input size is O(N) and auxiliary
                            space is O(M).

    :aux space complexity:  O(M), where M is the length of the longest string
                            in string_list. This is because we initialise
                            a temporary count_array of size M.

    :return:                (list) string_list sorted in order of length
    """

    # if list has less than two elements then it is already processed
    # correctly
    if len(string_list) < 2:
        return string_list

    # find the maximum length in string_list
    # complexity: O(N), where N is the length of string_list
    max_letters = 0
    for string in string_list:
        if len(string) > max_letters:
            max_letters = len(string)

    # initialise count_array with separate chaining
    # complexity: O(M), where M is the maximum length of the longest string
    #  in string_list
    count_array = [[]] * (max_letters + 1)
    for i in range(len(count_array)):
        count_array[i] = []

    # build count_array
    # complexity: O(N)
    for string in string_list:
        count_array[len(string)].append(string)

    # update string_list
    # complexity: O(M + N)
    index = 0
    for i in range(len(count_array)):
        frequency = len(count_array[i])
        for j in range(frequency):
            string_list[index] = count_array[i][j]
            index += 1

    return string_list


def _radix_sort_alphabet(string_list):
    """
    Perform radix sort on string_list which contains lowercase alphabet
    characters. Will be sorted in lexicographic order similar to Python's
    built in sorting function. This function modifies input list.

    :precondition:          string_list is sorted in order of length from
                            shortest to longest
    :param string_list:     (list) the list of strings to sort

    :time complexity:       Best Case:  O(NM), where N is the number of strings
                            in string_list and M is the maximum string length
                            amongst all strings in string_list. This is the
                            same as the worst case, see below.

                            Worst Case: O(NM), where N is the number of strings
                            in string_list and M is the maximum string length
                            amongst all strings in string_list. This occurs
                            with all inputs with 2 elements or more. Outer
                            for loop will iterate M times. Inside the loop,
                            initialising count_array is constant but updating
                            count_array takes at most N times. Finally,
                            updating string_list also takes at most n times.

    :space complexity:      O(N), where N is the number of strings in
                            string_list. This is because aux space complexity
                            is O(1) and the function takes in an input of size
                            N.

    :aux space complexity:  O(1). This algorithm initialises a temporary
                            array of constant size, count_array.

    :return:                (list) a sorted string_list
    """

    # check boundary cases: O(1) complexity
    if len(string_list) < 2:
        return string_list

    # use base 26 because there are 26 letters
    b = 26

    # maximum string length
    max_length = len(string_list[-1])

    # go through each column of characters, assume left alignment, start sorting
    # from the right and go from bottom to top
    # complexity: O(M)
    for col in range(max_length - 1, -1, -1):

        # initialise count_array of size b with separate chaining
        # complexity: O(1) since b is constant
        count_array = [[]] * (b + 1)
        for i in range(len(count_array)):
            count_array[i] = []

        # update count array
        # complexity at worst: O(N)
        item_pos = 0
        try:
            for i in range(len(string_list) - 1, -1, -1):
                string = string_list[i]
                item = ord(string[col]) - 97
                count_array[item].append(string)
                item_pos = i
                i -= 1
        except IndexError:
            pass

        # update string_list by using ch_length as to maintain stability
        # complexity: O(N)
        for i in range(len(count_array)):
            frequency = len(count_array[i])
            for j in range(frequency - 1, -1, -1):
                string = count_array[i][j]
                string_list[item_pos] = string
                item_pos += 1

    return string_list


def _find_duplicates(string_list):
    """
    Return the duplicates in string_list. This does not modify the input list.

    :precondition:          string_list is already sorted, and each string has
                            at most one other string that is the same
    :param string_list:     (list) a list of strings to search

    :time complexity:       Best Case: O(NM), where N is the length of
                            string_list and M is the length of the longest
                            string in string_list. This is the same as
                            the worst case, see below.

                            Worst Case: O(NM), where N is the length of
                            string_list and M is the length of the longest
                            string in string_list. This occurs when there are
                            two strings in string_list. The outer while loop
                            iterates at most N times and the comparison
                            inside the loop takes at most O(M) time since
                            since we are comparing strings. _swap() function
                            takes O(1) time so this is negligible.

    :space complexity:      O(N), where N is the length of string_list since
                            auxiliary space is O(N) and input list is O(N).

    :aux space complexity:  O(N), where N is the length of string_list. This
                            list splicing operation at the end returns
                            a new list that is at most length N.

    :return:                (list) list of strings that are the duplicates
    """

    # handle boundary cases, an empty list or a list with one item in it
    # does not have duplicates, so return early
    if len(string_list) < 2:
        return []

    i = 0
    j = 0

    # go through the list to swap elements that are duplicates and push
    # them to the end of the list
    while i < len(string_list)-1:
        # complexity: O(b)
        if string_list[j] == string_list[i+1]:
            i += 1
        else:
            _swap(string_list, j+1, i+1)
            j += 1
            i += 1

    # all the duplicate values will be at string_list[j+1:] so return this
    return string_list[j+1:]


def _swap(a_list, i, j):
    """
    Swap element at a_list[i] with element at a_list[j] and vice versa.
    Do nothing if i and j are not valid indexes.

    :param a_list:          (list) the list to modify
    :param i:               (int) the index that specifies the element to swap
    :param j:               (int) the index that specifies the element to swap

    :time complexity:       O(1), since accessing and re-assigning elements
                            in a list takes constant time.

    :space complexity:      O(N), where N is the size of the a_list. This is
                            because auxiliary space is O(1).

    :aux space complexity:  O(1), since the algorithm does not require
                            additional space.

    :return:                None
    """

    try:
        a_list[i], a_list[j] = a_list[j], a_list[i]
    except IndexError:
        pass

