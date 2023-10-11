# Define a function matmul that takes two matrices, m1 and m2, and performs matrix multiplication.

def matmul(m1, m2):

    # Check if the number of columns in m1 is not equal to the number of rows in m2 for valid matrix multiplication.
    if len(m1[0]) != len(m2):
        raise ValueError

    # Check if each row in m1 is iterable.
    for i in range(len(m1)):
        try:
            _ = iter(m1[i])  # Try to iterate over m1[i]
        except TypeError:
            raise TypeError

    # Check if each row in m2 is iterable.
    for i in range(len(m2)):
        try:
            _ = iter(m2[i])  # Try to iterate over m2[i]
        except TypeError:
            raise TypeError

    # Check if each element in m1 is either an int or a float.
    for i in range(len(m1)):
        for x in range(len(m1[i])):
            if isinstance(m1[i][x], int) is False and isinstance(m1[i][x], float) is False:
                raise TypeError


    L = [] #Result matrix

    # Perform matrix multiplication using nested loops.
    for i in range(len(m1)):
        L2 = []  # Initialize a new row for the result matrix.
        for j in range(len(m2[i])):
            t = 0  # Initialize a temporary variable to store the sum of products.
            for k in range(len(m1[i])):
                t += (m1[i][k] * m2[k][j])  # Calculate the product and update t.

            L2.append(t)  # Append the result to the current row.

        L.append(L2)  # Append the current row to the result matrix.


    return L

