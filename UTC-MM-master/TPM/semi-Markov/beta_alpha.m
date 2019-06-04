% Weibull distribution

%a = scale parameter; b = shape parameter
a = zeros(6,1);
b = zeros(6,1);

for i = 1:6
data = xlsread('semiMarkov_data.xlsx',i);
X = data(:,2);
parmhat = wblfit(X);
a(i) = parmhat(1);
b(i) = parmhat(2);


end
Scale = a(:);
Shape = b(:);

T = table(Scale,Shape)

