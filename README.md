# GRACE-FO Twin Satellite Fuel Leak Detection Model in Python

## Introduction

This research focuses on developing a software simulation to model fuel leaks in the GRACE-FO twin satellites using a Markov Chain as a mathematical framework to predict future states (leak/no leak/gross leak) for orbit-raising strategies. The model accounts for several key factors, including the mass flow rates of 32 thrusters (16 per satellite), time intervals of thruster usage (Δt), activation periods, internal tank pressure (2 tanks per satellite), temperatures in both the zenith and nadir directions, fuel mass levels, and the Van der Waals modified equation to quantify the instantaneous fuel levels in the tanks, incorporating a beta prime analysis. In this repository, I have **only** included the beginning portion of the research which is an analyzis of the fuel leak evolution of the GRACE-FO satellites given that this ongoing research currently developing

This repository contains only the initial portion of the research, focusing on the analysis of fuel leak evolution and presenting the strategies used to confirm and quantify a fuel leak in the GRACE-FO satellites, as further details remain confidential. The model is a work in progress and it is continuously evolving as I conduct further research. **The ultimate goal** is to translate these findings into a **Markov Chain model** to predict future fuel leak behavior, which is crucial for **orbit-raising strategies.**


### Important Information:

- The integration of Markov Chains, in depth details about the propulsion systems, and the application of this model are part of ongoing research and considered classified.
- Not all data and code files can be shared at this time, pending further notice.
- As a result, this document provides only a **brief summary** of the fuel leak model's development to showcase my knowledge of propulsion systems, research methodology, and coding skills.

## Purpose

This project is part of my undergraduate research at The University of Texas Center for Space Research under the invaluable guidance of the distinguished scientist, engineer, and esteemed professor, Dr. Srinivas Bettadpur, whose groundbreaking work in satellite geodesy and Earth science has greatly influenced my academic journey, I have had the privilege to grow both as a student and aspiring engineer. Dr. Bettadpur's mentorship has been instrumental in shaping my understanding of advanced propulsion systems and their potential to revolutionize space exploration.



## Estimation of Mass Inside Fuel Tanks
- During this research, I explore two methods to estimate and verify fuel leaks in the tanks:

### **Method 1:**

  - Estimating the ideal mass inside the tanks assuming no leaks, using thruster mass flow rates.
### Mass Flow Rate Equation (Solving for Mass):

The mass flow rate equation is typically given by:

$$
\dot{m} = \frac{m}{\Delta t}
$$

To solve for the mass \(m\), we rearrange the equation and integrate over a period of time:

$$
m = \dot{m} \times \Delta t
$$

where:

 - $\dot{m}$ = Mass flow rate (kg/s)
 - $m$ = Mass (kg)
 - $\Delta t$ = Time interval (s)


 
 ### **Method 2:** 

  - Calculating the instantaneous mass inside the fuel tanks using the **Van der Waals modified equation**:
    - Solve for the number of mols using a numerical method to find the root.
    - I decided to use Newton Raphson method because when VDW modified equation is rearranged to find (n), it forms a cubic function with two imaginary roots and one real root (root of interest)
      and the derivative evaluated at the points is never a number close to zero. Therefore, it converges fast and does not overshoot

$$
\left( P + \frac{a}{V^2} \right) \left( V - b \right) = nRT
$$

Where:
  - \(P\) = Pressure of the gas (Pa)
  - \(V\) = Volume of the tank (m³)
  - \(n\) = Number of moles of gas (mol)
  - \(R\) = Universal gas constant (8.314 J/mol·K)
  - \(T\) = Temperature (K)
    - In our case, the temperature used is an average of the temp in the zenith and nadir direction combined
  - \(a\) = Van der Waals constant (Pa·m⁶/mol²)
  - \(b\) = Van der Waals constant (m³/mol)

   


## How do we confirm if we have a leak in the fuel system? 

