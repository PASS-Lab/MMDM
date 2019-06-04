%Negative Binomial Regression Object function 

% lambda = e^(beta*X); beta is coefficient; X is explanatory variable, age in this
% case);
% maxmize to obtain beta and alpha


function  sumValue = NBR_objFun(beta)

% need to change sheet number to obtain beta for each group
% I have a problem to run this code with sheet number 3. !!!!! There are
% empty cells in column 3 of sheet 3 - is that the issue? !!!!!
data = xlsread('Binomial_data.xlsx',1);
[nrows, ncols] = size(data);
X = data(:,1);
Z = zeros(nrows,1);

logLike = zeros(nrows,1);

for i = 1:nrows
    Z(i) = data(i,2)-data(i,3);
    lambda = exp(beta(1)*X(i));
    
    AA = 1/beta(2);
    BB = 1/(1+(beta(2)*lambda));
    CC = gamma(AA+Z);
    DD = gamma(AA)*factorial(Z);
    
    
    logLike = log(CC)-log(DD)+(AA*log(BB))+(Z*log(1-BB));
end

sumValue = -sum(logLike);

end
