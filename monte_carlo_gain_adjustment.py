########################################################################################################################################################################
# Monte Carlo Simulation of Hearing Aid Gain Adjustments Towards Preferred Gain (Log-Normal Distribution)
# 
# Simulates how users self-adjust hearing aid gain towards their preferred gain. 
# The experiment starts at an initial gain setting and models multiple adjustment sessions (e.g., over days or trials). 
# Monte Carlo simulations introduce variability in user behaviour through varied preferred gain settings and adjustment steps. 
# 
# Preferred gains are modelled using a log-normal distribution (reflecting a skewed distribution towards milder hearing loss). 
# Adjustments made during simulations are modelled using a normal distribution.
# The mean adjustment is halved after half of the trials.
########################################################################################################################################################################

import numpy as np
import matplotlib.pyplot as plt

########################################################################################################################################################################
# Function to simulate hearing aid gain adjustments over sessions
########################################################################################################################################################################
def simulate_gain_adjustment(initial_gain, preferred_gain, num_adjustments, mean_adjustment, adjustment_sd):
    """
    Simulate user adjustments to hearing aid gain over time to approach their preferred gain.
    
    Parameters:
    initial_gain (float): Initial gain setting of the hearing aid (e.g., 0 to 100 scale)
    preferred_gain (float): The user-defined preferred gain setting
    num_adjustments (int): Number of adjustment attempts (e.g., over days or sessions)
    mean_adjustment (float): Mean adjustment per session
    adjustment_sd (float): Variability in each adjustment
    
    Returns:
    np.array: Simulated gain adjustments over the sessions
    """
    # Array to store gain settings over time
    gain_values = np.zeros(num_adjustments)
    gain_values[0] = initial_gain
    
    for i in range(1, num_adjustments):
        # Reduce the mean adjustment after a certain number of adjustments (e.g., after 6 adjustments)
        if i > round(num_adjustments*0.5):
            mean_adjustment = mean_adjustment * 0.5  # Reduce the adjustment size by half
        else:
            mean_adjustment = mean_adjustment

        # Simulation of adjustments to gain
        # Generate a random adjustment based on normal distribution
        adjustment = np.random.normal(mean_adjustment, adjustment_sd)
        
        # Determines direction of adjustment
        direction = 1 if preferred_gain > gain_values[i-1] else -1
        # Gain adjustment towards prefered gain
        gain_values[i] = gain_values[i-1] + direction * adjustment
        
        # Limit gain to a safe and practical range
        gain_values[i] = np.clip(gain_values[i], 0, 80)
    
    return gain_values

########################################################################################################################################################################
# Monte Carlo simulation for gain adjustments with skewed preferred gain (log-normal distribution)
########################################################################################################################################################################
def monte_carlo_simulation_preferred_gain(num_simulations, initial_gain, preferred_gain_mean, preferred_gain_sd, num_adjustments, mean_adjustment, adjustment_sd):
    """
    Perform Monte Carlo simulation for user gain adjustments with skewed preferred gain settings (log-normal distribution).
    
    Parameters:
    num_simulations (int): Number of simulations to run
    initial_gain (float): Initial gain setting
    preferred_gain_mean (float): Mean preferred gain setting (for the log-normal distribution)
    preferred_gain_sd (float): Standard deviation of preferred gain (for the log-normal distribution)
    num_adjustments (int): Number of adjustments
    mean_adjustment (float): Mean adjustment per session
    adjustment_sd (float): Standard deviation of adjustment
    
    Returns:
    np.array: A 2D array where each row is a simulation result over the adjustments
    np.array: A 1D array of the preferred gains for each simulation
    """
    # Generate skewed preferred gains using a log-normal distribution
    preferred_gains = np.random.lognormal(mean=np.log(preferred_gain_mean), sigma=preferred_gain_sd, size=num_simulations)
    
    # Clip the preferred gains to be within a practical range
    preferred_gains = np.clip(preferred_gains, 5, 50)
    
    # Array to store all simulation results
    all_simulations = np.zeros((num_simulations, num_adjustments))
    
    for i in range(num_simulations):
        # Run the gain adjustment simulation for each trial with a unique preferred gain
        all_simulations[i] = simulate_gain_adjustment(initial_gain, preferred_gains[i], num_adjustments, mean_adjustment, adjustment_sd)
    
    return all_simulations, preferred_gains

########################################################################################################################################################################
# Set simulation parameters
########################################################################################################################################################################
initial_gain = 0  # Initial gain setting
preferred_gain_mean = 20  # Mean for skewed distribution (closer to 20 dB, reflecting mild hearing loss)
preferred_gain_sd = 0.3  # Standard deviation for skewed distribution (controls tail length)

num_adjustments = 14  # Number of self-adjustments (e.g., over trials/sessions)
mean_adjustment = 4  # Mean starting gain adjustment
adjustment_sd = 1  # Variability in adjustment
num_simulations = 1000  # Number of simulations