- To confirm a leak, we compare results from two methods. Method 1 calculates the expected mass in the fuel tanks assuming no leaks, based solely on the mass exiting through the thrusters. Method 2 measures the current mass in the tanks without considering past states.   If there’s a discrepancy between the two results, it indicates a leak equal to that difference. If the results match, no leak is present.



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
4. **Extract the pressure from tank A and B to be used for method 2**
5. **Extract temperature in the nadir and zenith direction of tanks 1 and 2 to be used for method 2**
6. **Extract the mass flow rates, and time intervals**
7. **Use method 1 to find the ideal mass inside of the fuel tanks**
8. **Define the variables necessary to implement vander waals modified equation such as constants a and b which are dependent on propellant type being used in propulsion systems**
9. **Use Newton Raphson Method to find the number of moles from Van der Waals equation**
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


9. **Convert the number of mols to mass by multiplying times the molar mass of the propellant**
11. **Plot mass vs time for both methods**



### Important Notes

- **Newton Raphson Method**: I decided to use Newton Raphson method to find the root of the functions since Vander Waals modified equation becomes a cubic function
                             when rearrange having n as the unknown variable which presents three roots. Two roots are imaginary, and one real root which is the root
                             we are interested in finding. Given that it really only has one root to find, you cannot miss the root by choosing the wrong guess.
                             Additionally, the derivative evaluated at some x values does not result in a small value close to zero for all points tested.
                             Therefore, it will not overshoot the root finding process.
                        



# Results
In this section, I have included the mass versus time plots for the month of July 2020. Each daily file was average per day to simplify the visual results and estimate on average what the mass is per day.


- **Hand Calculation Comparasion**: This was done for July 1st 2020. Only one day is included in this report for simplification
<img width="1091" alt="Screenshot 2024-10-11 at 1 26 44 AM" src="https://github.com/user-attachments/assets/b80d6c8c-07d3-4c6e-96de-b1ff192a8fc9">

    
## Method 1 Daily Mass vs Time average per hour: 


<img width="935" alt="Screenshot 2024-10-11 at 1 27 07 AM" src="https://github.com/user-attachments/assets/eb262d85-4c27-407b-9a56-e11b1fcf68da">


## Method 1 Monthly average per day Mass vs Time for Tanks C and D: 

<img width="835" alt="Screenshot 2024-10-11 at 1 27 38 AM" src="https://github.com/user-attachments/assets/5e37af29-69ad-4e8c-a285-2d84cd9242ff">

## Method 2 Daily Mass vs Time average per hour: 

<img width="921" alt="July Method 2" src="https://github.com/user-attachments/assets/c78085ff-2edf-48ed-b167-323beb4e1bcc">


## Method 2 Monthly average per day Mass vs Time: 

<img width="903" alt="Screenshot 2024-10-11 at 1 27 54 AM" src="https://github.com/user-attachments/assets/e3b8b6da-05c0-45d5-be06-a9f6a3d2ff8d">

## Important Observations of Results:
- The plots for mass vs time using method 2 for individual days oscillates. If we take a closer look at the temperature data, we can notice that the temperatures oscillates causing the mass output to oscillate. The reason why the temperature of the satellite is oscillating is due to the rotation of the spacecraft as this motion causes some panels to be in the shadow protected from the sun and other panels to be more directly impacted by the photons. additionally, unpredicted solar storms with an unsteady intensity is another factor influencing the variation in the temperatures. 



### Requirements

- **Python**: Ensure you have Python installed on your system. You can download and install Python from the official [Python website](https://www.python.org/downloads/).
  
- **NASA Level 1A Public Data Access**: You need access to NASA Level 1A public data, available through the [Physical Oceanography Distributed Active Archive Center (PO.DAAC)](https://podaac.jpl.nasa.gov/). You can access the data by creating a free [NASA Earthdata account](https://urs.earthdata.nasa.gov/) and downloading the required datasets from the PO.DAAC repository.


## Contributor

This project was developed and maintained by:

- **Alexis Gracia**  
  [GitHub Profile](https://github.com/AlexisGGracia)  
  [Email](mailto:agg3455@my.utexas.edu)
