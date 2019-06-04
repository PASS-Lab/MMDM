% object function of BML

function sumValue = objFun(p)

% consider probability of transition to only next state 

p98 = p(1);
p99 = 1-p(1);
p87 = p(2);
p88 = 1-p(2);
p76 = p(3);
p77 = 1-p(3);
p65 = p(4);
p66 = 1-p(4);
p54 = p(5);
p55 = 1-p(5);
p43 = p(6);
p44 = 1-p(6);

P = [p99 p98 0 0 0 0 0;
    0 p88 p87 0 0 0 0;
    0 0 p77 p76 0 0 0;
    0 0 0 p66 p65 0 0;
    0 0 0 0 p55 p54 0;
    0 0 0 0 0 p44 p43;
    0 0 0 0 0 0 1];

t_all = [];
i_all = [];

data = xlsread('BML_data.xlsx',1);

logLike = zeros(60,1);

P_initial = [1 0 0 0 0 0 0];

for i=1:60
    t=P^i;
    t_all = [t_all t(:)];
    i_all = [i_all  ones(size(t_all,1),1)*i];
    NumValue = data(i,:);
    pValue = P_initial*t;
    logValue = log(pValue);
    
    % check log values
    logValue(logValue==-Inf)=0;
    
    logLike(i) = logValue * NumValue'; 

end

sumValue = -sum(logLike);
end
