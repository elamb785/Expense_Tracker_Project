# Expense_Tracker_Project
Track your finances visually using PySimpleGUI!

# Overview
A user can input their monthly bills during the year (or at the end of the year) into the GUI. Values may be edited 
and changed individually or in groups without corrupting the database. Maplotlib canvas is embedded in the GUI and
permits a user to generate a plot for their records. This plot demonstrates bills for each month for a given category 
and year. If the user has omitted intermediary months, the program will notify them in the plot and default those
months to $0.00. The user may also access the monthly and seasonal averages, which are defaulted to "Not Available"
and update automatically as the database recieves data. The goal will be to host this (perhaps via Django) online 
with other like tools for budgeting.

# Features
1) The program minimizes the size of the database by inputting all data with the same year and month at the same 
index in database. The database is a dictionary whose keys are the expense categories and whose values are lists 
with inputted data. 
2) When plotting, the program determines when intermediate data is missing. It also computes averages as data becomes 
available. 
3) All figures which are created can be saved to the local system. 
4) If the total is not provided, the program computes it for the user for future plotting.

# In Use
![img_home](img_home.JPG?raw=true)
Fig 1. Inputting Data of Various Types on Home Page

![img_plot](img_plot.JPG?raw=true)
Fig 2. Creating a Matplotlib Figure with User Data



