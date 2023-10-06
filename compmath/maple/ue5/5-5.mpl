
restart; # clear workspace
;
Digits:=20: # use 20 decimal digits in floating point computations
;
interface(displayprecision=10): # display 10 decimal digits of float objects by default
;

with(ListTools):

printStack := proc(A, name:="");        # access to stack elements (besides to one) ist cumbersome...
    local cpy, lst;

    cpy := copy(A);
    lst := [];
    
    while not stack[empty](cpy) do
        lst := [op(lst), stack[pop](cpy)];
    end do;

    print(name = Reverse(lst));

end proc:


ToH := proc(A, B, C, n, name_A:="A", name_B:="B", name_C:="C");

    if n = 0 then
        return;
    end if;

    ToH(A, C, B, n-1, "A", "C", "B");
    stack[push](stack[pop](A), C);

    print("moving disk...");
    printStack(A, name_A);
    printStack(B, name_B);
    printStack(C, name_C);

    ToH(B, A, C, n-1, "B", "A", "C");

end proc:
NULL;
n := 6:

A := stack[new]():
B := stack[new]():
C := stack[new]():

for i from n by -1 to 1 do
    stack[push](i, A);
end do:

printStack(A, "A");

ToH(A,B,C,n);





















































