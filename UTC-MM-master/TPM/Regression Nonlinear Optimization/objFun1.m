% object function of Gruop1 (0-6 years old bridges)
% S(t) = 9-9+0.01151*t^3-0.02598*t^2+-0.5213*t;

function sumValue = objFun1(p)
P = [p(1) 1-p(1) 0 0 0 0 0;
    0 p(2) 1-p(2) 0 0 0 0;
    0 0 p(3) 1-p(3) 0 0 0;
    0 0 0 p(4) 1-p(4) 0 0;
    0 0 0 0 p(5) 1-p(5) 0;
    0 0 0 0 0 p(6) 1-p(6);
    0 0 0 0 0 0 1];
t_all = [];
i_all = [];
S = zeros(6,1);
ExpValue = zeros(6,1);
diffValue = zeros(6,1);
P_initial = [1 0 0 0 0 0 0];
CR = [9 8 7 6 5 4 3];

for i=1:6
    t=P^i;
    t_all = [t_all t(:)];
    i_all = [i_all  ones(size(t_all,1),1)*i];
    ExpValue(i) = P_initial*t*CR';
    S(i) = 9+0.01151*i^3-0.02598*i^2+-0.5213*i;
    diffValue(i)= abs(S(i)-ExpValue(i));
end  

sumValue = sum(diffValue);
