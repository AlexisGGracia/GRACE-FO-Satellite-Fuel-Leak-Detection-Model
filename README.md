# GRACE-FO Satellite Fuel Leak Detection Model in Python

## Introduction

In this project, I analyze the evolution of a fuel leak in the GRACE-FO satellite. The model considers several key factors, including the mass flow rates of the thrusters, the time intervals of thruster usage (Δt), activation periods of the thrusters, internal pressure of the tanks, and the temperature in both the zenith and nadir directions of the fuel tanks.

This project aims to study the evolution of the leak, though the model is a work in progress and continuously evolving as I conduct further research. The ultimate goal is to translate these findings into a Markov Chain model to predict future fuel leak behavior, which is crucial for orbit-raising strategies.

During this research, I explore two methods to estimate and verify fuel leaks in the tanks:

### **Method 1:**

  - Estimating the ideal mass inside the tanks assuming no leaks, using thruster mass flow rates.

### **Method 2:** 

  - Calculating the mass inside the fuel tanks at all times using the Van der Waals equation:

$$
P = \frac{nRT}{V - nb} - \frac{a}{V^2}
$$

Where:
  - \(P\) is the pressure inside the tank,
  - \(V\) is the volume,
  - \(n\) is the number of moles,
  - \(R\) is the gas constant (8.314 J/mol·K),
  - \(T\) is the temperature,
  - \(a\) and \(b\) are Van der Waals constants.

### Mass Flow Rate Equation (Solving for Mass):

The mass flow rate equation is typically given by:

$$
\dot{m} = \frac{m}{\Delta t}
$$

To solve for the mass \(m\), we rearrange the equation:

$$
m = \dot{m} \times \Delta t
$$

Where:
  - \( \dot{m} \) is the mass flow rate (kg/s),
  - \( m \) is the mass (kg),
  - \( \Delta t \) is the time interval (seconds).

## Purpose

This project is part of my undergraduate research at The University of Texas Center for Space Research.







# Code Breakdown and Workflow

This section provides a detailed explanation of the logic and steps involved in the code.

1. **Defines parameters such as semi-major axis, eccentricity, Greenwich Sidereal Meridian Time (GMST) at burnout, etc.**

   - Orbital elements such as semi-major axis, eccentricity are determined based on mission constraints such as altitude of orbiting spacecraft and desired orbit type.
   - Parameters defined are as follows:

   ```MATLAB
   % Defining parameters
   format longG
   a = 6500;                       % Semi-major axis (km)
   e = 0.001;                      % Orbit's eccentricity
   theta1 = 20*pi/180;             % Initial true anomaly at burnout
   GSMT = 0;                       % Greenwich Sidereal Meridian time at burnout
   mu_earth = 398600.4415;         % Gravitational parameter of Earth (km^3/s^2)
   R_earth = 6378.1363;            % Radius of Earth (km)
   J2 = 0.0010826267;              % J2 perturbations due to Earth's obliqueness
   w_earth = 2*pi / 86164;         % Earth's rotation rate
   n = 10;
   iterations = 4;
   i = 1;                          % Counting variable
   f = 3.353*10^-3;               % Earth's obliqueness constant
   height = 0;

     
         
2. **Using Katherine Johnson and Skopinski NASA technical notes, determine the burnout azimuth of the spacecraft.**

3. **Determine the orbital elements of the satellite at burnout** to achieve the goal of passing over a desired position after a precise number of revolutions.

4. **Propagate the orbit using ODE45 based on two-body dynamics**, including J2 perturbations.

5. **Determine the accuracy of the solution by:**
   - (a) **Generating groundtracks for the satellite**, including coastlines and the desired location on the map.
   - (b) **Plotting the satellite elevation relative to the desired location** over the time period when it should pass overhead.


### Important Notes

- **J2 Perturbations**: In this project, J2 perturbations (due to Earth's oblateness) are only considered during the **first iteration** of the burnout azimuth calculation.
                        This is because the primary goal of this calculation is to determine the **initial azimuth angle at burnout** required to position the spacecraft
                        over a target location immediately after burnout.
                        
  
- **First Iteration**: During the first iteration, J2 perturbations are included to refine the orbital parameters (such as inclination and node) at the moment of burnout.
                       These perturbations slightly affect the spacecraft’s trajectory and need to be accounted for to ensure accurate initial positioning.

- **Subsequent Iterations**: For later iterations, J2 perturbations are **ignored**. This simplification is made because the subsequent calculations focus primarily on
                             placing the satellite in the desired position **immediately after burnout**. The long-term effects of J2 on the orbit (such as orbital precession)
                             are considered minimal for this immediate mission goal.

- **Why This Approach?**: The neglect of J2 in later iterations is a practical choice, as the impact of J2 on short-term positioning is minimal compared to the complexity
                          it would add to the calculations. For long-term mission planning, J2 and other perturbations should be modeled, but for the purposes of this burnout
                          azimuth determination, they do not significantly affect the accuracy of the placement.




  
## Requirements

To run this project, you will need the following software and tools:

- **MATLAB**: Ensure that MATLAB is installed. You can download it from [here](https://www.mathworks.com/products/matlab.html).
- **MATLAB Toolboxes**: The following toolboxes are recommended for running the simulations:
  - Aerospace Toolbox
  - Mapping Toolbox
  - MATLAB functions which are included as separate files under this project 

### Additional Information:
The project uses MATLAB's built-in functions and toolboxes to perform orbital simulations, including two-body propagation, J2 perturbations, and groundtrack generation.

You can install necessary MATLAB packages directly through the MATLAB interface.


# Visual Results
In this section, I have included the groundtracks and an elevation plot relative to my desire location that demonstrates the accuracy of this model.

## Groundtracks: 

- **Groundtracks**: Starting location is along the coast of california and final destination is Austin, Texas. My mission was designed such that it completes this after 10th orbital periods.
![Austin_Grountrack_Pic](https://github.com/user-attachments/assets/95396d28-e579-4f98-964d-ea55ac6b8ee7)
    
## Elevation vs Time plot: 

- **Elevation Plot**: The elevation plot versus time plot helps track how the altitude of a spacecraft changes over time, providing valuable insight into its orbital path and visibility from a ground station or observation point. 
   - Since the final destination is Austin, Texas (right above the ground station) it shows that the final elevation is 90 degrees

![Austin_Texas_ELEVATION](https://github.com/user-attachments/assets/dbe41be2-75e8-48ee-8ffe-a421fe4186d0)

## Citations

H. Skopinski and K. G. Johnson, *"Determination of Azimuth Angle at Burnout for Placing a Satellite Over a Selected Earth Position"*, NASA Tech Note D-233, September 1960. [NASA Technical Report](https://ntrs.nasa.gov/citations/19980227091)


## Contributor

This project was developed and maintained by:

- **Alexis Gracia**  
  [GitHub Profile](https://github.com/AlexisGGracia)  
  [Email](mailto:agg3455@my.utexas.edu)