# Run the Monte Carlo simulation with skewed preferred gains
# simulated_gain_adjustments: A 2D array where each row represents the gain adjustments for one simulation (i.e., one user) across multiple sessions.
# preferred_gains: A 1D array of preferred gains for each simulation (user), drawn from a log-normal distribution.
gains, preferred_gains = monte_carlo_simulation_preferred_gain(num_simulations, initial_gain, preferred_gain_mean, preferred_gain_sd, num_adjustments, mean_adjustment, adjustment_sd)

########################################################################################################################################################################
# Calculate adjustments, means, delta gains
########################################################################################################################################################################
# Calculate individual gain adjustments (trial differences)
gain_adjustments = np.diff(gains, axis=1)
# Add back the initial gain to match the original number of sessions
initial_gains = gains[:, 0].reshape(-1, 1)  # Extract the initial gains for each user
gain_adjustments = np.hstack((initial_gains, gain_adjustments))  # Concatenate the initial gains with the session-by-session adjustments

# Calculate the mean and percentiles for the individual gain adjustments
gain_adj_mean = np.mean(gain_adjustments, axis=0)
gain_adj_5 = np.percentile(gain_adjustments, 5, axis=0)
gain_adj_95 = np.percentile(gain_adjustments, 95, axis=0)

# Calculate the mean and percentiles of cumulative gains from the simulations
cum_gain_adj_mean = np.mean(gains, axis=0)
cum_gain_adj_5 = np.percentile(gains, 5, axis=0)
cum_gain_adj_95 = np.percentile(gains, 95, axis=0)

# Calculate the delta gain (change from preferred gain)
delta_gain_mean = np.mean(gains - preferred_gains[:, None], axis=0)
delta_gain_5 = np.percentile(gains - preferred_gains[:, None], 5, axis=0)
delta_gain_95 = np.percentile(gains - preferred_gains[:, None], 95, axis=0)

########################################################################################################################################################################
# Plot histogram of preferred gains
########################################################################################################################################################################
plt.rcParams['font.family'] = 'Calibri'
plt.figure(figsize=(8, 6))
plt.hist(preferred_gains, bins=30, color='lightblue', edgecolor='black', alpha=0.7)
plt.title("Histogram of Preferred Gains", fontsize=17, fontweight='bold')
plt.xlabel("Preferred Gain (dB)", fontsize=16, fontweight='bold')
plt.ylabel("Frequency", fontsize=16, fontweight='bold')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)

# Save and show the histogram
folder = 'C:/Users/bc22/OneDrive/Documents/code/gain_adjustment_monte-carlo/'
plt.savefig(folder+'mc_preferred_gains.png', dpi=300, bbox_inches='tight')
plt.show()

########################################################################################################################################################################
# Plot results of simulation with delta gain
########################################################################################################################################################################
plt.figure(figsize=(10, 6))
plt.plot(delta_gain_mean, label="Mean Δ Gain from Preference", color="#4169E1",lw=3)
plt.fill_between(range(num_adjustments), delta_gain_5, delta_gain_95, color='lightblue', alpha=0.2, label="90% Confidence Interval")
plt.title("Convergence to Preferred Gain", fontsize=18, fontweight='bold')
plt.xlabel("Number of Adjustments", fontsize=18, fontweight='bold')
plt.ylabel("Δ Gain (dB)", fontsize=18, fontweight='bold')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(loc='lower right', fontsize=12, frameon=False, framealpha=0.1)
plt.grid(True, linestyle='--', alpha=0.3)

# Save and show the figure
plt.savefig(folder+'mc_convergence.png', dpi=300, bbox_inches='tight')
plt.show()

########################################################################################################################################################################
# Plot individual gain adjustments
########################################################################################################################################################################
plt.figure(figsize=(10, 6))
# Plot the mean individual gain adjustment
plt.plot(gain_adj_mean, label="Mean Adjustment", color="#4169E1", lw=3)
# Fill between the 5th and 95th percentiles for the confidence interval
plt.fill_between(range(num_adjustments), gain_adj_5, gain_adj_95, color='lightblue', alpha=0.2, label="90% CI")
# Update title and labels
plt.title("Trial-by-Trial Gain Adjustments", fontsize=18, fontweight='bold')
plt.xlabel("Number of Adjustments", fontsize=18, fontweight='bold')
plt.ylabel("Gain Adjustment (dB)", fontsize=18, fontweight='bold')
# Style the ticks and legend
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(loc='lower left', fontsize=12, frameon=False, framealpha=0.1)
plt.grid(True, linestyle='--', alpha=0.3)

# Save and show the updated figure
plt.savefig(folder+'mc_adjustments.png', dpi=300, bbox_inches='tight')
plt.show()