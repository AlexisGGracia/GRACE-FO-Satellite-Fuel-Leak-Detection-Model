# GRACE-FO Satellite Fuel Leak Detection Model in Python

## Introduction

In this project, I analyze the evolution of a fuel leak in the GRACE-FO satellite. The model considers several key factors, including the mass flow rates of the thrusters, the time intervals of thruster usage (Δt), activation periods of the thrusters, internal pressure of the tanks, and the temperature in both the zenith and nadir directions of the fuel tanks.

This project aims to study the evolution of the leak, though the model is a work in progress and continuously evolving as I conduct further research. The ultimate goal is to translate these findings into a Markov Chain model to predict future fuel leak behavior, which is crucial for orbit-raising strategies.

During this research, I explore two methods to estimate and verify fuel leaks in the tanks:

### **Method 1:**

  - Estimating the ideal mass inside the tanks assuming no leaks, using thruster mass flow rates.
### Mass Flow Rate Equation (Solving for Mass):

The mass flow rate equation is typically given by:

$$
\dot{m} = \frac{m}{\Delta t}
$$

To solve for the mass \(m\), we rearrange the equation:

$$
m = \dot{m} \times \Delta t
$$

where:

 - $\dot{m}$ = Mass flow rate (kg/s)
 - $m$ = Mass (kg)
 - $\Delta t$ = Time interval (s)


 

 ### **Method 2:** 

  - Calculating the mass inside the fuel tanks at all times using the **Van der Waals modified equation**:

$$
\left( P + \frac{a}{V^2} \right) \left( V - b \right) = nRT
$$

Where:
  - \(P\) = Pressure of the gas (Pa)
  - \(V\) = Volume of the tank (m³)
  - \(n\) = Number of moles of gas (mol)
  - \(R\) = Universal gas constant (8.314 J/mol·K)
  - \(T\) = Temperature (K)
  - \(a\) = Van der Waals constant (Pa·m⁶/mol²)
  - \(b\) = Van der Waals constant (m³/mol)


## How do we confirm if we have a leak in the fuel system? 

- To confirm if we have a leak, we compare the results from method 1 and method 2. Given that method 1 computes the mass that should be in the fuel tanks without any leaks since it only accounts for mass leaving the system through the appropiate output surface (thrusters) using an integrative style and method 2 computes the instantaneous mass in the fuel tanks disregarding previous states, we can compare both results. If there is a difference in the mass estimates between method 1 and 2, we can confirm that we have a leak and the leak is the difference in both methods. If both results are the same, then no leak is present.


## Purpose

This project is part of my undergraduate research at The University of Texas Center for Space Research.


# Code Breakdown and Workflow

This section provides a detailed explanation of the logic and steps involved in the code.

1. **Upload data into python**
   - I have included a for loop in this section such that it processes mutliple files using the datetime function to process anual data
   - Example:
   ```Python
   base_dir = '/Volumes/GRACEFO/GRACE-FODATA/'
   filename_template = 'gracefo_1A_{date}_RL04.ascii.noLRI/TNK1A_{date}_C_04.txt'  # Define the template
   months = {'01':31,'02':29, '03':31} 
   filenames = []

   # Generate filenames for each day in February and March 2020
   for month, days in months.items():
    for day in range(1, days + 1):
        date_str = f'2020-{month}-{day:02d}'  # Format date string with numeric month
        month_dir = f'{datetime.date(2020, int(month), 1):%B}_2020/'  # Convert numeric month to full month name
        filename = base_dir + month_dir + filename_template.format(date=date_str)
        filenames.append(filename)
     
         
2. **Developed a function to skip the introduction header that is given for each data file downloaded from NASA po.daac (optional)**
4. **Extract the pressure from tank 1 and 2 to be used for method 2**
5. **Extract temperature in the nadir and zenith direction of tanks 1 and 2 to be used for method 2**
6. **Define the variables necessary to implement vander waals modified equation such as constants a and b which are dependent on propellant type being used in propulsion systems**
7. **Use Newton Raphson Method to find the number of moles from Van der Waals equation**
    - Approximating the root of a Van der Waals modified equation using the **Newton-Raphson method**:

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

  Where:
      - $x_{n+1}$ is the next approximation of the root
      - $x_n$ is the current approximation
      - $f(x_n)$ is the value of the function at $x_n$
      - $f'(x_n)$ is the derivative of the function at $x_n$

  The iteration continues until the difference between $x_{n+1}$ and $x_n$ is smaller than a predefined tolerance.


        













9. **Propagate the orbit using ODE45 based on two-body dynamics**, including J2 perturbations.










10. **Determine the accuracy of the solution by:**
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
