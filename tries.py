class Node:
    """
    Node class for Trie.

    """
    def __init__(self, data=None):
        """
        Initialise a new Node with data, level and size.

        :param data:    The data payload.

        :time complexity:   O(1). Initialising all the variables takes constant
                            time.

        :space complexity:  O(1). Initialising all the variables takes constant
                            space.

        :aux space complexity:  O(1). Initialising all the variables takes
                                constant space.

        :return:    None
        """
        # size is 27 because 26 alphabets and 1 terminal character
        # [$, a, b, c, ..., z]
        size = 27
        self.link = [None] * size   # link to next node

        self.data = data        # data payload

        self.freq = 0           # total number of words with this prefix
        self.unique_freq = 0    # total number of unique words with this prefix


class Trie:
    """
    Trie class.

    """

    def __init__(self, text):
        """
        Initialise a new Trie with a list of strings, text.

        :precondition:          The input, text, is a list of strings.
                                Each string is text is composed only of lower-
                                case English alphabet characters. No empty
                                strings in text.

        :param text:            A list of strings each of which will be
                                composed only of lowercase English alphabet
                                characters. No empty strings, but the list
                                may be empty and may contain duplicates.

        :time complexity:       Best Case:  O(T), where T is the total number
                                of characters over all the strings in the
                                input list, text. This is the same as the
                                worst case, see below.

                                Worst Case: O(T), where T is the total number
                                of characters over all the strings in the
                                input list, text. The function calls
                                insert() which has a time complexity which has
                                a time complexity of O(D) where D is the
                                total number of characters in its input. We
                                are calling insert() for every string in text,
                                thus this equates to T which is the total
                                number of characters over all the strings in
                                text.

        :space complexity:  O(T), where T is the size of the input list,
                            text. This function has an aux space of O(L) but
                            L is always less than or equal to T, thus,
                            the total space complexity is O(T).

        :aux space complexity:  O(L), where L is the total number of characters
                                of the longest string in text. This is because
                                insert() has an aux space complexity of O(D),
                                where D is the total number of characters
                                of the string currently being inserted into the
                                trie. Thus, the size of the recursion stack is
                                bounded by O(L).

        :return:                None
        """
        self.root = Node()
        for data in text:
            self.insert(data)

    def insert(self, data):
        """
        Add data into trie.

        :param data:    (String) Data to insert to the tree.

        :time complexity:   Best Case: O(D), where D is the total number
                            of characters in data. This is the same as the
                            worst case, see below.

                            Worst Case: O(D), where D is the total number
                            of characters in data. This function calls
                            _insert_aux() which has a worst case time
                            complexity of O(D).

        :space complexity:  O(D), where D is the total number of characters
                            in data. This is because the input string, data has
                            D characters and the aux space of this
                            function is O(D).

        :aux space complexity:  O(D), where D is the total number of characters
                                in data. This is because the function calls
                                _insert_aux() which has an aux space of
                                O(D) due to its recursive nature.

        :return:    None
        """
        # begin from root
        current = self.root
        self.root.unique_freq += self._insert_aux(current, data, 0)

    def _insert_aux(self, current, data, curr_index):
        """
        Insert data into trie.

        :param current:     (Node) Current node we are at.
        :param data:        (String) Data to insert.
        :param curr_index:  (int) Current index of data we are inserting.

        :time complexity:   Best Case: O(D), where D is the total number
                            of characters in data. This is the same as the
                            worst case, see below.

                            Worst Case: O(D), where D is the total number
                            of characters in data. This function recursively
                            calls itself D times until it either creates a new
                            node (if character in data does not exist) or
                            traverses an existing node until data is added
                            into the Trie and the appropriate variables
                            are updated.

        :space complexity:  O(D), where D is the total number of characters
                            in data. This is because the input string, data has
                            D characters and the aux space of this
                            function is O(D).

        :aux space complexity:  O(D), where D is the total number of characters
                                in data. This is because the function
                                recursively calls itself D times so the
                                recursion stack will take D space.

        :return:    (int) Returns 1 if a new word is added to the trie,
                    otherwise return 0.
        """

        current.freq += 1

        if curr_index == len(data):

            # check if leaf node already exists
            if current.link[0] is not None:
                # leaf node exists
                # increase leaf node freq but not unique_freq
                current.link[0].freq += 1

                return 0
            else:
                # leaf node does not exist
                # increase freq and unique_freq and create new node with data
                current.unique_freq += 1

                leaf = Node(data)
                leaf.freq += 1
                leaf.unique_freq += 1

                current.link[0] = leaf

                return 1
        else:
            # calculate index to insert the new character into
            index = ord(data[curr_index]) - 97 + 1

            # check if path exists
            if current.link[index] is not None:
                # path exists
                current = current.link[index]
            else:
                # path does not exist
                # create a new node
                current.link[index] = Node()
                current = current.link[index]

        if self._insert_aux(current, data, curr_index + 1) == 1:
            current.unique_freq += 1
            return 1

        return 0

    def string_freq(self, query_str):
        """
        Return number of elements of the text which are exactly query_str.
        Do not count instances where query_string occurs as a proper substring
        of some element of the text. Return 0 if query_str does not match
        any elements of the text.

        :precondition:      query_str is non-empty and only consists of
                            lowercase English alphabet characters.

        :param query_str:   A non-empty string consisting only of lowercase
                            English alphabet characters.

        :time complexity:   Best Case: O(1). This occurs when query_str
                            does not exist in this trie. Then, we return
                            early in the first for loop.

                            Worst Case: O(q), where q is the length of
                            query_str. This occurs when query_str either
                            exists in the trie or query_str matches a prefix
                            of a string in this Trie but does not match a
                            complete string. Then, the function will go
                            through the for loop q times.

        :space complexity:  O(q), where q is the length of the input string,
                            query_str.

        :aux space complexity:  O(1). This function uses constant auxiliary
                                space.

        :return:            (int) The number of elements of the
                            text which are exactly query_string.
        """
        # start from root
        current = self.root

        for char in query_str:
            # calculate index
            index = ord(char) - 97 + 1

            if current.link[index] is not None:
                current = current.link[index]
            else:
                return 0

        # check leaf node
        if current.link[0] is not None:
            return current.link[0].freq

        # return 0 if leaf node does not exist, this means query_str
        # does not exist in this trie
        return 0

    def prefix_freq(self, query_str):
        """
        Returns the number of words in text which have query_str as a prefix.

        :precondition:      query_str only contains lowercase English alphabet
                            characters
                            query_str may be an empty string
        :param query_str:   (str) String to search in this trie.

        :time complexity:   Best Case: O(1). This occurs when query_str
                            does not exist in the the trie. This function
                            calls _prefix_helper() which has a best case
                            of O(1), see below.

                            Worst Case: O(q), where q is the length of
                            query_str. This occurs when query_str exists
                            in the trie. This function calls _prefix_helper()
                            which has a worst case of O(q) (since we are
                            passing the root of the trie as a parameter),
                            see below.

        :space complexity:      O(q), where q is the length of the input string,
                                query_str.

        :aux space complexity:  O(1). This function uses constant auxiliary
                                space.

        :return:            Returns an integer which represents the number
                            of words that match query_str as a prefix.
        """
        # start from root
        current = self.root
        return self._prefix_helper(query_str, 0, current)

        # Alternate implementation.
        # for char in query_str:
        #     # calculate index
        #     index = ord(char) - 97 + 1
        #
        #     if current.link[index] is not None:
        #         current = current.link[index]
        #     else:
        #         return 0
        #
        # # return current freq
        # return current.freq

    def wildcard_prefix_freq(self, query_str):
        """
        Returns a list containing all the strings which have a prefix which
        matches query_str. These strings must be in lexicographic order.

        :precondition:      query_str is non-empty.
                            query_str consists only of lowercase English
                            alphabet characters (possibly no characters).
                            query_str contains exactly one '?' character,
                            representing a wildcard which can occur at any
                            position in query_str.

        :param query_str:   A non-empty string consisting only of lowercase
                            English alphabet characters (possibly no characters)
                            and exactly one '?' character, representing a
                            wildcard.

        :time complexity:       Best Case: O(1). This occurs when query_str
                                does not exist in this Trie. Then, the function
                                will return an empty list early.

                                Worst Case: O(q + S), where q is the length
                                of query_str and S is the total number of
                                characters in all strings of the text (inclusive
                                of duplicates) which have a prefix matching
                                query_str. The first for loop runs at most
                                q times. The second for loop runs at most
                                27 times and calls _prefix_helper() at each
                                iteration which brings the complexity to O(27q)
                                which is O(q). The time taken to initialise
                                matching_words is always O(S) since the total
                                number of characters is always more than or
                                equal to the number of strings returned in the
                                array. The third for loop runs at most
                                27 times and calls _prefix_find() at each
                                iteration. _prefix_find() has a time complexity
                                of O(q + M), where M is the total number
                                of nodes between a certain node and all the
                                leaves linked to this node. This brings
                                the time complexity to O(27q + 27M). O(27M) is
                                O(S) since in this loop we are traversing
                                through all the characters in all strings of
                                the text which have a prefix matching query_str.
                                Thus, the time complexity is O(27q + S) which
                                is O(q + S). This means the total time
                                complexity is O(q + q + q + S) which is
                                O(q + S).

        :space complexity:      O(q + S), where q is the length of the input
                                string, query_str and S is the total number of
                                characters in all strings of the text which
                                have a prefix matching query_str. This is
                                because this function has an auxiliary space
                                of O(S).

        :aux space complexity:  O(S), where S is the total number of characters
                                in all strings of the text which have a prefix
                                matching query_str. This is because we
                                initialise an array, matching_words. The size
                                of this array, will always be less than or
                                equal to S. This is because the size is
                                initialised to the number of strings which
                                have a prefix of query_str and the number
                                of strings is always less than or equal
                                to the number of characters in these strings.
                                Furthermore, the function calls _prefix_find()
                                which has an aux space of O(M). In this
                                function, M represents the total number of
                                characters in the longest string which has a
                                prefix matching query_str. Thus,  M is always
                                less than or equal to S, so the
                                aux space complexity is O(S).

        :return:            (list) A list of all the strings which have a prefix
                            that matches query_str, in lexicographic order.
        """
        # start from self.root
        current = self.root

        wildcard_index = 0
        # assumes string always contains wildcard "?"
        for char in query_str:
            if char == "?":
                break
            # traverse until you find the wildcard
            index = ord(char) - 97 + 1      # calculate index
            current = current.link[index]

            # return early if query_str does not exist any strings in this Trie
            if current is None:
                return []

            # keep track of index wildcard appears at
            wildcard_index += 1

        # find the number of strings which have a prefix of query_str
        size = 0
        for j in range(1, len(current.link)):
            if current.link[j] is not None:
                size += self._prefix_helper(query_str, wildcard_index + 1,
                                            current.link[j])

        matching_words = [None] * size  # initialise a new array with size
        count = 0   # track number of strings inserted into matching_words
        wildcard_index += 1

        # loop through all links except for terminal node and add
        # to matching_words
        for j in range(1, len(current.link)):
            curr_node = current.link[j]
            if curr_node is not None:
                count = self._prefix_find(query_str, wildcard_index,
                                          curr_node, matching_words, count)

        return matching_words

    def _prefix_helper(self, query_str, curr_index, curr_node):
        """
        Return the number of words in this Trie that match query_str as a
        prefix if any, otherwise return 0.

        :precondition:      curr_node is not None.
        :param query_str:   (str) The prefix string we are searching for.
        :param curr_index:  (int) Current index we are looking at for query_str.
        :param curr_node:   (Node) The current node we are traversing.

        :time complexity:   Best Case: O(1). This occurs when query_str
                            does not exist in the the trie, so we
                            break out of the loop early and return 0.

                            Worst Case: O(q), where q is the length of
                            query_str. This occurs when query_str exists
                            in the trie. The for loop iterates q times and
                            finds the node in the Trie whose path corresponds
                            to query_str and then returns the frequency of this
                            node.

        :space complexity:      O(q), where q is the length of the input
                                string, query_str.

        :aux space complexity:  O(1). This function uses constant auxiliary
                                space.

        :return:            (int) Returns the number of words that match
                            query_str as a prefix.
        """

        # start from current node
        current = curr_node

        while curr_index < len(query_str):
            char = query_str[curr_index]
            # calculate index
            index = ord(char) - 97 + 1

            if current.link[index] is not None:
                current = current.link[index]
            else:
                return 0

            curr_index += 1

        # return current freq
        return current.freq

    def _prefix_find(self, query_str, curr_index, curr_node, array, count):
        """
        Find query_str in this Trie and then find all the strings in this
        Trie that match query_str as a prefix and add these strings to array.

        :param query_str:   (str) The prefix string we are searching for.
        :param curr_index:  (int) Current index we are looking at for query_str.
        :param curr_node:   (Node) The current node we are traversing.
        :param array:       (list) An array of strings.
        :param count:       (int) The number of strings inside array.

        :time complexity:   Best Case: O(1). This occurs when query_str
                            does not exist in this Trie so the function
                            will return early as seen in the for loop.

                            Worst Case: O(q + M), where q is the length of
                            query_str and M is the total number of nodes
                            between curr_node and all the leaves that are
                            linked to curr_node. The for loop will loop
                            at most q times. This function calls _find_data()
                            which has time complexity of O(M). Thus,
                            the total worst case time complexity is O(M).

        :space complexity:      O(q + N + M), where q is the length of the
                                input string, query_str and N is the length of
                                the input array and M is the total number of
                                nodes between curr_node (the node that
                                corresponds to the very last character in
                                query_str) and all the leaves that are linked
                                to this node. This is because this function
                                has an aux space of O(M).

        :aux space complexity:  O(M), where M is the total number of nodes
                                between curr_node (the node that corresponds to
                                the very last character in query_str) and all
                                the leaves that are linked to this node.
                                This is because this function calls _find_data()
                                which has an aux space of O(M) since it is
                                recursive.

        :return:                (int) The number of strings inside array.
        """

        # traverse until the end of query_str
        for i in range(curr_index, len(query_str)):
            char = query_str[i]
            # calculate index
            index = ord(char) - 97 + 1
            if curr_node is not None:
                curr_node = curr_node.link[index]
            else:
                return count

        if curr_node is not None:
            # find all the matching words
            count = self._find_data(curr_node, array, count)

        return count

    def _find_data(self, curr_node, array, count):
        """
        Find all the leaf nodes of curr_node and add the data of each leaf into
        array at the appropriate position. Return the number of strings
        that are currently in array.

        :param curr_node:       current node
        :param array:           array of strings
        :param count:           number of strings currently in array

        :time complexity:       Best Case: O(M), where M is the total number
                                of nodes between curr_node and all the leaves
                                that are linked to curr_node. This is the
                                same as the worst case, see below.

                                Worst Case: O(M), where M is the total
                                number of nodes between curr_node and all
                                the leaves that are linked to curr_node. This
                                is because the function will traverse to
                                all the leaf nodes of curr_node and
                                add the data from each leaf into the
                                array.

        :space complexity:      O(N + M), where N is the length of the input
                                array and M is the total number of nodes
                                between curr_node and all the leaves that
                                are linked to curr_node. This is because
                                this function has an aux space complexity
                                of O(M).

        :aux space complexity:  O(M), where M is the total number of nodes
                                between curr_node and all the leaves
                                that are linked to curr_node. This is because
                                the function is recursively called
                                M times and so the size of the recursion
                                stack is M.

        :return:                (int) the number of strings currently
                                in array.
        """

        return self._find_data_aux(curr_node, array, count)

    def _find_data_aux(self, curr_node, array, count):
        """
        Auxiliary function for _find_data().

        :param curr_node:       current node
        :param array:           array of strings
        :param count:           number of strings currently in array

        :time complexity:       Best Case: O(M), where M is the total number
                                of nodes between curr_node and all the leaves
                                that are attached to curr_node. This is the
                                same as the worst case, see below.

                                Worst Case: O(M), where M is the total
                                number of nodes between curr_node and all
                                the leaves that are attached to curr_node. This
                                is because the function will traverse to
                                all the leaf nodes of curr_node and
                                add the data from each leaf into the
                                array.

        :space complexity:      O(N + M), where N is the size of the input
                                array and M is the total number of nodes
                                between curr_node and all the leaves that
                                are linked to curr_node. This is because
                                this function has an aux space complexity
                                of O(M).

        :aux space complexity:  O(M), where M is the total number of nodes
                                between curr_node and all the leaves
                                that are linked to curr_node. This is because
                                the function is recursively called
                                M times and so the size of the recursion
                                stack is M.

        :return:                (int) the number of strings currently
                                in array.
        """

        # check if leaf exists
        if curr_node.link[0] is not None:
            # if leaf exists, update the array with its data
            leaf = curr_node.link[0]
            for _ in range(leaf.freq):
                array[count] = leaf.data
                count += 1

        # loop through all other possible links and repeat
        for i in range(1, len(curr_node.link)):
            next_node = curr_node.link[i]
            if next_node is not None:
                count = self._find_data_aux(next_node, array, count)

        return count

