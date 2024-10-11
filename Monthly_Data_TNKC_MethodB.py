import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


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

# Now filenames contain all the paths for February and March 2020

# Function to skip the header
def podaacHeaderSkipper(filename):
    with open(filename, 'r') as file:
        next_line = file.readline().strip()
        if next_line.startswith('tSDS'):
            next_line = file.readline()
        else:
            for line in file:
                if line.strip() == '# End of YAML header':
                    break

        filedata = file.readlines()
        return filedata

# List to store the processed file data
all_data = []

# Process each file
for filename in filenames:
    file_data = podaacHeaderSkipper(filename)
    all_data.extend(file_data)  # accumulate data from each file


#extracts the pressures for tank 1 and tank 2
def data_extract(filedata):
    # Initialize lists to store the extracted data
    last_two_elements = []
    last_two_pre = []

    previous_line = None
    preprevios = None

    for line in filedata:
        # Split the line into variables (assuming whitespace separation)
        variables = line.split()
        
        # Check if the current line has more than 9 elements
        if len(variables) > 9:
            if previous_line is not None:
                prev_variables = previous_line.split()
                if len(prev_variables) >= 2:
                    try:
                        last_two = list(map(float, prev_variables[-2:]))
                        last_two_elements.append(last_two)
                    except ValueError:
                        continue

            if preprevios is not None:
                preprevar = preprevios.split()
                if len(preprevar) >= 2:
                    try:
                        last_two2 = list(map(float, preprevar[-2:]))
                        last_two_pre.append(last_two2)
                    except ValueError:
                        continue

        # Update the previous line
        preprevios = previous_line
        previous_line = line

    matrix2 = np.array(last_two_elements) 
    matrix3 = np.array(last_two_pre)  # (86400,2) matrix for last two elements before 9-element rows
    return  matrix2, matrix3


[last_two_elements, pressures] = data_extract(all_data)  # matrix stores time in seconds and last two elements before 9-element rows

#extracts the temperatures for tank 1 and tank 2
def temp_extractor(filedata):
    # Initialize an empty list to store the extracted data
    data = []
    data1 = []
    data2 = []

    for line in filedata:
        # Split the line into variables (assuming whitespace separation)
        variables = line.split()
        # Extract the first variable and convert them to floats
        total_time_Variable = list(map(float, variables[:1]))

        if len(variables) > 9:
            first_variable_secs = list(map(float, variables[:1]))
            data.append(first_variable_secs)
            second_variable_quaternians = list(map(float, variables[7:9]))
            data1.append(second_variable_quaternians)
        data2.append(total_time_Variable)

    matrix = np.array(data)   #(1,86400) matrix for time
    matrix1 = np.array(data1)    #(86400,4) matrix for temperatures
    matrix2 = np.array(data2).T  #total time for epoch  
    return [matrix, matrix1, matrix2]

[time_for_temps, temperatures, total_time] = temp_extractor(all_data) #matrix storage of time and temperatures for both tanks

# Further processing...

plotting_times = []
for i in range(len(time_for_temps)):
    if i % 2 == 0:
        plotting_times.append(time_for_temps[i])


# Separating temperatures and pressures based on tanks
TNK1C_Pressure = []
TNK2C_Pressure = []
TNK1C_Temperature = []
TNK2C_Temperature = []


for i in range(0, len(pressures), 2):
    TNK1C_Pressure.append(pressures[i])  # Append the entire even rows for tank 1
    TNK1C_Temperature.append(temperatures[i])

for i in range(1, len(pressures), 2):
    TNK2C_Pressure.append(pressures[i])    #append the entire odd rows for tank 2
    TNK2C_Temperature.append(temperatures[i])

TNK1C_internal_pressure = []
TNK1C_reg_pressure = []
TNK1C_temp_zenith = []
TNK1C_temp_nadir = []

TNK2C_internal_pressure = []
TNK2C_reg_pressure = []
TNK2C_temp_zenith = []
TNK2C_temp_nadir = []

