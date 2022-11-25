

The target programs in both the $max$ and $array\_search$ problems are of the form:

```
(ite BoolExp1 target1 (ite BoolExp2 target2 (... (ite BoolExpn targetn1 targetn2))))
```

The difficulty in searching such programs is that the search space grows exponentially with the expression length, and in practice most programs can be pruned during the search. For example, for the input and output pairs of functions $(x,y)$, if:

$$Assign(BoolExp1,x)=True \land Assign(target1,x)\ne y$$

Subsequent searches do not need to continue.

Through this pruning method, we reduce the original search space that grows exponentially with the number of targets to linear growth.


The limitation of this algorithm is mainly that it only optimizes the search for the target program of nested $ite$, and we use ordinary limited-width search for programs that do not meet this condition.


1. 
   Filter candidate targets from constraint definitions
   Use predefined rules to filter out the possible return values of the function $[arg0, arg1]$. Then the program we finally generate looks like (ite BoolExp0 arg0 arg1), where BoolExp0 is to be searched.

2. 
   K different assignments of variables defined in the numeration constraint definition file. Enumerate different assignments of variables $[x,y]$, for example, when $k=3$, a possible result is $[(1,2),(2,1),(2,2)]$. 

3. 
   Recursively search for function return values that satisfy all constraints.  We enumerate the different results of $[max2(1,2), max2(2,1), max2(2,2)]$, and then substitute into the constraint to check whether it is satisfied, and finally get the following two results that meet the conditions kind:

	$[max2(1,2)=arg1=2,max2(2,1)=arg0=2,max2(2,2)=arg0=2]$
	$[max2(1,2)=arg1=2,max2(2,1)=arg0=2,max2(2,2)=arg1=2]$

	We get two possible input-output pairs:
	$S_1=[(1,2)\rightarrow arg1,(2,1)\rightarrow arg0,(2,2)\rightarrow arg0]$
	$S_2=[(1,2)\rightarrow arg1,(2,1)\rightarrow arg0,(2,2)\rightarrow arg1]$

4. 
   Use the function input and return value pairs generated in 2 and 3 to search BoolExp.
   
   For these two possible situations, we search for BoolExp respectively. The algorithm of step 4 is as follows:

	```
	Condition: S, Target: BoolExps
	Let: BoolExpk = And(exp1, exp2, ..., expkn)
	Divide the input and output pair S into n sets according to the return value, Si = {pair | pair.target == targeti}
   	for i = 1 to n:
		ni = 0
		S1 = Si
		S2 = Union(Sk), k > i
		remainSize = |S2|
		while remainSize > 0:
			Generate an expression exp from the BoolExp space
			exp_ni = exp
			Si1 = { pair | pair[0] satisfies exp and pair in S1}
			Si2 = { pair | pair[0] satisfies exp and pair in S2}
			if |Si1| < |S1|:
				continue
			if |Si2| == 0:
				ni = ni + 1
             	break
			if |Si2| < |S2|:
				ni = ni + 1
				S2 = Si2
	```

5. 
   For $S1$ and $S2$, step 4 finds a target program that satisfies the input-output pair, uses SMT Solver to confirm whether the generated program is correct.
   
6. 
   If it passes the detection, the search ends, otherwise, increase the number of enumerated assignments to generate more input-output pairs, and start searching again from step 2. ```k = k * 2; goto 2;```