% run_2019_svar_estimation.m
clear; clc;
ext_dir = '/Volumes/X9 Pro/2 Research Projects/Uncertainty and Financial Friction/Crown replication code/insample';
cd(ext_dir);

% 1. Load the most recent data
load('chp21.mat');

% 2. Truncate data to 2019:Q4 (approx. index 244)
chp20 = output(62:244, 1:end);    

Datar = [chp20(:, 1:2), chp20(:, end), chp20(:, 3:17), chp20(:, end-1), ...
    chp20(:, 18:20)];
Datar = Datar(1:end,:); 

% standardized data
Data = (Datar - repmat(mean(Datar),size(Datar,1),1))./repmat(std(Datar), size(Datar,1),1);

%% MCMC setup
nsmcmc = 25000;
burnin = 5000;
skip = 1;
p = 4;                                  % order of VAR
q = 2;                                  % order of SV in mean (q + 1)

%% construct X Y 
g      = 3;
Y      = Data(p+1:end,:);
Yhlag  = Data(p:end-1,:);
longY  = reshape(Y',[],1);
[T,ng] = size(Y);
kb     = ng*p + 1;
ka     = g*(q+1);
k      = kb + ka;
kgam   = ng*(ng - 1)/2;
ph     = 2;
X      = zeros(T,kb-1);
for ii = 1:p
    X(:, (ii-1)*ng + 1 : ii*ng) = Data(p - ii + 1 : end-ii, :); 
end
X = [ones(T,1) X];

% Classification (CRITICAL FIX: Ensure T is defined correctly)
bigs = repmat([ones(1,14) 2 3*ones(1,7)],T,1);

%% The rest is the core SVMVAR logic
script_text = fileread('SVMVAR_AddingHousingPrice.m');
start_marker = '%% construct BigW';
start_idx = strfind(script_text, start_marker);
end_idx = strfind(script_text, 'save(''est_result.mat'')');

if isempty(start_idx) || isempty(end_idx)
    error('Could not find MCMC loop markers in SVMVAR_AddingHousingPrice.m');
end

core_logic = script_text(start_idx:end_idx-1);

fprintf('Starting MCMC for 2019 sample at %s...\n', datestr(now));
eval(core_logic);

% 3. Save as the 2019 specific result
out_file = '/Users/linshih-yang/Documents/GitHub/Caught-in-the-Crossfire/code/empirical_bca_us/data/est_result_2019.mat';
save(out_file);

disp(['MCMC Estimation for 2019 sample finished successfully at ', datestr(now)]);
exit;
