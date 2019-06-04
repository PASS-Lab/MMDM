% Compute transition probability for state i
% probability(j) =
% (gamma((1/alpha)+j)/(gamma(1/alpha)*j!))*((1/(1+(alpha*lambda))^(1/alpha))*(1-(1/(1+(alpha*lambda))))^j)
% where j is the drops of states

% need to change sheet number to obtain beta for each group
data = xlsread('Binomial_data.xlsx',6); %can you loop this through the number of sheets? You could determine the number with [STATUS,SHEETS] = xlsfinfo(FILENAME)
[nrows, ncols] = size(data);
X = data(:,1);
prob = zeros(nrows,4);

for i = 1:nrows
        lambda = exp(beta(1)*X(i));
       
        for j = 1:4
        AA = 1/beta(2);
        BB = 1/(1+(beta(2)*lambda));
        CC = gamma(AA+(j-1));
        DD = gamma(AA)*factorial(j-1);
        EE = BB^AA;
        FF = (1-BB)^(j-1);
        
        prob(i,j) = CC/DD*EE*FF;
        end
        
end

transProb4 = zeros(1,4);
for i = 1:4
    transProb4(1,i) = sum(prob(:,i))/nrows;
end
