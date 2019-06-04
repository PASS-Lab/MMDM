% optimization 

LB = [0.00001;0.00001;0.00001;0.00001;0.00001;0.00001]; % lower bound
UB = [0.99999;0.99999;0.99999;0.99999;0.99999;0.99999]; % upper bound

p0 = [0.5;0.5;0.5;0.5;0.5;0.5]; %initial values

A = []; % No linear inequality constraints
B = [];
Aeq = []; % No linear equality constraints
Beq = [];
nonlcon = @const % constraint function

% object function need to be changed to obtain p value for each group
[p, sumValue] = fmincon(@objFun9, p0, A, B, Aeq, Beq, LB, UB, nonlcon);

% Transition Probability Matrix
transMatrix9 = [p(1) 1-p(1) 0 0 0 0 0;0 p(2) 1-p(2) 0 0 0 0;0 0 p(3) 1-p(3) 0 0 0;0 0 0 p(4) 1-p(4) 0 0;0 0 0 0 p(5) 1-p(5) 0;0 0 0 0 0 p(6) 1-p(6);0 0 0 0 0 0 1];