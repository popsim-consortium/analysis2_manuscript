import numpy as np
import scipy.stats.distributions as ssd

# From https://github.com/popsim-consortium/stdpopsim/blob/main/stdpopsim/catalog/PhoSin/dfes.py
gamma_shape = 0.131
gamma_mean = -0.0257
dominance_coeff_list=[0.0, 0.01, 0.1, 0.4]
dominance_coeff_breaks=[-0.1, -0.01, -0.001]

# Construct the corresponding gamma distribution
gamma_scale = -gamma_mean / gamma_shape
dfe = ssd.gamma(gamma_shape, scale=gamma_scale)
assert(dfe.mean() == abs(gamma_mean))

# Simulate draws from the DFE
N = 100000
s_array = -dfe.rvs(N)

# Sanity check, using method of moments to recover simulated shape and scale.
# (Fixing location parameter to zero.)
# mean = shape * scale, var = shape * scale**2
# So scale = var/mean, and shape = mean/scale
fit_s_scale = s_array.var()/s_array.mean()
fit_s_shape = s_array.mean()/fit_s_scale
# Or just use fit_s_shape, _, fit_s_scale = ssd.gamma.fit(s_array, method='MM', floc=0) 
print('Sanity check: Inferred s shape and mean: {0:.4f}, {1:.5f}'.format(fit_s_shape, fit_s_shape*fit_s_scale))

# Convert to 2*hs
breaks = [-np.inf] + list(dominance_coeff_breaks) + [0]
hs_arrays = []
for h, s_start, s_end in zip(dominance_coeff_list, breaks[:-1], breaks[1:]):
    hs_arrays.append(2*h*s_array[np.logical_and(s_start < s_array, s_array < s_end)])
hs_array = np.concatenate(hs_arrays)

# Calculate mean hs
mean_hs = hs_array.mean()
print('Simulated mean 2hs: {0:.6f}'.format(mean_hs))

#fit_hs_shape, _, fit_hs_scale = ssd.gamma.fit(hs_array, method='MM', floc=0)
#dfe_hs = ssd.gamma(fit_hs_shape, scale=-fit_hs_scale)
#
#print('Inferred 2hs shape and mean: {0:.4f}, {1:.5f}'.format(fit_hs_shape, fit_hs_shape*fit_hs_scale))

# Results from inferences
dfe_dadi= ssd.gamma(0.33, scale=0.002)
dfe_polydfe = ssd.gamma(0.33, scale=0.002)
dfe_grapes = ssd.gamma(0.35, scale=0.0035)

# Plotting
import matplotlib.pyplot as plt
plt.rc('font', size=10)

fig = plt.figure(2132, figsize=(3.5,2.5))
fig.clear()
ax = fig.add_subplot(1,1,1)
# Histogram of 2*hs, scaled by 10^3
ax.hist(hs_array*1e3, bins=101, density=True, label='Simulated 2hs distribution')
# DFE inferred for 2hs
xx = np.linspace(-2.2, 0, 1001)
ax.plot(xx, dfe.pdf(-xx/1e3)/1e3, '-k', label='Original s DFE')
ax.plot(xx, dfe_dadi.pdf(-xx/1e3)/1e3, '-', label='Inferred DFE (GRAPES)')
ax.plot(xx, dfe_polydfe.pdf(-xx/1e3)/1e3, '-', label='Inferred DFE (polyDFE)')
ax.plot(xx, dfe_grapes.pdf(-xx/1e3)/1e3, '-', label='Inferred DFE (dadi)')
ax.set_xlabel(r'$2hs\,\,(\times 10^{-3})$')
ax.set_ylabel('Probability density')
ax.legend(loc='upper left')
ax.set_ylim(0, 2)
ax.set_xlim(-2.2,0)
fig.tight_layout(pad=0)
fig.savefig('hs_hist.pdf')