# For loop separates regulated and internal fuel tank pressure for tank 1
for row in TNK1C_Pressure:
    TNK1C_internal_pressure.append(row[0])
    TNK1C_reg_pressure.append(row[1])

# For loop separates skin temperature(zenith) and adaptive temperature(nadir) for tank 1
for row in TNK1C_Temperature:
    TNK1C_temp_zenith.append(row[0])
    TNK1C_temp_nadir.append(row[1])
    
# For loop separates regulated and internal fuel tank pressure for tank 2
for row in TNK2C_Pressure:
    TNK2C_internal_pressure.append(row[0])
    TNK2C_reg_pressure.append(row[1])

# For loop separates skin temperature(zenith) and adaptive temperature (nadir) for tank 2
for row in TNK2C_Temperature:
    TNK2C_temp_zenith.append(row[0])
    TNK2C_temp_nadir.append(row[1])

TNK1C_average_Temp = []
TNK2C_average_Temp = []
for i in range(len(TNK1C_Temperature)):
    average_Temp = sum(TNK1C_Temperature[i])/2
    average_Temp2 = sum(TNK2C_Temperature[i])/2
    TNK1C_average_Temp.append(average_Temp)
    TNK2C_average_Temp.append(average_Temp2)

def celsius_to_kelvin(TNK1, TNK2):
    TNK1_output = []
    TNK2_output = []
    for i in range(len(TNK1)):
        TNK1_kelvin = TNK1[i] + 273.15
        TNK2_kelvin = TNK2[i] + 273.15

        TNK1_output.append(TNK1_kelvin)
        TNK2_output.append(TNK2_kelvin)
    
    return TNK1_output, TNK2_output

    
[TNK1C_averageTemp_kelvin, TNK2C_averageTemp_kelvin] = celsius_to_kelvin(TNK1C_average_Temp, TNK2C_average_Temp) 
# Variable initiation to compute mass differences
v = 52      # volume of fuel tanks in liters
a = 1.370   # constant for N2 (bar L^2/ mol^2)
b = 0.0387  # constant for N2 (L/mol)
R = 0.08314 # ideal gas constant in (bar L/ mol K)
n0 = 0.5     # initial guess for newton raphson
molar_mass_N2 = 28.006148008 #molar mass of N2 in g/mol
total_mass = 16       # 16 kg of mass per fuel tank 


# Defining Van der Waals modified equation for tanks
def fTNK(n, P, T):
    return (-a*b/(v**2))*n**3 + (a/v)*n**2 - (P*b + R*T)*n + P*v

# Defining the derivative of Van der Waals modified equation for tanks
def f_primeTNK(n, P, T):
    return (-3*a*b/(v**2))*n**2 + (2*a/v)*n - (P*b) - (R*T)

# Newton-Raphson method implementation
def newton_raphson(f, f_prime, x0, P, T, tolerance=1e-8, max_iterations=100):
    x = x0
    for i in range(max_iterations):
        fx = f(x, P, T)
        fpx = f_prime(x, P, T)
        x_new = x - fx / fpx
        if abs(x_new - x) < tolerance:
            return x_new
        x = x_new

# Solve for each value in the lists
n_tank1C_results = []
n_tank2C_results = []

for P, T in zip(TNK1C_internal_pressure, TNK1C_averageTemp_kelvin):
    try:
        n_tank1C = newton_raphson(fTNK, f_primeTNK, n0, P, T)
        n_tank1C_results.append(n_tank1C)
    except ValueError as e:
        print(e)
        n_tank1C_results.append(None)

for P, T in zip(TNK2C_internal_pressure, TNK2C_averageTemp_kelvin):
    try:
        n_tank2C = newton_raphson(fTNK, f_primeTNK, n0, P, T)
        n_tank2C_results.append(n_tank2C)
    except ValueError as e:
        print(e)
        n_tank2C_results.append(None)


