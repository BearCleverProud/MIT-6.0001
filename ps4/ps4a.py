# Problem Set 4A
# Name: <BearCleverProud>
# Collaborators:None
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    length=len(sequence)
    result=[]
    if length==1:
        return sequence
    else:
        sequence_list=list(sequence)
        for i in range(length):
            sequence_list[i],sequence_list[0]=sequence_list[0],sequence_list[i]
            temp=[sequence_list[0]+x for x in get_permutations(''.join(sequence_list[1:]))]
            result.extend(temp)
            sequence_list[i],sequence_list[0]=sequence_list[0],sequence_list[i]
        return result

if __name__ == '__main__':
    #EXAMPLE
    example_input = 'abcdefgh'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)
