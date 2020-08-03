# Expense Tracking GUI
# Created By: Evan Lamb
# Date Writtten: 7/20/2020 - (current)

import json
import calendar
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# Helper function
matplotlib.use("TkAgg")

def draw_sample_figure(canvas, figure):
    '''Create the sample figure on the GUI's front page'''
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def set_inter_months(x, y):
    '''Set bill of omitted intermediate months to be 0 when plotted.'''
    flag = 0
    first_month = min(x)
    last_month = max(x)
    for i in range(first_month, last_month + 1):
        if i not in x:
            x.insert(-1, i)
            y.insert(-1, 0)
            flag = 1
    return x, y, flag

def draw_plot(x_vals, y_vals, field_name, yr):
    '''Create a matplot figure in a new window given data'''
    x_values, y_values, changed = set_inter_months(x_vals, y_vals)
    x_values, y_values = zip(*sorted(zip(x_values, y_values))) # reorder months in ascending order
    plt.grid()
    plt.margins(x=0)
    if changed:
        plt.title(f"Expenses Over Time for {field_name} in {yr}*\n*Intermediate months with no data deafulted to $0.00.")
    else:
        plt.title(f"Expenses Over Time for {field_name} in {yr}\n")
    plt.ylabel("$")
    plt.xlabel("Month")
    plt.xticks(np.arange(1, 13, step=1), calendar.month_abbr[1:13])
    plt.plot(x_values, y_values)
    plt.show(block=False)

