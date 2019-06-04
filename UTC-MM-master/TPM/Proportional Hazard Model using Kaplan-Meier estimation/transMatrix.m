% Hazard Ratio using Cox Proportional Hazards Regression
HR = zeros(1,6);
for i = 1:6
data = xlsread('PHM_data.xlsx',i);

X = data(:,3);
T = data(:,1);
b = coxphfit(X,T);
HR(i) = exp(b);
end


% Transition probability


Prob = zeros(1,6);

for i = 1:6
data = xlsread('KM_data.xlsx',i);
y = data(:,1);
cens = data(:,3);
[f,x] = ecdf(y,'function','survivor');

Prob(i) = f(2,:);

end    


% Transition Matrix
P99 = Prob(1,1)^HR(1,1);
P98 = (1-Prob(1,1))^HR(1,1);
P88 = Prob(1,2)^HR(1,2);
P87 = (1-Prob(1,2))^HR(1,2);
P77 = Prob(1,3)^HR(1,3);
P76 = (1-Prob(1,3))^HR(1,3);
P66 = Prob(1,4)^HR(1,4);
P65 = (1-Prob(1,4))^HR(1,4);
P55 = (1-Prob(1,5))^HR(1,5);
P54 = Prob(1,5)^HR(1,5);
P44 = Prob(1,6)^HR(1,6);
P43 = (1-Prob(1,6))^HR(1,6);

transProbMatrix = [P99 P98 0 0 0 0 0;0 P88 P87 0 0 0 0;0 0 P77 P76 0 0 0;0 0 0 P66 P65 0 0;0 0 0 0 P55 P54 0;0 0 0 0 0 P44 P43;0 0 0 0 0 0 1]

% Compute future condition state
% A bridge has been in CR7 for 3 years already and want to know CR an
% addition 5 years into the future, n = 8
% CR at 5 years into the future is P(n) = Intial*transMatrix^(n)