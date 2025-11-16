# DHK (2025) Replication - Module-Specific Instructions

This document provides detailed, technical instructions for implementing each module of the DHK replication.

---

## Module 1: Data Collection

### M1.1: Download FRED-MD Dataset

**File**: `data_processing/01_download_fredmd.R`

```r
# Download FRED-MD dataset (monthly, 1960-2021)
# Source: https://research.stlouisfed.org/econ/mccracken/fred-databases/

library(readxl)
library(dplyr)

# Option 1: Manual download
# 1. Visit https://files.stlouisfed.org/files/htdocs/fred-md/monthly/current.csv
# 2. Save to data/raw/

# Option 2: Automated download
download_fredmd <- function(save_path = "data/raw/fredmd_raw.csv") {
  url <- "https://files.stlouisfed.org/files/htdocs/fred-md/monthly/current.csv"
  download.file(url, save_path)
  return(read.csv(save_path))
}

# Read data
fredmd <- download_fredmd()

# Extract date range: 1960-01 to 2021-10
fredmd_subset <- fredmd %>%
  filter(date >= "1960-01-01" & date <= "2021-10-31")
```

**Variable Selection** (from Online Appendix B):

**30-Variable Model** (CCM baseline):
1. RPI - Real Personal Income
2. W875RX1 - Real personal income ex transfer receipts
3. INDPRO - IP Index
4. IPFPNSS - IP: Final Products and Nonindustrial Supplies
5. IPFINAL - IP: Final Products (Market Group)
6. IPCONGD - IP: Consumer Goods
7. IPDCONGD - IP: Durable Consumer Goods
8. IPNCONGD - IP: Nondurable Consumer Goods
9. IPBUSEQ - IP: Business Equipment
10. IPMAT - IP: Materials
11. IPDMAT - IP: Durable Materials
12. IPNMAT - IP: Nondurable Materials
13. IPMANSICS - IP: Manufacturing (SIC)
14. IPB51222s - IP: Residential Utilities
15. IPFUELS - IP: Fuels
16. CUMFNS - Capacity Utilization: Manufacturing
17. HWI - Help-Wanted Index for United States
18. HWIURATIO - Ratio of Help Wanted/No. Unemployed
19. CLF16OV - Civilian Labor Force
20. CE16OV - Civilian Employment
21. UNRATE - Unemployment Rate
22. UEMPMEAN - Average Duration of Unemployment (Weeks)
23. UEMPLT5 - Civilians Unemployed - Less Than 5 Weeks
24. UEMP5TO14 - Civilians Unemployed for 5-14 Weeks
25. UEMP15OV - Civilians Unemployed - 15 Weeks & Over
26. UEMP15T26 - Civilians Unemployed for 15-26 Weeks
27. UEMP27OV - Civilians Unemployed for 27 Weeks and Over
28. CLAIMSx - Initial Claims
29. PAYEMS - All Employees: Total nonfarm
30. USGOOD - All Employees: Goods-Producing Industries

**43-Variable Model** adds:
31-43: See Online Appendix B for complete list

---

### M1.2: Apply Transformations

**File**: `data_processing/02_transform_data.R`

```r
# Transformation codes (from FRED-MD documentation):
# 1 - No transformation
# 2 - First difference: x(t) - x(t-1)
# 3 - Second difference: (x(t) - x(t-1)) - (x(t-1) - x(t-2))
# 4 - Log: log(x)
# 5 - First difference of log: log(x(t)) - log(x(t-1))
# 6 - Second difference of log
# 7 - First difference of percent change

apply_transformation <- function(x, tcode) {
  if (tcode == 1) return(x)
  if (tcode == 2) return(c(NA, diff(x)))
  if (tcode == 4) return(log(x))
  if (tcode == 5) return(c(NA, diff(log(x))))
  # Add other transformation codes as needed
}

# Apply transformations to each variable
# Transformation codes are provided in FRED-MD dataset
```

---

### M1.3: Standardize Data

**File**: `data_processing/03_standardize_data.R`

