
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Number:43792964
#
#   Student Name:Junchuan Xue
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *

#####################################
# End of support 
#####################################

# Add your code here

def load_dates(stations):
    """Return the list of all the dates in the data set.

    Takes a list of stations(produced by the load_stations function)
    and returns the list of all the dates in the data set.
    
    load_dates(list[str]) -> list[str]
    Precondition: All the listed station files exist and are readable and in the correct format
    (in this function, the first station file in the list is used).
    
    """
    dates=[]
    f=open(stations[0]+".txt",'r')
    for line in f:
        dates.append(line[0:8])
    f.close()
    return dates

def load_station_data(station):
    """Return the list of temperatures of the given station.

    Takes a station name and returns the list of temperatures (as floats) in the order given.
    
    load_station_data(str) -> list[float]
    Precondition: The station files exists and is readable and in the correct format.
    
    """
    station_data=[]
    f=open(station+".txt",'r')
    for line in f:
        station_data.append(float(line[8:].strip()))
    f.close()
    return station_data

def load_all_stations_data(stations):
    """Return a list of the data for each station.

    Takes a list of stations and returns a list of the data for each station.
    
    load_all_stations_data(list[str]) -> list[list[float]]
    
    """
    data=[]
    for i in stations:
        data.append(load_station_data(i))
    return data
    
def display_maxs(stations, dates, data, start_date, end_date):
    """Display a table of maximum temperatures for given stations and date range.

    Takes in list of stations, list of dates, list of data, start&end dates
    and display a table of maximum temperatures for the given stations and the given date range.
    
    display_maxs(list[str], list[str], list[list[float], str, str) -> None
    Precondition: start_date <= end_date and they are in yyyymmdd format and are all in dates' range.
    
    """
    display_stations(stations, "Date")
    for i,d in enumerate(dates):                                   #i - index of date; d - the date
        if d>=start_date and d<=end_date:
            print("{:<12}".format(d), end='')
            for j, st in enumerate(stations):                      #j - index of station; st - name of station
                display_temp(data[j][i])
            print()

def temperature_diffs(data, dates, stations, station1, station2, start_date, end_date):
    """Return a list of pairs of dates and temperature differences on that date.

    Takes in list of data, list of dates, list of stations, two station names, start&end dates
    and returns a list of pairs of dates and temperatures between the temperatures for station1 and station2 on that date.

    temperature_diffs(list[list[float], list[str], list[str], str, str, str, str) -> list[(str, float)]
    Precondition: station1 and station2 are in the list of stations;
    start_date <= end_date and they are in yyyymmdd format and are all in dates' range.
    
    """
    st1=stations.index(station1)                                   #st1 - index of station1
    st2=stations.index(station2)                                   #st2 - index of station2
    diffs=[]
    for i,d in enumerate(dates):                                   #i - index of date; d - the date
        if d>=start_date and d<=end_date:
            if data[st1][i]!=UNKNOWN_TEMP and data[st2][i]!=UNKNOWN_TEMP:
                diff=data[st1][i]-data[st2][i]
                diffs.append((d,diff))
            else:
                diffs.append((d,UNKNOWN_TEMP))
    return diffs
            
def display_diffs(diffs, station1, station2):
    """Display each temperature differences of two stations.

    Takes in list of pairs of dates and temperature differences (produced by temperature_diffs ) and names of station1 and station2
    and displays the temperature differences between station1 and station2.

    display_diffs(list[(str, float)], str, str) -> None
    Precondition: station1 and station2 are the same as processed in temperature_diffs.
    
    """
    print("Temperature differences between",station1,"and",station2)
    print()
    print("{:<10}".format("Date"), end='')
    print("{:<15}".format("Temperature Differences"), end='')
    print()
    for i in diffs:
        print("{:<10}".format(i[0]), end='')
        display_temp(i[1])
        print()

def yearly_averages(dates, data, start_year, end_year):
    """Return the pair of the list of years and the yearly averages for each station.

    Takes in list of dates, list if data and the start&end years
    and returns the pair of the list of years and the yearly averages
    for each station whose data is given in data for the given range of years.

    yearly_averages(list[str], list[list[float], str, str) -> (list[str], list[list[float]])
    Precondition: start_year <= end_year and they are in yyyy format and are all in dates' range.
    
    """
    year_info=get_year_info(dates, start_year, end_year)
    years=year_info[0]
    indicies=year_info[1]
    indicies[len(years)]+=1                 #make the last year's end index into next year's start index(just as previous indexes)
    averages=[]
    for i, st in enumerate(data):           #i - index of station; st - station data
        st_average=[]
        for yr in years:
            yr_sum=0
            count=0
            for j in range(indicies[years.index(yr)], indicies[years.index(yr)+1]):         #j - index of date 
                if data[i][j]!=UNKNOWN_TEMP:
                    yr_sum+=data[i][j]
                    count+=1
            st_average.append(yr_sum/count) 
        averages.append(st_average)
    return(years, averages)

def display_yearly_averages(years, averages, stations):
    """Display a table of yearly average max temperatures for each given stations on each given year

    Takes in years and averages data produced by yearly_averages and list of stations
    and displays a table of yearly average max temperatures for each given stations on each given year.

    display_yearly_averages(list[str], list[list[float]], list[str]) -> None
    
    """
    display_stations(stations, "Year")
    for i, yr in enumerate(years):          #i - index of year; yr - the year
        print("{:<12}".format(yr), end='')
        for j, st in enumerate(stations):   #j - index of station; st - name of station
            display_temp(averages[j][i])
        print()
    
def interact():
    """Top-level function that defines the text-base user interface.

    The program first asks for a stations file (that lists the stations of interest)
    and then it enters a loop prompting for a command.
    commands:
        dm start date end date
            displays the maximum temperatures for each station for the supplied start date up to
            and including the end date.
        dd station1 station2 start date end date
            displays the differences of the maximum temperatures between the two stations for the given date range.
        ya start year end year
            displays the yearly average maximum temperatures for the given year range.
        q
            quits the program.
    For any unknown command or a command with wrong number of arguments, displays an error message.

    interact(None) -> None

""" 
    print("Welcome to BOM Data")
    print()
    file=input("Please enter the name of the Stations file: ")
    print()
    stations = load_stations(file)
    dates=load_dates(stations)
    data = load_all_stations_data(stations)
    while True:
        command=input("Command: ")
        command_s=command.strip().split(" ")                  #strip():in case of wrong argument number count caused by space at the end of the string
        if command_s[0]=="dm" and len(command_s)==3:
            print()
            display_maxs(stations, dates, data, command_s[1],command_s[2])
        elif command_s[0]=="dd" and len(command_s)==5:
            print()
            diffs = temperature_diffs(data, dates, stations, command_s[1],command_s[2], command_s[3],command_s[4])
            display_diffs(diffs, command_s[1],command_s[2])
        elif command_s[0]=="ya" and len(command_s)==3:
            print()
            years, averages = yearly_averages(dates, data, command_s[1],command_s[2])
            display_yearly_averages(years, averages, stations)
        elif command_s[0]=="q" and len(command_s)==1:
            return
        else:
            print("Unknown command: "+command)
        print()
    #pass


##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
