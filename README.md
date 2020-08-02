# Expense_Tracker_Project
Track your finances visually using PySimpleGUI!

# OVERVIEW:
A user can input their monthly bills during the year (or at the end of the year) into the GUI. Values may be edited 
and changed individually or in groups without corrupting the database. Maplotlib canvas is embedded in the GUI and
permits a user to generate a plot for their records. This plot demonstrates bills for each month for a given category 
and year. If the user has omitted intermediary months, the program will notify them in the plot and default those
months to $0.00. The user may also access the monthly and seasonal averages, which are defaulted to "Not Available"
and update automatically as the database recieves data. The goal will be to host this (perhaps via Django) online 
with other like tools for budgeting.

# ISSUES:
1) If a user clicks view data or cancel, I want the fields to
not clear.
2) Needs try catch statements to make sure that 
  a) Users input year and month as integers
  b) All expense categories are inputted as floats (only period delimiters)
  c) No characters are ever inputted
3) The program should not stop if the user clicks cancel then clicks X.
  a) can be awkwardly fixed with adding ", background_color = 'blue',no_titlebar=True" to its popup arguments
4) The average button drops the trailing zero when performing round with integer-valued
floats. Decimal class would resolve this.

# FUTURE ADD-ONS
1) A compare button so that we can compare plots from different years
2) Introduce a CLEAR button to remove one entry from the database (probably by
the user inputting the year and month and bill that they want to change--no bill
indicated means clear all data from that month and year)