```r
# Standardize each variable: zero mean, unit variance
# IMPORTANT: Save mean and SD for rescaling later

standardize_data <- function(X) {
  means <- colMeans(X, na.rm = TRUE)
  sds <- apply(X, 2, sd, na.rm = TRUE)

  X_std <- scale(X, center = means, scale = sds)

  # Save transformation parameters
  transform_params <- data.frame(
    variable = colnames(X),
    mean = means,
    sd = sds
  )

  return(list(
    data = X_std,
    params = transform_params
  ))
}
```

---

## Module 2: Model Specification

### M2.1: Core Model Structure

**File**: `model/svmvar_equations.R`

**Equation (1): VAR with SV in Mean**
```r
# yt = Σ(i=1 to p) Bi*yt-i + Σ(j=0 to q) Aj*ht-j + B0^(-1)*εt
# where εt ~ N(0, Ut)

# Create lagged matrices
create_lags <- function(y, p) {
  T <- nrow(y)
  n <- ncol(y)

  # Initialize lag matrix
  y_lags <- array(0, dim = c(T, n, p))

  for (i in 1:p) {
    y_lags[(i+1):T, , i] <- y[1:(T-i), ]
  }

  return(y_lags)
}

# VAR mean equation
compute_var_mean <- function(y, ht, B_coefs, A_coefs, p, q) {
  T <- nrow(y)
  n <- ncol(y)

  y_lags <- create_lags(y, p)
  h_lags <- create_lags(ht, q+1)  # q+1 for contemporaneous

  mu <- matrix(0, T, n)

  for (t in (p+1):T) {
    # VAR term
    for (i in 1:p) {
      mu[t, ] <- mu[t, ] + B_coefs[[i]] %*% y[t-i, ]
    }

    # SV in mean term
    for (j in 0:q) {
      if (t-j >= 1) {
        mu[t, ] <- mu[t, ] + A_coefs[[j+1]] %*% ht[t-j, ]
      }
    }
  }

  return(mu)
}
```

**Equation (2): Covariance Structure**
```r
# Ut = diag(Ωm,t, Ωu,t, Ωf,t)
# where Ωm,t = diag(exp(ωm_1,t), ..., exp(ωm_nm,t))

compute_covariance_matrix <- function(omega_m, omega_u, omega_f) {
  Omega_m <- diag(exp(omega_m))
  Omega_u <- diag(exp(omega_u))
  Omega_f <- diag(exp(omega_f))

  Ut <- as.matrix(Matrix::bdiag(Omega_m, Omega_u, Omega_f))
  return(Ut)
}
```

**Equations (3)-(5): Volatility Decomposition**
```r
# ωm_i,t = ηm_i,t + hm,t
# ωf_i,t = ηf_i,t + hf,t
# ωu_i,t = ηu_i,t + hs_i,t,t

decompose_volatility <- function(eta_m, eta_f, eta_u, h_m, h_f, class_indicators) {
  nm <- length(eta_m[1,])
  nf <- length(eta_f[1,])
  nu <- length(eta_u[1,])
  T <- nrow(h_m)

  # Macro volatilities
  omega_m <- matrix(0, T, nm)
  for (i in 1:nm) {
    omega_m[, i] <- eta_m[, i] + h_m
  }

  # Financial volatilities
  omega_f <- matrix(0, T, nf)
  for (i in 1:nf) {
    omega_f[, i] <- eta_f[, i] + h_f
  }

  # Unclassified volatilities (time-varying!)
  omega_u <- matrix(0, T, nu)
  for (i in 1:nu) {
    for (t in 1:T) {
      if (class_indicators[i, t] == "m") {
        omega_u[t, i] <- eta_u[t, i] + h_m[t]
      } else {
        omega_u[t, i] <- eta_u[t, i] + h_f[t]
      }
    }
  }

  return(list(omega_m = omega_m, omega_u = omega_u, omega_f = omega_f))
}
```

