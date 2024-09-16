# Hearing aid gain adjustment  Monte Carlo simulation

## Overview
Python script for simulating how users adjust hearing aid gain to reach their preferred gain settings. The simulation models the adjustments users make over time, starting from an initial reference gain. Monte Carlo simulations introduce variability in user preferences and adjustment patterns to study the overall distribution and trends in user gain adjustments. User preferences for gain are modelled using a log-normal distribution to reflect the skewed nature of real-world preferences. Most users tend to prefer lower gains (e.g., around 20 dB, corresponding to mild hearing loss), with a few users requiring higher gains.

## Features
- **Simulated adjustments**: Models user self-adjustments of hearing aid gain over multiple sessions.
- **Monte Carlo simulation**: Simulates multiple user trials with varied preferences, enabling an understanding of how different users adjust their gain.
- **Adjustable parameters**: Customise the number of adjustments, the mean adjustment size, and variability in both user adjustments and preferred gain settings.
- **Visualisation**: Plots the mean and confidence intervals for gain adjustments, as well as changes from preferred gain over time.

<img src="./monte_carlo_preferred_gains_log_normal.png" alt="Simulation Plot" width="400"/>

<img src="./monte_carlo_gain_adjustment_plot.png" alt="Simulation Plot" width="400"/>
