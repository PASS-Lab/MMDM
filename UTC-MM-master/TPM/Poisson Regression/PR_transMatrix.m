% Compute transition probability for state i

% need to change sheet number to obtain beta for each group
data = xlsread('Poisson_data.xlsx',5);
[nrows, ncols] = size(data);
X = data(:,1);

prob = zeros(nrows,4);
lambdaPower = zeros(nrows,1);
lambda = zeros(nrows,1);

for i = 1:nrows
        lambda(i) = exp(beta*X(i));
        
        for j = 1:4
        lambdaPower(i) = lambda(i)^(j-1);
        prob(i,j) = (exp(-lambda(i))*lambdaPower(i))/factorial(j-1);
        end
        
end

transProb5 = zeros(1,4);
for i = 1:4
    transProb5(1,i) = sum(prob(:,i))/nrows;
end
