########################################################################################################################################################################
# Monte Carlo Simulation of Hearing Aid Gain Adjustments
# Simulates how users self-adjust their hearing aid gain towards their preferred gain. 
# The experiment starts at an initial gain setting and models multiple adjustment sessions (e.g., over days or trials). 
# Monte Carlo simulations introduce variability in user behaviour through varied preferred gain settings and 
# adjustment steps. This allows us to assess how users converge to their preferred gain and the variability in the process.
########################################################################################################################################################################

import numpy as np
import matplotlib.pyplot as plt

########################################################################################################################################################################
# Function to simulate hearing aid gain adjustments over sessions
########################################################################################################################################################################
def simulate_gain_adjustment(initial_gain, preferred_gain, num_adjustments, mean_adjustment, std_dev_adjustment):
    """
    Simulate user adjustments to hearing aid gain over time to approach their preferred gain.
    
    Parameters:
    initial_gain (float): Initial gain setting of the hearing aid (e.g., 0 to 100 scale)
    preferred_gain (float): The user-defined preferred gain setting
    num_adjustments (int): Number of adjustment attempts (e.g., over days or sessions)
    mean_adjustment (float): Mean adjustment per session
    std_dev_adjustment (float): Variability in each adjustment
    
    Returns:
    np.array: Simulated gain adjustments over the sessions
    """
    # Array to store gain settings over time
    gain_settings = np.zeros(num_adjustments)
    gain_settings[0] = initial_gain
    
    for i in range(1, num_adjustments):
        # Simulation of adjustments to gain
        # Generate a random adjustment based on normal distribution
        adjustment = np.random.normal(mean_adjustment, std_dev_adjustment)
        
        # Determines direction of adjustment
        direction = 1 if preferred_gain > gain_settings[i-1] else -1
        # Updates gain setting with adjustment towards prefered gain
        gain_settings[i] = gain_settings[i-1] + direction * adjustment
        
        # Limit gain to a safe and practical range
        gain_settings[i] = np.clip(gain_settings[i], 0, 70)
    
    return gain_settings

########################################################################################################################################################################
# Monte Carlo simulation for gain adjustments with varied preferred gain
########################################################################################################################################################################
def monte_carlo_simulation_varied_preferred_gain(num_simulations, initial_gain, preferred_gain_mean, preferred_gain_std, num_adjustments, mean_adjustment, std_dev_adjustment):
    """
    Perform Monte Carlo simulation for user gain adjustments with varied preferred gain settings.
    
    Parameters:
    num_simulations (int): Number of simulations to run
    initial_gain (float): Initial gain setting
    preferred_gain_mean (float): Mean preferred gain setting
    preferred_gain_std (float): Standard deviation of preferred gain
    num_adjustments (int): Number of adjustments
    mean_adjustment (float): Mean adjustment per session
    std_dev_adjustment (float): Standard deviation of adjustment
    
    Returns:
    np.array: A 2D array where each row is a simulation result over the adjustments
    np.array: A 1D array of the preferred gains for each simulation
    """
    # Array to store all simulation results
    all_simulations = np.zeros((num_simulations, num_adjustments))
    
    # Generate varied preferred gains for each simulation
    preferred_gains = np.random.normal(preferred_gain_mean, preferred_gain_std, num_simulations)
    
    for i in range(num_simulations):
        # Run the gain adjustment simulation for each trial with a unique preferred gain
        all_simulations[i] = simulate_gain_adjustment(initial_gain, preferred_gains[i], num_adjustments, mean_adjustment, std_dev_adjustment)
    
    return all_simulations, preferred_gains

########################################################################################################################################################################
# Set simulation parameters
########################################################################################################################################################################
initial_gain = 0  # Initial gain setting (0 to 100 scale)
preferred_gain_mean = 30  # Mean preferred gain setting
preferred_gain_std = 10  # Standard deviation for preferred gain to introduce variability
num_adjustments = 25  # Number of self-adjustments (e.g., over sessions)
mean_adjustment = 4  # Mean gain adjustment per session
std_dev_adjustment = 1  # Variability in adjustment
num_simulations = 1000  # Number of Monte Carlo simulations

# Run the Monte Carlo simulation with varied preferred gains
simulated_gain_adjustments, preferred_gains = monte_carlo_simulation_varied_preferred_gain(num_simulations, initial_gain, preferred_gain_mean, preferred_gain_std, num_adjustments, mean_adjustment, std_dev_adjustment)

# Calculate the mean and percentiles from the simulations
mean_simulation = np.mean(simulated_gain_adjustments, axis=0)
percentile_5 = np.percentile(simulated_gain_adjustments, 5, axis=0)
percentile_95 = np.percentile(simulated_gain_adjustments, 95, axis=0)

# Calculate the delta gain (change from preferred gain), using varied preferred gains
delta_gain_mean = np.mean(simulated_gain_adjustments - preferred_gains[:, None], axis=0)
delta_gain_5 = np.percentile(simulated_gain_adjustments - preferred_gains[:, None], 5, axis=0)
delta_gain_95 = np.percentile(simulated_gain_adjustments - preferred_gains[:, None], 95, axis=0)

########################################################################################################################################################################
# Plot results
########################################################################################################################################################################
plt.rcParams['font.family'] = 'Calibri'

# Plot the results with delta gain (change from preferred gain)
plt.figure(figsize=(10, 6))
plt.plot(delta_gain_mean, label="Mean Δ Gain from Preference", color="blue",lw=3)
plt.fill_between(range(num_adjustments), delta_gain_5, delta_gain_95, color='lavender', alpha=0.5, label="90% Confidence Interval")
plt.title("Monte Carlo Simulation of Adjustments to Preferred Gain", fontsize=18, fontweight='bold')
plt.xlabel("Number of Adjustments", fontsize=18, fontweight='bold')
plt.ylabel("Δ Gain (dB)", fontsize=18, fontweight='bold')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(loc='lower right', fontsize=12, frameon=False, framealpha=0.1)
plt.grid(True, linestyle='--', alpha=0.3)

# Save and show the figure
folder = 'C:/Users/bc22/OneDrive/Documents/code/gain_adjustment_monte-carlo/'
plt.savefig(folder+'monte_carlo_gain_adjustment_plot.png', dpi=300, bbox_inches='tight')
plt.show()