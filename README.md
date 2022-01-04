# Test Samples

Python script for testing and validating competitive programming test cases

Additionaly it defines macros in cc templates for debuging 

It will compair the output of the program with the expected output of the problem statement

This script will only work with specific cc program file templates

### Example

##### Input

```shell
testsamples <filename>
```
##### Output

```shell
#0 __VA_ARGS__ (a - b): 0
#1 __VA_ARGS__ (a - b): -1
#2 __VA_ARGS__ (a - b): 0
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

1/3 Tests Passed

Found: 5 ~ Expected: 3 ~ Missmatch_On_Line: 2
Found: 10 ~ Expected: 9 ~ Missmatch_On_Line: 3

```