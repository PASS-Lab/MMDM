%Poisson Regression Object function 
% probability(j) = (e^(-lambda)*lambda^j)/j!
% where Z is the drops of states; X is explanatory variable, age in this
% case);
% lambda = e^(beta*X); beta is coefficient
% maxmize to obtain beta
function  sumValue = PR_objFun(beta)

% need to change sheet number to obtain beta for each group
data = xlsread('Poisson_data.xlsx',5);
[nrows, ncols] = size(data);
X = data(:,1);


ZBetaX_expBetaX = zeros(nrows,1);
ZBetaX = zeros(nrows,1);
expBetaX = zeros(nrows,1);

for i = 1:nrows
    Z = data(i,2)-data(i,3);
    ZBetaX(i) = Z*beta*X(i);
    expBetaX(i) = exp(beta*X(i));
    ZBetaX_expBetaX(i) = ZBetaX(i) - expBetaX(i);
    
end

sumValue = -sum(ZBetaX_expBetaX);

end