**Equation (6): Common Volatility Dynamics**
```r
# ht = Σ(i=1 to ph) Φi*ht-i + Σ(j=1 to py) Ψj*yt-j + εh
# where εh ~ N(0, Σh)

compute_h_mean <- function(ht, yt, Phi_coefs, Psi_coefs, ph, py) {
  T <- nrow(ht)

  h_lags <- create_lags(ht, ph)
  y_lags <- create_lags(yt, py)

  h_mean <- matrix(0, T, 2)  # 2 factors: macro and financial

  for (t in (max(ph, py)+1):T) {
    # Autoregressive term
    for (i in 1:ph) {
      h_mean[t, ] <- h_mean[t, ] + Phi_coefs[[i]] %*% ht[t-i, ]
    }

    # Link to observables
    for (j in 1:py) {
      h_mean[t, ] <- h_mean[t, ] + Psi_coefs[[j]] %*% yt[t-j, ]
    }
  }

  return(h_mean)
}
```

---

## Module 3: MCMC Algorithm

### M3.1: Sample B0 (Novel Order-Invariant Approach)

**File**: `mcmc/sample_B0.R`

This is the **key innovation** of the paper.

**Step 1: Parameter Transformation** (Equation 14)
```r
# Transform b̃0,1 to w via: w = d + Q*b̃0,1
# where Q = [-b'0,21 * B^(-1)0,22; 0_(n-2)×1, I_(n-2)]

transform_b_to_w <- function(b_tilde_01, B0_22, b0_21) {
  n <- length(b_tilde_01) + 1

  # Construct Q matrix
  Q_row1 <- -t(b0_21) %*% solve(B0_22)
  Q <- rbind(
    c(Q_row1, 0),
    cbind(matrix(0, n-2, 1), diag(n-2))
  )

  d <- c(1, rep(0, n-2))

  w <- d + Q %*% b_tilde_01

  return(list(w = w, Q = Q, d = d))
}
```

**Step 2: Sample w1 from Absolute Normal** (Proposition 1)
```r
# Sample from absolute normal distribution using mixture approximation

sample_absolute_normal <- function(a, b, n_components = 10) {
  # Use normal mixture approximation from Villani (2009), Appendix C
  # fAN(x; a, b) ∝ |x| * (1/b) * exp(-1/(2b) * (x-a)^2)

  # Mixture components
  # ... implement mixture approximation ...

  # For simplicity, use Metropolis-Hastings
  current_w1 <- rnorm(1, a, sqrt(b))

  # Target density (up to constant)
  log_target <- function(x) {
    log(abs(x)) - 1/(2*b) * (x - a)^2
  }

  # MH step
  proposal <- rnorm(1, current_w1, 0.1)
  log_alpha <- log_target(proposal) - log_target(current_w1)

  if (log(runif(1)) < log_alpha) {
    return(proposal)
  } else {
    return(current_w1)
  }
}
```

**Step 3: Sample w_{-1} from Conditional Gaussian** (Equation 18)
```r
# p(w_{-1} | w1, ...) is Gaussian

sample_w_minus1 <- function(w1, w_bar, K_inv, lambda_11, lambda_21) {
  # Mean: μw_{-1} = w̄_{-1} + (w1 - w̄1)/λ11 * λ21
  mu_w_minus1 <- w_bar[-1] + (w1 - w_bar[1])/lambda_11 * lambda_21

  # Covariance: Σw_{-1} = Λ̃22 - λ21*λ'21/λ11
  Sigma_w_minus1 <- K_inv[-1, -1] - lambda_21 %*% t(lambda_21) / lambda_11

  # Sample
  w_minus1 <- mvtnorm::rmvnorm(1, mu_w_minus1, Sigma_w_minus1)

  return(w_minus1)
}
```

**Step 4: Transform back to b̃0,1** (Equation 15)
```r
# b̃0,1 = Q^(-1)*w - Q^(-1)*d

transform_w_to_b <- function(w, Q, d) {
  Q_inv <- solve(Q)
  b_tilde_01 <- Q_inv %*% w - Q_inv %*% d
  return(b_tilde_01)
}
```

**Full B0 Sampler**
```r
sample_B0_row <- function(row_idx, B0_current, Omega_i, Y_tilde) {
  # 1. Extract current values
  # 2. Transform to w
  # 3. Sample w1 from absolute normal
  # 4. Sample w_{-1} from conditional Gaussian
  # 5. Transform back to b̃0,i
  # 6. Update B0

  # ... implement full procedure ...
}

sample_B0 <- function(B0_current, Omega, Y_tilde) {
  n <- nrow(B0_current)
  B0_new <- B0_current

  # Sample each row sequentially
  for (i in 1:n) {
    B0_new[i, ] <- sample_B0_row(i, B0_new, Omega[[i]], Y_tilde)
  }

  return(B0_new)
}
```