def show_sample_figure(x_values, y_values):
    '''Define characteristics of matplot figure'''
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title('Expenses Over Time for Electricity in 2019')
    ax.set_xlabel('Month')
    ax.set_xticklabels(calendar.month_abbr[0:13])
    ax.set_ylabel('$')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.margins(x=0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.plot(x_values, y_values)
    return fig, ax

def store_data(database, data, keyList):
    count = 0
    for k, v in data.items():
        if count < 10:
            assign_data(keyList[k], v, count)
            count += 1  

    tot = 0
    if data[10] == '':
        for i in range(2, 10):
            if data[i] != '':
                tot += float(data[i])
        database['Total'].append(tot)
    else:
        tot = float(data[10])
        database['Total'].append(tot)

def get_expense_data(database, field_name, yr):
    '''Search database for the user's desired data and return it'''
    x, y = [], []
    for index, _ in enumerate(database):
        if index < len(database['Year']):
            if database['Year'][index] == int(yr):
                x.append(database['Month'][index])
                y.append(database[field_name][index])
    return x, y

def assign_data(key, value, count):
    '''Assign values inputted into the GUI into the database'''
    default = 0
    if value == '':
        expenses[key].append(default)
    else:
        if count < 2:
            expenses[key].append(int(value))
        else:
            expenses[key].append(float(value))

def compute_seasonal_costs(database):
    '''Determine the total bill for each season'''
    sum_winter, sum_spring, sum_summer, sum_fall = [], [], [], []
    for index, _ in enumerate(database['Months']):
        if 1 <= months[index] <= 3:
            sum_winter.append(costs[index])
        elif 4 <= months[index] <= 6:
            sum_spring.append(costs[index])
        elif 7 <= months[index] <= 9:
            sum_summer.append(costs[index])
        else:
            sum_winter.append(costs[index])
    return sum_winter, sum_spring, sum_summer, sum_fall

def find_averages(sum_winter, sum_spring, sum_summer, sum_fall):
    ''' Compute the average bill for each season. Handles missing months'''
    if sum_winter == []:
        aver_winter = 'Not available'
    else:
        aver_winter = '$' + str(round(sum(sum_winter)/len(sum_winter), 2))
    if sum_spring == []:
        aver_spring= 'Not available'
    else:
        aver_spring = '$' + str(round(sum(sum_spring)/len(sum_spring), 2))
    if sum_summer == []:
        aver_summer = 'Not available'
    else:
        aver_summer = '$' + str(round(sum(sum_summer)/len(sum_summer), 2))
    if sum_fall == []:
        aver_fall = 'Not available'
    else:
        aver_fall = '$' + str(round(sum(sum_fall)/len(sum_fall), 2))
    return aver_winter, aver_spring, aver_summer, aver_fall

def get_index_to_change(database, year, month):
    '''Determine the index of the year/month element in the list of previous entries'''
    indices = [j for j, x in enumerate(database['Year']) if x == int(year)]
    matches = []
    if indices:
        for _, i in enumerate(indices):
            if database['Month'][i] != int(month):
                matches.append(i)
        for i in matches:
            indices.remove(i) 
    return indices

def verify_in_database(database, year, month, data_to_check=[]):
    '''Determine whether the inputted data is already in the database'''
    storage = {}
    fields_w_data_already = []
    i = get_index_to_change(database, year, month)

    if i:   
        for bill_type in data_to_check: # this is a integer valued for each
            if database[keyList[bill_type]][i[0]] == 0 or database[keyList[bill_type]][i[0]] != 0:
                fields_w_data_already.append(bill_type)

        if any(fields_w_data_already):
            for index, data in enumerate(fields_w_data_already):
                fields_w_data_already[index] = keyList[data]
                storage.update({fields_w_data_already[index]: i})
            # storage will be a dictionary where keys are bills being overwritten and values is the index value (index is always the same for each key)
            return True, storage
    else:
        return False, None

# Define database 
keyList = ['Year', 'Month', 'Water', 'Phone', 'Electric', 'Groceries', 'Housing', 'Automotive', 'Tithes', 'Misc', 'Total']

expenses_map = {}
expenses = {}

val = 0
for key in keyList:
    expenses_map.update({key: val})
    expenses[key] = []
    val += 1

# Create the GUI's layout

tab1_layout = [[sg.T('Enter a year')],
               [sg.In(key='Water1')]]
tab2_layout = [[sg.T('Enter a year')],
               [sg.In(key='Phone1')]]
tab3_layout = [[sg.T('Enter a year')],
               [sg.In(key='Electric1')]]
tab4_layout = [[sg.T('Enter a year')],
               [sg.In(key='Groceries1')]]
tab5_layout = [[sg.T('Enter a year1')],
               [sg.In(key='Housing1')]]
tab6_layout = [[sg.T('Enter a year')],
               [sg.In(key='Automotive1')]]
tab7_layout = [[sg.T('Enter a year')],
               [sg.In(key='Tithes1')]]
tab8_layout = [[sg.T('Enter a year')],
               [sg.In(key='Misc1')]]
tab9_layout = [[sg.T('Enter a year')],
               [sg.In(key='Total1')]]

col_1 = [[sg.Text('WELCOME TO EXPENSE TRACKER\nInstructions For Use\nSubmit = Enter or edit or zero specific data (default for each bill is 0)\nView Data = View current data \
    \nCancel = Erase all expense data\nPlot = Plot monthly bill data for a given expense category and year \n(intermediate months with no data default to $0.00) \
    \nAverage = Computes seasonal and monthly averages for a given year for data')],
    [sg.Text('Please enter the year and month as numbers')], 
    [sg.Text('Year', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Month', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Please fill out at least one of the relevant expense data fields below (default is 0)')],
    [sg.Text('Water', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Phone', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Electric', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Groceries', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Housing', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Automotive', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Tithes', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('Misc', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Text('OR enter the total expenses for that month')],
    [sg.Text('Total', size=(15, 1)), sg.InputText(do_not_clear=False)],
    [sg.Submit(), sg.Button('View Data'), sg.Cancel()]]

col_2 = [[sg.Text('Select the Category for which you would like to see Expenses per month')],
    [sg.TabGroup([[sg.Tab('Water', tab1_layout), sg.Tab('Phone', tab2_layout), sg.Tab('Electric', tab3_layout), sg.Tab('Groceries', tab4_layout), sg.Tab('Housing', tab5_layout), sg.Tab('Automotive', tab6_layout), sg.Tab('Tithes', tab7_layout), sg.Tab('Misc', tab8_layout), sg.Tab('Total', tab9_layout),]])], [sg.Button('Plot'), sg.Button('Average')],
    [sg.Text("Displaying Sample Expenses...")],
    [sg.Canvas(key="-CANVAS-")]]

layout = [[sg.Column(col_1), sg.Column(col_2)]]

# Create the form and show it without the plot
window = sg.Window(
    "Expense Tracker", 
    layout, 
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 12",
)

# Create data for sample plot 
t = np.arange(1, 13, 1)
y = [24.45, 28.75, 32.78, 33.98, 54.87, 79.65, 85.43, 75.51, 52.11, 43.90, 40.96, 37.65]
fig, ax = show_sample_figure(t, y)
draw_sample_figure(window["-CANVAS-"].TKCanvas, fig) 

# Create default value for table
default = 0

while True:

    event, values = window.read() # values[0] would be year, values[1] would be month
    b = list(values.values())[:-2]

    # If some fields are filled and the user presses submit, run this
    if bool(any(b)) and event == 'Submit':

        if values[0] == '' or values[1] == '': 
            sg.popup('Please enter a year and a month.', title='ERROR')
        else:
            # Determine which fields were filled
            l = (2, 3, 4, 5, 6, 7, 8, 9, 10)
            ans = {k:values[k] for k in l if k in values}
            filled_entries = [k for k, v in ans.items() if v != '']

            if filled_entries == []:
                continue

            # Check for previously stored data with that year and month an bill
            occupied, filled_bills = verify_in_database(expenses, values[0], values[1], filled_entries)

            if occupied:
                sg.popup_yes_no(f"You already have other data for year: {values[0]} and month: {values[1]}\n WARNING: You may be overwriting a bill's amount.\n Do you wish to overwrite the data?", title='WARNING')
                if event == 'Submit':
                        changes = 0 # new_values - old_values
                        for bill, index in filled_bills.items(): 
                            old_val = expenses[bill][index[0]]
                            new_val = float(values[keyList.index(bill)])
                            expenses[bill][index[0]] = new_val
                            changes += new_val - old_val
                            if filled_entries == [10]:
                                expenses['Total'][index[0]] = float(values[10])
                            else:
                                expenses['Total'][index[0]] = expenses['Total'][index[0]] + changes
                        sg.popup('Data Overwritten Successfully! Please enter more data or plot.', title='SUCCESS')
            else:
                store_data(expenses, values, keyList)
                sg.popup('Data Saved Successfully! Please enter more data or plot.', title='SUCCESS')

    if event == 'View Data':
        sg.popup(expenses)
        #sg.popup(json.dumps(expenses, indent=4, sort_keys=True))
        #sg.popup(str(expenses).replace(', ',',\n '), title='CURRENT DATA')

    if event == 'Cancel':
        event = sg.popup_yes_no('Are you sure you want to clear all expense data?', title='WARNING')
        if event == 'Yes':
            for key in keyList:
                expenses[key] = []

    if event == 'Plot' and values[11] != '': # make sure no null tabs are present
        # determine which tab the user is using and get the year
        tab_name = values[11]
        year = values[tab_name + '1']
        if year == '':
            sg.popup("Please enter a year and then replot", title='ERROR')
        else:
            if len(expenses['Year']) == len(expenses['Month']) == len(expenses[tab_name]) and len(expenses['Year']) > 1:
                x, y = get_expense_data(expenses, tab_name, year)
                if any(y):
                    draw_plot(x, y, tab_name, year)
                else:
                    sg.popup(f"You have no data stored for {tab_name} bills in {year}.", title='ERROR')
            else:
                sg.popup(f"The number of year, month, and {tab_name} bill values are not equal " \
                    "or you need to enter more than one month\'s expenses.", title='ERROR')

    if event == 'Average' and values[11] != '': # make sure no null tabs are present
        tab_name = values[11]
        year = values[tab_name + '1']
        if year == '' and len(expenses[tab_name]) == 0:
            sg.popup("Please check that at least one month\'s expenses have been entered and then enter a year.", title='ERROR')
        elif year == '':
            sg.popup("Please enter a year and retry.", title='ERROR')
        elif len(expenses[tab_name]) == 0:
            sg.popup("Please check that at least one month\'s expenses have been entered.", title='ERROR')
        else:
            months, costs = get_expense_data(expenses, tab_name, year)
            if costs == []:
                aver = 'Not available'
            else:
                aver = '$' + str(round(sum(costs)/len(costs), 2))
            results = {'Months': months, 'Costs': costs}
            sum_winter, sum_spring, sum_summer, sum_fall = compute_seasonal_costs(results)
            aver_winter, aver_spring, aver_summer, aver_fall = find_averages(sum_winter, sum_spring, sum_summer, sum_fall)
        
            sg.popup(f"Average Monthly {tab_name} bill in {year}: {aver}\n"\
                f"Average Seasonal {tab_name} bill in {year}...\n" \
                    f"\tWinter (Jan - Mar): {aver_winter}\n"\
                    f"\tSpring (Apr - Jun): {aver_spring}\n"\
                    f"\tSummer (Jul - Sept): {aver_summer}\n"\
                    f"\tFall (Oct - Dec): {aver_fall}\n")

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
