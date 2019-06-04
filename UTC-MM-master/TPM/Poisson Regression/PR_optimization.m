% optimization of Poisson Regression object function

lb = []; % lower bound
ub = []; % upper bound

betaInit = [0.001]; %initial values

A = []; % No linear inequality constraints
B = [];
Aeq = []; % No linear equality constraints
Beq = [];


[beta, fval] = fmincon(@PR_objFun, betaInit, A, B, Aeq, Beq, lb, ub)