---

### M3.2: Sample Log-Volatilities (CHKP Algorithm)

**File**: `mcmc/sample_volatilities.R`

**Reference**: Cross et al. (2023) - Large Stochastic Volatility in Mean VARs

```r
# This uses band and sparse matrix algorithms
# Key insight: Hessian of log-posterior is block-banded

sample_volatilities_chkp <- function(y, h_current, B0, A_coefs, Sigma_h) {
  T <- nrow(y)

  # 1. Compute conditional posterior mode
  # ... use Newton-Raphson on band system ...

  # 2. Compute Hessian (block-banded structure!)
  H <- compute_hessian_banded(y, h_current, B0, A_coefs)

  # 3. Generate proposal using Hessian as variance
  # Use band/sparse matrix solver for efficiency
  library(spam)  # Sparse matrix package

  h_proposal <- rmvnorm.canonical(1, b = h_mode, Q = H)

  # 4. Acceptance-Rejection step
  log_alpha <- compute_log_acceptance_prob(h_proposal, h_current, ...)

  if (log(runif(1)) < log_alpha) {
    return(h_proposal)
  } else {
    return(h_current)
  }
}
```

**Note**: This is computationally intensive. Must use sparse/band matrix algorithms.

---

### M3.3: Sample Classification Indicators

**File**: `mcmc/sample_classification.R`

**Reference**: Chib (1996)

```r
# Sample si,t ∈ {m, f} for each unclassified variable
# Uses forward-filtering backward-sampling

sample_classification_single_var <- function(i, h_m, h_f, eta_u_i, trans_prob) {
  T <- length(h_m)

  # Forward filtering (compute filtered probabilities)
  filtered_prob <- matrix(0, T, 2)  # P(si,t = m | y1:t)

  for (t in 1:T) {
    # Likelihood: depends on how well hm vs hf explains omega_u_i,t
    like_m <- dnorm(omega_u_i[t], eta_u_i[t] + h_m[t], sigma_u_i)
    like_f <- dnorm(omega_u_i[t], eta_u_i[t] + h_f[t], sigma_u_i)

    if (t == 1) {
      # Initial probabilities
      filtered_prob[t, 1] <- like_m * 0.5
      filtered_prob[t, 2] <- like_f * 0.5
    } else {
      # Update using Markov transition
      pred_prob_m <- trans_prob["m", "m"] * filtered_prob[t-1, 1] +
                     trans_prob["f", "m"] * filtered_prob[t-1, 2]
      pred_prob_f <- trans_prob["m", "f"] * filtered_prob[t-1, 1] +
                     trans_prob["f", "f"] * filtered_prob[t-1, 2]

      filtered_prob[t, 1] <- like_m * pred_prob_m
      filtered_prob[t, 2] <- like_f * pred_prob_f
    }

    # Normalize
    filtered_prob[t, ] <- filtered_prob[t, ] / sum(filtered_prob[t, ])
  }

  # Backward sampling
  s_draws <- rep(0, T)

  # Draw sT
  s_draws[T] <- sample(c("m", "f"), 1, prob = filtered_prob[T, ])

  # Draw st | st+1, y1:T for t = T-1, ..., 1
  for (t in (T-1):1) {
    # P(st | st+1, y1:T) ∝ P(st | y1:t) * P(st+1 | st)
    prob_m <- filtered_prob[t, 1] * trans_prob["m", s_draws[t+1]]
    prob_f <- filtered_prob[t, 2] * trans_prob["f", s_draws[t+1]]

    s_draws[t] <- sample(c("m", "f"), 1, prob = c(prob_m, prob_f))
  }

  return(s_draws)
}
```

---

### M3.7: Main MCMC Loop

**File**: `mcmc/mcmc_main.R`

