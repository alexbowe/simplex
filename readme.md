Simplex
=======

Simplex is a tool to generate rows of Pascal's generalised triangle (simplex in n dimensions).

To use it, run it with two parameters: first the row number, then the number of dimensions.

Here is an example of its use:

    $ python simplex.py 3 2
    0,3 1
    2,1 3

This has generated each unique element in the third row of the 2D simplex.

The first field is the 2D integer partition that adds up to 3, the second field (separated by a space) is the value at that position in the simplex. Note that the partition (3,0) and (1,2) are not present, because they are equivalent to the values here. In other words, this program generates a table of the unique integer partitions only.

I have plans to add something to order these based on *all* integer partition permutations, and output to graphviz format.

This code is free to do whatever you want with.
