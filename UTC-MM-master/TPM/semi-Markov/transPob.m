% Probability Matrices



data = xlsread('tranProb_data.xlsx',1);

p99 = data(:,2);p98 = data(:,7);p97 = data(:,12);
p88 = data(:,3);p87 = data(:,8);p86 = data(:,13);
p77 = data(:,4);p76 = data(:,9);p75 = data(:,14);
p66 = data(:,5);p65 = data(:,10);p64 = data(:,15);
p55 = data(:,6);p54 = data(:,11);
p44 = 1; % this is obtained from the process done by Excel

% time, t = 1 year to 20 years
t = 20; 
P = zeros(7,7,t);

% Generate probability matrices
for i = 1:t
    P(:,:,i) = [p99(i) p98(i) p97(i) 0 0 0 0;
            0 p88(i) p87(i) p86(i) 0 0 0;
            0 0 p77(i) p76(i) p75(i) 0 0;
            0 0 0 p66(i) p65(i) p64(i) 0;
            0 0 0 0 p55(i) p54(i) 0;
            0 0 0 0 0 p44 0;
            0 0 0 0 0 0 1];
end