```r
run_mcmc_oi_svmvar <- function(data, model_spec, mcmc_spec) {
  # Extract specifications
  y <- data$y
  n <- ncol(y)
  T <- nrow(y)
  p <- model_spec$p
  q <- model_spec$q

  M <- mcmc_spec$n_iter
  burn <- mcmc_spec$burn_in
  thin <- mcmc_spec$thin

  # Initialize parameters
  params <- initialize_parameters(y, model_spec)

  # Storage for draws
  draws <- initialize_storage(M, n, T, model_spec)

  # MCMC loop
  pb <- txtProgressBar(min = 0, max = M, style = 3)

  for (m in 1:M) {
    # Step 1: Sample B0 (order-invariant)
    params$B0 <- sample_B0(params$B0, params$Omega, y, ...)

    # Step 2: Sample classification indicators (if unclassified variables)
    if (model_spec$nu > 0) {
      params$class_ind <- sample_classification(
        params$h_m, params$h_f, params$eta_u, params$trans_prob
      )
    }

    # Step 3: Transform model based on classification
    # (Reorder unclassified variables to group with appropriate block)
    y_transformed <- transform_by_classification(y, params$class_ind, model_spec)

    # Step 4: Sample log-volatilities (CHKP algorithm)
    params$h <- sample_volatilities_chkp(
      y_transformed, params$h, params$B0, params$A_coefs, params$Sigma_h
    )

    # Step 5: Sample VAR coefficients
    params$B_coefs <- sample_var_coefs(y, params$h, params$B0, ...)
    params$A_coefs <- sample_volatility_in_mean_coefs(y, params$h, ...)

    # Step 6: Sample volatility dynamics
    params$Phi <- sample_h_var_coefs(params$h, ...)
    params$Psi <- sample_h_y_coefs(params$h, y, ...)
    params$Sigma_h <- sample_h_covariance(params$h, params$Phi, params$Psi, ...)

    # Step 7: Sample idiosyncratic volatilities
    params$eta_params <- sample_idiosyncratic(
      params$omega, params$h, params$class_ind, ...
    )

    # Step 8: Sample Markov transition probabilities (if time-varying classification)
    if (model_spec$nu > 0) {
      params$trans_prob <- sample_transition_probs(params$class_ind, ...)
    }

    # Save draws (after burn-in, with thinning)
    if (m > burn && (m - burn) %% thin == 0) {
      idx <- (m - burn) / thin
      draws <- save_draws(draws, params, idx)
    }

    # Update progress
    setTxtProgressBar(pb, m)

    # Print diagnostics every 100 iterations
    if (m %% 100 == 0) {
      cat(sprintf("\nIteration %d: B0 acceptance = %.2f, h acceptance = %.2f\n",
                  m, acceptance_rate_B0, acceptance_rate_h))
    }
  }

  close(pb)

  # Compute posterior summaries
  posterior <- compute_posterior_summaries(draws)

  # Convergence diagnostics
  diagnostics <- compute_diagnostics(draws)

  return(list(
    draws = draws,
    posterior = posterior,
    diagnostics = diagnostics,
    acceptance_rates = list(B0 = acceptance_rate_B0, h = acceptance_rate_h)
  ))
}
```

---

## Module 4: Simulation Study

### M4.1: Generate Synthetic Data

**File**: `simulation/01_generate_data.R`

