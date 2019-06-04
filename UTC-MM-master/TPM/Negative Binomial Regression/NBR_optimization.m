% optimization of Negative Binomial Regression object function

lb = [-Inf,-Inf,-Inf,-Inf]; % lower bound
ub = [Inf,Inf,Inf,Inf]; % upper bound
betaInit = [0.089,1.1]; %initial values
A = []; % No linear inequality constraints
B = [];
Aeq = []; % No linear equality constraints
Beq = [];


[beta, fval] = fmincon(@NBR_objFun, betaInit, A, B, Aeq, Beq, lb, ub);