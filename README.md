# Test Samples

----

Python script for testing and validating competitive programming test cases

Additionaly it defines macros in cc templates for debugging 

It will compair the output of the program with the expected output of the problem statement

This script will only work with specific cc program file templates 
examples can be found [Here](https://github.com/BrandonPacewic/CompetitiveProgramming/tree/master/templates)

### Example

##### Input

```shell
testsamples <filename>
```
##### Output

```
#0 [A - B, A * B]: -4 5
Compairing...
Time: 0.003s
-------------
Expected:

10
-------------
Output:

6

-------------

0 / 1 Tests Passed

Found: 6 ~ Expected: 1 ~ MissmatchOnLine: 1

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

```
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