```r
generate_simulation_data <- function() {
  # Set up DGP parameters (Section 3.1)
  nm <- 10  # macro variables
  nf <- 10  # financial variables
  nu <- 3   # unclassified variables
  n <- nm + nf + nu
  T <- 600
  p <- 2    # VAR lags
  q <- 1    # Volatility-in-mean lags

  # Generate B0 (full nonzero matrix)
  B0 <- diag(n)
  for (i in 1:n) {
    for (j in 1:n) {
      if (i != j) {
        B0[i, j] <- rnorm(1, 0, 0.2)
      }
    }
  }

  # Generate B1
  B1 <- matrix(0, n, n)
  for (i in 1:n) {
    B1[i, i] <- runif(1, 0, 0.6)
    for (j in 1:n) {
      if (i != j) {
        B1[i, j] <- runif(1, -0.2, 0.2)
      }
    }
  }

  # Generate B2, ..., Bp
  B2 <- matrix(rnorm(n*n, 0, 0.12/4), n, n)

  # Generate A0, A1
  A0 <- matrix(rnorm(n*2, 0, 0.52), n, 2)
  A1 <- matrix(rnorm(n*2, 0, 0.52/4), n, 2)

  # Generate Phi, Psi
  Phi <- diag(2) * 0.95
  Sigma_h <- diag(2) * 0.05

  # Set classification
  class_ind <- matrix("", nu, T)
  class_ind[1, ] <- "m"  # Always macro
  class_ind[3, ] <- "f"  # Always financial
  class_ind[2, 1:200] <- "f"
  class_ind[2, 201:400] <- "m"
  class_ind[2, 401:600] <- "f"

  # Simulate data
  h <- matrix(0, T, 2)
  y <- matrix(0, T, n)

  for (t in 3:T) {
    # Generate ht
    h[t, ] <- Phi %*% h[t-1, ] + mvtnorm::rmvnorm(1, rep(0, 2), Sigma_h)

    # Generate yt
    mu_t <- B1 %*% y[t-1, ] + B2 %*% y[t-2, ] + A0 %*% h[t, ] + A1 %*% h[t-1, ]

    # Construct Ut based on classification
    omega_m <- h[t, 1]
    omega_f <- h[t, 2]

    Omega <- rep(0, n)
    Omega[1:nm] <- exp(omega_m)
    for (i in 1:nu) {
      if (class_ind[i, t] == "m") {
        Omega[nm + i] <- exp(omega_m)
      } else {
        Omega[nm + i] <- exp(omega_f)
      }
    }
    Omega[(nm+nu+1):n] <- exp(omega_f)

    Ut <- diag(Omega)

    epsilon_t <- mvtnorm::rmvnorm(1, rep(0, n), Ut)
    y[t, ] <- mu_t + solve(B0) %*% t(epsilon_t)
  }

  # Return
  return(list(
    y = y,
    h = h,
    B0 = B0,
    B1 = B1,
    B2 = B2,
    A0 = A0,
    A1 = A1,
    Phi = Phi,
    Sigma_h = Sigma_h,
    class_ind = class_ind,
    true_params = list(...)  # Save all true parameters
  ))
}
```

---

## Module 6: Analysis Tools

### M6.1: Impulse Response Functions

**File**: `analysis/01_compute_irfs.R`

```r
compute_irfs <- function(posterior_draws, model_spec, irf_spec) {
  # Extract specifications
  horizons <- irf_spec$horizons  # e.g., 0:48 months
  shock_size <- irf_spec$shock_size  # e.g., 1 SD
  shock_type <- irf_spec$shock_type  # "macro" or "financial"

  n_draws <- dim(posterior_draws$B_coefs)[1]
  n_vars <- model_spec$n
  n_horizons <- length(horizons)

  # Storage
  irfs <- array(0, dim = c(n_draws, n_vars, n_horizons))

  for (d in 1:n_draws) {
    # Extract draw
    B0 <- posterior_draws$B0[d, , ]
    B_coefs <- posterior_draws$B_coefs[d, , , ]
    A_coefs <- posterior_draws$A_coefs[d, , , ]
    Phi <- posterior_draws$Phi[d, , ]
    Sigma_h <- posterior_draws$Sigma_h[d, , ]

    # Identify structural uncertainty shocks
    # L is lower triangular: LL' = Sigma_h
    L <- t(chol(Sigma_h))

    # Initial shock
    if (shock_type == "macro") {
      eps_h <- c(shock_size, 0)
    } else {
      eps_h <- c(0, shock_size)
    }

    # Structural shock
    eh <- solve(L) %*% eps_h

    # Simulate impulse response
    h_path <- matrix(0, n_horizons, 2)
    y_path <- matrix(0, n_horizons, n_vars)

    h_path[1, ] <- eh  # Initial shock

    for (h in 2:n_horizons) {
      # Propagate through h dynamics
      h_path[h, ] <- Phi %*% h_path[h-1, ]

      # Effect on y through volatility-in-mean
      for (j in 0:min(q, h-1)) {
        y_path[h, ] <- y_path[h, ] + A_coefs[, , j+1] %*% h_path[h-j, ]
      }

      # VAR propagation
      for (i in 1:min(p, h-1)) {
        y_path[h, ] <- y_path[h, ] + B_coefs[, , i] %*% y_path[h-i, ]
      }
    }

    # Cumulate if needed (for variables in levels)
    y_path_cumul <- apply(y_path, 2, cumsum)

    irfs[d, , ] <- y_path_cumul
  }

  # Compute posterior summaries
  irf_median <- apply(irfs, c(2, 3), median)
  irf_lower <- apply(irfs, c(2, 3), quantile, probs = 0.15)
  irf_upper <- apply(irfs, c(2, 3), quantile, probs = 0.85)

  return(list(
    irfs = irfs,
    median = irf_median,
    lower = irf_lower,
    upper = irf_upper
  ))
}
```

