
# Name:              Stephen O Driscoll
# Student Number:    R00146853

import numpy as np


# My main runs a while loop displaying menu and getting input until user chooses exit (6)
def main():

    choice = 0

    while choice != 6:

        print("Menu")
        print("1. Basic Statistics for Total Rainfall(Millimetres)")
        print("2. Basic Statistics for Most Rainfall in a Day (Millimetres)")
        print("3. Basic Statistics for Number of Rain days (0.2mm or More)")
        print("4. Wettest Location")
        print("5. Percentage of Rain Days")
        print("6. Exit")
        choice = int(input("> "))

        if choice == 1:
            totalRainfall()

        elif choice == 2:
            mostRainfallDay()

        elif choice == 3:
            rainDays()

        elif choice == 4:
            wettestLocation()

        elif choice == 5:
            percentRainDays()


def totalRainfall():

    location = selectOption()   # Location to examine is chosen

    data = np.genfromtxt(location + "Rainfall.txt", delimiter=' ')  # Get data from appropriate text file
    maximum = np.amax(data[:, 2])       # get maximum of column 3; total rainfall
    average = round(float(np.mean(data[:, 2])), 4)      # Get average of third column rounded to 4 decimal places

    # Display maximum, average and wait for user to hit enter to proceed back to menu
    print(location, ": Max Total Rainfall = ", maximum, sep="")
    print(location, ": Average Total Rainfall = ", average, "\n", sep="")
    input("Press Enter to Continue")


def mostRainfallDay():

    location = selectOption()   # Location to examine is chosen

    data = np.genfromtxt(location + "Rainfall.txt", delimiter=' ')  # Get data from appropriate text file
    maximum = np.amax(data[:, 3])       # get maximum of column 4; most rainfall in a day
    average = round(float(np.mean(data[:, 3])), 4)  # Get average of fourth column rounded to 4 decimal places

    # Display maximum, average and wait for user to hit enter to proceed back to menu
    print(location, ": Max Most Rainfall in a Day = ", maximum , sep="")
    print(location, ": Average Most Rainfall in a Day = ", average, "\n", sep="")
    input("Press Enter to Continue")


def rainDays():

    location = selectOption()   # Location to examine is chosen

    data = np.genfromtxt(location + "Rainfall.txt", delimiter=' ')  # Get data from appropriate text file
    maximum = np.amax(data[:, 4])       # get maximum of column 5; number of rain days
    average = round(float(np.mean(data[:, 4])), 4)      # Get average of fifth column rounded to 4 decimal places

    # Display maximum, average and wait for user to hit enter to proceed back to menu
    print(location, ": Max Number of Rain Days = ", maximum, sep="")
    print(location, ": Average Number of Rain Days = ", average, "\n", sep="")
    input("Press Enter to Continue")


def wettestLocation():

    # Create an array of 5 blank objects and create a parallel array to represent location
    data = np.array([0, 0, 0, 0, 0], dtype=object)
    locations = ["Belfast", "Cork", "Dublin", "Galway", "Limerick"]

    # Populate this data array with our data
    data[0] = np.genfromtxt("BelfastRainfall.txt", delimiter=' ')
    data[1] = np.genfromtxt("CorkRainfall.txt", delimiter=' ')
    data[2] = np.genfromtxt("DublinRainfall.txt", delimiter=' ')
    data[3] = np.genfromtxt("GalwayRainfall.txt", delimiter=' ')
    data[4] = np.genfromtxt("LimerickRainfall.txt", delimiter=' ')

    # Create variables to hold name and wetness of wettest location. Create counter i
    name = ""
    wettest = 0
    i = 0

    # While we haven't checked every location keep iterating
    while i < data.__len__():

        # Set wetness equal to the sum of all values in column 3 rounded to one decimal place and display
        wetness = round(float(np.sum(data[i][:, 2])), 1)
        print(i+1, ". ", locations[i], " ", wetness, "mm", sep="")

        # Check if this location is wetter than our current wettest location
        if wetness > wettest:

            # If it is record the new wettest and name of this location
            wettest = wetness
            name = locations[i]

        i += 1

    # Display details about the wettest location and wait for user to hit enter
    print("The Wettest Location in Ireland is ", name, " with a rainfall figure of ", wettest, "mm", sep="")
    input("Press Enter to Continue")


def percentRainDays():

    # Get the threshold for how many rainy days we want to know are present
    threshold = int(input("Please enter maximum threshold value for number of rain days: "))

    if threshold > 31:

        print("Please input a number 31 or less")
        return

    # Create an array of 5 blank objects and create a parallel array to represent location
    data = np.array([0, 0, 0, 0, 0], dtype=object)
    locations = ["Cork", "Belfast", "Dublin", "Galway", "Limerick"]

    data[0] = np.genfromtxt("CorkRainfall.txt", delimiter=' ')
    data[1] = np.genfromtxt("BelfastRainfall.txt", delimiter=' ')
    data[2] = np.genfromtxt("DublinRainfall.txt", delimiter=' ')
    data[3] = np.genfromtxt("GalwayRainfall.txt", delimiter=' ')
    data[4] = np.genfromtxt("LimerickRainfall.txt", delimiter=' ')

    # Display header for printing percentage of months with more than threshold rain days
    print("The following are the percentage of rain days less than or equal to ", threshold, ": ", sep="")

    i = 0

    while i < data.__len__():

        result = data[i][:, 4] <= threshold     # Result is an array of booleans, true if less than threshold

        # Get percent of months that have less than threshold rainy days and display
        percent = round((len(data[i][result]) * 100.0) / len(data[i]), 2)
        print(i + 1, ". ", locations[i], " ", percent, "%", sep="")

        i += 1

    input("Press Enter to Continue")


# Select location simply with if statements
def selectOption():

    location = ""

    print("1. Cork")
    print("2. Belfast")
    print("3. Dublin")
    print("4. Galway")
    print("5. Limerick")
    choice = int(input("Please select a location:"))

    print()

    if choice == 1:
        location = "Cork"

    elif choice == 2:
        location = "Belfast"

    elif choice == 3:
        location = "Dublin"

    elif choice == 4:
        location = "Galway"

    elif choice == 5:
        location = "Limerick"

    return location


main()

exit(0)
