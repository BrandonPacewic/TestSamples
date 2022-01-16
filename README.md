# Test Samples

----

Python script for testing and validating competitive programming test cases

Additionaly it defines macros in cc templates for debugging 

It will compair the output of the program with the expected output of the problem statement

This script will only work with specific cc program file templates

### Example

##### Input

```shell
testsamples <filename>
```
##### Output

_VA_ARGS_ is part of the previously mentioned debugging tool

```shell
__VA_ARGS__ (a - b): 0
__VA_ARGS__ (a - b): -1
__VA_ARGS__ (a - b): 0
Compairing...
Time: 0.004s
-------------
Expected:

4
3
9

-------------
Output:

4
5
10

-------------

1 / 3 Tests Passed

Found: 5 ~ Expected: 3 ~ Missmatch_On_Line: 2
Found: 10 ~ Expected: 9 ~ Missmatch_On_Line: 3

```

# Sample Gen

----

Yet another python script for generating the sample .txt files used

by the test samples script

### Example

```shell
sample_gen <file name>
```

##### Input

```shell
[CREATEING FILES] With Base -> <file name>
[INPUT TEXT] Enter Input:
--------------
<sample input>

--------------

[EXPECTED TEXT] Enter Expected
--------------
<sample input>

--------------

[Accepted]

```

### Install

----

For your convenience there is a install script that will create the global commands for you

```
sudo ./INSTALL.sh
```

And enjoy :)