%Ordered Probit Object function 
% probability(j) = F(theta(j+1)-beta*X)-F(theta(j)-beta*X)
% where j is the drops of states; X is explanatory variable, age in this
% case); beta is coefficient
function  sumValue = OPM_objFun(theta)

% beta = 0.5;
% theta1 = 1;
% theta2 = 1.2;
% theta3 = 1.4;
% theta4 = 1.6;
beta = theta(1);
theta1 = theta(2);
theta2 = theta(3);
theta3 = theta(4);
% theta4 = theta(5);
% theta5 = theta(6);
% theta6 = theta(7);
% theta7 = theta(8);
% theta8 = theta(9);
% theta9 = theta(10);


% need to change sheet number to obtain theta for each group
data = xlsread('OPM_data.xlsx',1);
[nrows, ncols] = size(data);
X = data(:,1);



prob = zeros(nrows,1);
logProb = zeros(nrows,1);


for i = 1:nrows
    j = data(i,2)-data(i,3);
    if j == 0
    prob(i) = normcdf(theta1 - beta * X(i));
    logProb = log(prob);
    % check log values
    logProb(logProb==-Inf)=0;
    elseif j == 1
        prob(i) = normcdf(theta2 - beta * X(i)) - normcdf(theta1 - beta * X(i));
        logProb = log(prob);
        logProb(logProb==-Inf)=0;
    elseif j == 2
        prob(i) = normcdf(theta3 - beta * X(i)) - normcdf(theta2 - beta * X(i));
        logProb = log(prob);
        logProb(logProb==-Inf)=0;
%     elseif j == 3
%         prob(i) = normcdf(theta4 - beta * X(i)) - normcdf(theta3 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;
%      elseif j == 4
%         prob(i) = normcdf(theta5 - beta * X(i)) - normcdf(theta4 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;
%      elseif j == 5
%         prob(i) = normcdf(theta6 - beta * X(i)) - normcdf(theta5 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;   
%      elseif j == 6
%         prob(i) = normcdf(theta7 - beta * X(i)) - normcdf(theta6 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;
%      elseif j == 7
%         prob(i) = normcdf(theta8 - beta * X(i)) - normcdf(theta7 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;
%      elseif j == 8
%         prob(i) = normcdf(theta9 - beta * X(i)) - normcdf(theta8 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;
%      elseif j == 9
%         prob(i) = 1- normcdf(theta9 - beta * X(i));
%         logProb = log(prob);
%         logProb(logProb==-Inf)=0;   
    end
end
sumValue = -sum(logProb);
end



   