---

## Programming Best Practices

### Code Organization
```
# Each file should have:
# 1. Header with description
# 2. Dependencies
# 3. Functions
# 4. Example usage (commented out)

##############################################
# File: sample_B0.R
# Purpose: Sample B0 using order-invariant algorithm
# Reference: DHK (2025), Section 2.2
# Author: [Name]
# Date: 2025-11-16
##############################################

# Dependencies
library(Matrix)
library(mvtnorm)

# Main function
sample_B0 <- function(...) {
  # ... implementation ...
}

# Example usage (for testing)
# if (FALSE) {
#   # Test code here
# }
```

### Testing
```r
# Create test file for each module
# tests/test_sample_B0.R

test_sample_B0 <- function() {
  # Test 1: Check dimensions
  # Test 2: Check B0 has diagonal = 1
  # Test 3: Compare with known solution

  cat("All tests passed!\n")
}
```

### Documentation
```r
#' Sample B0 matrix using order-invariant algorithm
#'
#' @param B0_current Current value of B0 (n x n matrix)
#' @param Omega List of variance matrices
#' @param Y_tilde Transformed data matrix
#' @return Updated B0 matrix (n x n)
#' @references Davidson, Hou, Koop (2025), Section 2.2
#' @examples
#' B0_new <- sample_B0(B0_current, Omega, Y_tilde)
sample_B0 <- function(B0_current, Omega, Y_tilde) {
  # ... implementation ...
}
```

---

## Computational Optimization Tips

1. **Use sparse/band matrices**:
```r
library(spam)  # Sparse matrix package
H_sparse <- as.spam(H)  # Convert to sparse
x <- solve.spam(H_sparse, b)  # Much faster than solve(H, b)
```

2. **Vectorize operations**:
```r
# Bad (slow)
for (i in 1:n) {
  for (j in 1:T) {
    result[i, j] <- f(x[i], y[j])
  }
}

# Good (fast)
result <- outer(x, y, f)
```

3. **Pre-allocate memory**:
```r
# Bad
result <- c()
for (i in 1:n) {
  result <- c(result, f(i))
}

# Good
result <- numeric(n)
for (i in 1:n) {
  result[i] <- f(i)
}
```

4. **Profile your code**:
```r
Rprof("profile.out")
# Run your code
Rprof(NULL)
summaryRprof("profile.out")
```

---

## Debugging Strategies

1. **Start simple**: Test on 6-variable model first
2. **Use known solutions**: Test MCMC on data with known parameters
3. **Check one step at a time**: Isolate each MCMC step
4. **Monitor diagnostics**: Track acceptance rates, parameter paths
5. **Compare with paper**: Check if uncertainty estimates look reasonable

---

## Next Steps

1. ✅ Review this document
2. ⬜ Choose programming language (R recommended)
3. ⬜ Set up development environment
4. ⬜ Start with M1 (Data collection)
5. ⬜ Implement M2.1 (Model equations) - test on toy example
6. ⬜ Implement M3.1 (Sample B0) - test in isolation
7. ⬜ Continue with remaining modules

For questions or clarifications, refer to:
- Main plan: `llm_logs/2025-11-16_DHK_replication_plan.md`
- Original paper: `references/Investigating Economic Uncertain.pdf`
- Online Appendix: Check journal website
