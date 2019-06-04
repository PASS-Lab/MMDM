% optimization of BML
% consider probabilites of tranistion to only next state

LB = [0.00001;0.00001;0.00001;0.00001;0.00001;0.00001]; % lower bound
UB = [0.99999;0.99999;0.99999;0.99999;0.99999;0.99999]; % upper bound

p0 = [0.0 0.6 0.95 0.95 0.97 1]; %initial values
A = []; % No linear inequality constraints
B = [];
Aeq = []; % No linear equality constraints
Beq = [];

[p, sumValue] = fmincon(@objFun, p0, A, B, Aeq, Beq, LB, UB);

p98 = p(1);
p99 = 1-p(1);
p87 = p(2);
p88 = 1-p(2);
p76 = p(3);
p77 = 1-p(3);
p65 = p(4);
p66 = 1-p(4);
p54 = p(5);
p55 = 1-p(5);
p43 = p(6);
p44 = 1-p(6);

transMatrix = [p99 p98 0 0 0 0 0;
    0 p88 p87 0 0 0 0;
    0 0 p77 p76 0 0 0;
    0 0 0 p66 p65 0 0;
    0 0 0 0 p55 p54 0;
    0 0 0 0 0 p44 p43;
    0 0 0 0 0 0 1];