mass_TNK1C = []
mass_TNK2C = []

for i in range(len(n_tank1C_results)):
    MTNK1D = (molar_mass_N2*n_tank1C_results[i]) / 1000 # divide by 1000 to convert to kg
    MTNK2D = (molar_mass_N2*n_tank2C_results[i])/1000   # divide by 1000 to convert to kg

    mass_TNK1C.append(MTNK1D)
    mass_TNK2C.append(MTNK2D)


# Loop through each day and calculate the average
def average(data):
    num_days = 2*31 + 29 
    data_points_per_day = len(data)//num_days
    daily_averages_TNK = []
    for i in range(num_days):
        # Extract data for the current day
        start_index = i * data_points_per_day
        end_index = start_index + data_points_per_day
        daily_data = data[start_index:end_index]
        
        # Calculate the average for the current day
        daily_average = np.mean(daily_data)
        daily_averages_TNK.append(daily_average)
    
    return (daily_averages_TNK)

mass_TNK1C_Dailyaverage = average(mass_TNK1C)
mass_TNK2C_Dailyaverage = average(mass_TNK2C)
Temperature_TNK1C_Dailyaverage = average(TNK1C_averageTemp_kelvin)
Temperature_TNK2C_Dailyaverage= average(TNK2C_averageTemp_kelvin)



# (Include the rest of your code here...)

# Save the plots as images
t = list(range(1, len(mass_TNK1C_Dailyaverage) + 1))
plt.figure(figsize=(8, 6))
plt.scatter(t, mass_TNK1C_Dailyaverage, marker='o', linestyle='-', color='b', label='Tank 1C Mass')
plt.title('Mass vs Time for Tank 1C (Jan - Dec 2020)')
plt.xlabel('Time (Days)')
plt.ylabel('Mass (Kg)')
plt.legend()
plt.savefig('tank1c_mass_vs_time.png')

plt.figure(figsize=(8, 6))
plt.scatter(t, mass_TNK2C_Dailyaverage, marker='o', linestyle='-', color='b', label='Tank 2C Mass')
plt.title('Mass vs Time for Tank 2C (Jan - Dec 2020)')
plt.xlabel('Time (Days)')
plt.ylabel('Mass (Kg)')
plt.legend()
plt.savefig('tank2c_mass_vs_time.png')

plt.figure(figsize=(8, 6))
plt.scatter(t, Temperature_TNK1C_Dailyaverage, marker='o', linestyle='-', color='b', label='Tank 1C Temperature')
plt.title('Temperature vs Time for Tank 1C (Jan - Dec 2020)')
plt.xlabel('Time (Days)')
plt.ylabel('Temperature (K)')
plt.legend()
plt.savefig('tank1c_temperature_vs_time.png')

plt.figure(figsize=(8, 6))
plt.scatter(t, Temperature_TNK2C_Dailyaverage, marker='o', linestyle='-', color='b', label='Tank 2C Temperature')
plt.title('Temperature vs Time for Tank 2C (Jan - Dec 2020)')
plt.xlabel('Time (Days)')
plt.ylabel('Temperature (K)')
plt.legend()
plt.savefig('tank2c_temperature_vs_time.png')

# Open a file in write mode ('w') to store mass variables (optional)
with open("output.txt", "w") as file:
    # Write the daily averages to the file
    file.write("mass_TNK1C_Dailyaverage:\n")
    for value in mass_TNK1C_Dailyaverage:
        file.write(f"{value}\n")

    file.write("\nmass_TNK2C_Dailyaverage:\n")
    for value in mass_TNK2C_Dailyaverage:
        file.write(f"{value}\n")

    file.write("\nTemperature_TNK1C_Dailyaverage:\n")
    for value in Temperature_TNK1C_Dailyaverage:
        file.write(f"{value}\n")

    file.write("\nTemperature_TNK2C_Dailyaverage:\n")
    for value in Temperature_TNK2C_Dailyaverage:
        file.write(f"{value}\n")
