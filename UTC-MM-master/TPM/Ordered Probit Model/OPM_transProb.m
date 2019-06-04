beta = theta(1);
theta1 = theta(2);
theta2 = theta(3);
% theta3 = theta(4);
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



prob = zeros(nrows,2);


for i = 1:nrows

        prob(i,1) = normcdf(theta1 - beta * X(i));

        prob(i,2) = normcdf(theta2 - beta * X(i)) - normcdf(theta1 - beta * X(i));

        prob(i,3) = normcdf(theta3 - beta * X(i)) - normcdf(theta2 - beta * X(i));
%        
%         prob(i,4) = normcdf(theta4 - beta * X(i)) - normcdf(theta3 - beta * X(i));
%         
%         prob(i,5) = normcdf(theta5 - beta * X(i)) - normcdf(theta4 - beta * X(i));
%         
%         prob(i,6) = normcdf(theta6 - beta * X(i)) - normcdf(theta5 - beta * X(i));
%         
%         prob(i,7) = normcdf(theta7 - beta * X(i)) - normcdf(theta6 - beta * X(i));
%         
%         prob(i,8) = normcdf(theta8 - beta * X(i)) - normcdf(theta7 - beta * X(i));
%         
%         prob(i,9) = normcdf(theta9 - beta * X(i)) - normcdf(theta8 - beta * X(i));
%         
%         prob(i,10) = 1 - normcdf(theta9 - beta * X(i));
%         
    end
transProb9 = zeros(1,3);
for i = 1:3
    transProb9(1,i) = sum(prob(:,i))/nrows;
end
       
transMatrix = [transProb9(1) transProb9(2) transProb9(3) 0 0 0 0;
               0 transProb8(1) transProb8(2) transProb8(3) 0 0 0;
               0 0 transProb7(1) transProb7(2) transProb7(3) 0 0;
               0 0 0 transProb6(1) transProb6(2) transProb6(3) 0;
               0 0 0 0 transProb5(1) transProb5(2) transProb5(3);
               0 0 0 0 0 transProb4(1) transProb4(2);
               0 0 0 0 0 0 1];
        