# Cliquet

::: qablet_contracts.eq.cliquet

In an **Accumulator** the payoff depends on the asset price on
several fixing dates $T_0 < T_1 < ... T_N$.

If the returns are given by

$$
r_i = \frac{S_{T_{i+1}}-S_{T_i}}{S_{T_i}}
$$

Then contract has a single payoff at $T_N$, given by

$$
\max \left( floor_G, \Sigma_0^{N-1} \max(\min(r_i, cap_L), floor_L) \right)
$$

