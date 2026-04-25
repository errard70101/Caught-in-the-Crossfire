% Consolidated sanity checks for the preliminary FVGQ output folder.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

fail_count = 0;

WU = readtable(fullfile(output_dir, 'warmup_diagnostics.csv'));
tail_diff = WU.value(strcmp(WU.name, 'sss_tail_diff_norm'));
if tail_diff > 1e-6
    fprintf('[FAIL] SSS tail-diff norm %.3e exceeds 1e-6\n', tail_diff);
    fail_count = fail_count + 1;
else
    fprintf('[PASS] SSS tail-diff norm %.3e\n', tail_diff);
end

T1 = readtable(fullfile(output_dir, 'experiment1_sample.csv'));
resid1 = T1.y - T1.cspt - 0.06 * T1.ivst;
if max(abs(resid1)) > 1e-6
    fprintf('[FAIL] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
end

S = load(fullfile(output_dir, 'experiment2_paths.mat'));
expected_shape = [S.N, S.H, numel(S.var_names)];
for tag = {'fin', 'macro'}
    pb = S.(['paths_base_' tag{1}]);
    ps = S.(['paths_shock_' tag{1}]);
    if ~isequal(size(pb), expected_shape) || ~isequal(size(ps), expected_shape)
        fprintf('[FAIL] Exp2 (%s) shape mismatch: got %s and %s, expected %s\n', ...
                tag{1}, mat2str(size(pb)), mat2str(size(ps)), mat2str(expected_shape));
        fail_count = fail_count + 1;
    else
        diff_max = max(abs(squeeze(ps(1, 1, :) - pb(1, 1, :))));
        if diff_max < 1e-8
            fprintf('[FAIL] Exp2 (%s) no shock propagation at h=1 (diff=%.3e)\n', ...
                    tag{1}, diff_max);
            fail_count = fail_count + 1;
        else
            fprintf('[PASS] Exp2 (%s) shape OK, h=1 diff %.3e\n', tag{1}, diff_max);
        end
    end
end

W = readtable(fullfile(output_dir, 'wedges_exp1.csv'));
if max(abs(W.G_share)) > 1e-6
    fprintf('[FAIL] Wedge G_share max |.| = %.3e\n', max(abs(W.G_share)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Wedge G_share max |.| = %.3e\n', max(abs(W.G_share)));
end

if fail_count > 0
    error('sanity_checks:%d_failures', '%d check(s) failed.', fail_count);
else
    fprintf('\nAll 5 sanity checks passed.\n');
end
