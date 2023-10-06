## Output
```c++
5
<Address of N>
10
```

## Why?
The method `int* getptrN(){ return &N; };`
is the reason this works. It returns the
address of the instance variable `N` of
the instance `A` of the class `Test`. By
gaining access to the pointer of an object
you can manipulate it however you like (e.g.
reading the value, setting a new value).
Which is exactly what this code does in the
line
```c++
*ptr = 10;
```

## Bad Programming Style
You should not do this as
* the set and get methods become useless
* the instance variable `N` is effectively
public now 
* you can not control the value of `N` (e.g.
if `N` should always be bigger than 42, this
can not be checked)
* if for some reason get and set methods are
not sufficient, making `N` public makes the
code more readable and conveys the danger of
unchecked values