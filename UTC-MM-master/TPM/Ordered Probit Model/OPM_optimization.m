% optimization of OPM object function

% lb = [0.0001,0,0,0,0,0,0,0,0,0]; % lower bound
% ub = [9,9,9,9,9,9,9,9,9,9]; % upper bound
lb = [0.0001,0,0,0]; % lower bound
ub = [9,9,9,9]; % upper bound
% thetaInit = [0.5,1,1.2,1.4,1.5,1.6,1.7,1.8,1.9,2.0]; %initial values
thetaInit = [0.5,1,1.2,1.3]; %initial values
A = []; % No linear inequality constraints
B = [];
Aeq = []; % No linear equality constraints
Beq = [];
nonlcon = @const; % constraint function

% options = optimset('PlotFcns',@optimplotfval);

[theta, fval] = fmincon(@OPM_objFun, thetaInit, A, B, Aeq, Beq, lb, ub,nonlcon);
