
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number:43792964
#
#   Student Name:Junchuan Xue
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here
CB_WIDTH=8

class TemperatureData(object):
    """
    A class for holding the temperature data for each loaded station,
    using a dictionary to store the data with the station names as keys
    and Station objects as values.
"""
    def __init__(self):
        """Create and initialise the object

        Constructor: TemperatureData(None)
        """
        self._st_data={}
        self._st_list=[]
        self._st_selected=[False,False,False,False,False,False,False,False]
        self._st_min_year=9999
        self._st_max_year=0
        self._st_min_temp=999.999
        self._st_max_temp=0.0
        
    def load_data(self, filename):
        """Loads in data from the given filename.

        load_data(str) -> None
        Precondition: filename is of the form "StationName.txt"
        """
        station=Station(filename)
        self._st_data[station.get_name()]=station
        self._st_list.append(station.get_name())
        self._st_selected[len(self._st_list)-1]=True
        
    def get_data(self):
        """Returns the dictionary of station data

        get_data() -> dict(str:obj)
        """
        return self._st_data      

    def toggle_selected(self, i):
        """toggles the flag for displaying the station at index i.

        toggle_selected(int) -> None
        """
        self._st_selected[i]= not self._st_selected[i]

    def is_selected(self, i):
        """Returns a boolean used to determine if the data for the station
        at index i is to be displayed.
        
        is_selected(int) -> bool
        """        
        return self._st_selected[i]

    def get_stations(self):
        """Returns the list of loaded station names in the order they were loaded.

        get_stations(None) -> list[str]
        """     
        return self._st_list

    def get_ranges(self):
        """Returns year range and temperature range for all loaded stations
        in a 4-tuple of the form (min_year, max_year, min_temp, max_temp).
        
        get_ranges(None) -> (int, int, float, float)
        """             
        for i in self._st_data.values():
            if self._st_min_year>i._min_year:
                self._st_min_year=i._min_year
            if self._st_max_year<i._max_year:
                self._st_max_year=i._max_year
            if self._st_min_temp>i._min_temp:
                self._st_min_temp=i._min_temp
            if self._st_max_temp<i._max_temp:
                self._st_max_temp=i._max_temp
        return (self._st_min_year,self._st_max_year,self._st_min_temp,self._st_max_temp)

    
class Plotter(tk.Canvas):
    """A customised Canvas that is responsible for doing the plotting."""
    def __init__(self, parent):
        """Create and initialise a canvas.

        Constructor: Plotter(tk.Widget)
        """
        super().__init__(parent)
        self._width=800
        self._height=340
        self.config(bg="white", width=self._width, height=self._height)


class SelectionFrame(tk.Frame):
    """A customised Frame widget used for selecting which stations data is to be displayed.
    It consists of a label and a Checkbutton for each loaded station.
    """
    def __init__(self, parent):
        """Create and initialise the widget.

        Constructor: SelectionFrame(tk.Widget)
        """
        super().__init__(parent)
        self._label=tk.Label(self, text="Station Selection: ",width=15,anchor=tk.W)
        self._label.pack(side=tk.LEFT)


class DataFrame(tk.Frame):
    """A customised Frame widget used for displaying the temperatures for
    a chosen year for each selected station.
    """
    def __init__(self,parent):
        """Create and initialise the widget.

        Constructor: DataFrame(tk.Widget)
        """
        super().__init__(parent)
        self._label0=tk.Label(self,text="",width=15,anchor=tk.W)
        self._label0.pack(side=tk.LEFT)
        self._label_list=[]
        for i in range(0,8):
            a=tk.Label(self,text="",fg=COLOURS[i],width=CB_WIDTH+3,padx=2)
            a.pack(side=tk.LEFT)
            self._label_list.append(a)                    


class TemperaturePlotApp(object):
    """Top-level class for the GUI. It is responsible for creating and
    managing instances of the above classes."""
    def __init__(self, master):
        """Create and initialise the app.

        Constructor: TemperaturePlotApp(Tk.BaseWindow)
        """
        #Create GUI objects
        master.title("Max Temperature Plotter")
        self._plotter=Plotter(master)
        self._plotter.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._selectframe=SelectionFrame(master)
        self._selectframe.pack(side=tk.BOTTOM,anchor=tk.W)   
        self._dataframe=DataFrame(master)
        self._dataframe.pack(side=tk.BOTTOM,anchor=tk.W)

        #Create data objects
        self._data=TemperatureData()
        self._coordinate=CoordinateTranslator(self._plotter._width,self._plotter._height,1,1,1,1)

        #Variables
        self._select_year=None
        self._year1=None
        self._year2=None
        self._fit_line=False
        self._new_line=False
        self._cb_list=[]
        self._file_list=[]

        #Events
        self._plotter.bind("<Configure>", self.config_event)
        self._plotter.bind("<Button-1>", self.plotter_click)
        self._plotter.bind("<B1-Motion>", self.plotter_click)
        self._plotter.bind_all("<Key>", self.plotter_press)

        #Create menu
        menubar=tk.Menu(master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Open",command=self.open_file)

    def open_file(self):
        """Provides a filedialog so that the user can choose a file to open.
        Uses the file to update TemperatureData object, labels and create check boxes.
        And uptate plotter using new coordinate and temperature data.

        open_file(None) -> None
        Precondition: the loaded file should be valid for get_data method and the data
        within the file should be sufficient for plotting lines.
        """
        filename = filedialog.askopenfilename()
        if filename:
            try:
                if len(self._data.get_stations())<8:
                    if filename not in self._file_list:
                        self._data.load_data(filename)
                        i=len(self._data.get_stations())-1
                        cb=tk.Checkbutton(self._selectframe,text=self._data.get_stations()[-1], \
                                          fg=COLOURS[i], width=CB_WIDTH, command=lambda: self.cb_click(i))
                        cb.select()
                        cb.pack(side=tk.LEFT)
                        self._cb_list.append(cb)
                        self.draw()
                        self.label_change()
                        self._file_list.append(filename)
                    else:
                        messagebox.showerror(title="File Error", message="{0} is already opened".format(filename))
                else:
                    messagebox.showerror(title="File Error", message="Already reached maximum file number")
                        
            except Exception: 
                messagebox.showerror(title="File Error", message="{0} is not a suitable data file".format(filename))

    def cb_click(self, i):
        """Toggles station select flag when user click a checkbutton with an index of i
        and redraw lines & update labels.

        cb_click(int) -> None
        """
        self._data.toggle_selected(i)
        self.draw()
        self.label_change()  

    def config_event(self,event):
        """Updates plotter width and height variables when user resize the window
        and redraw lines.

        config_event(tk.Event) -> None
        """        
        self._plotter._width=event.width
        self._plotter._height=event.height
        self.draw()

    def plotter_click(self, event):
        """Updates selected year variable when user click or drag within the plotter
        and redraw lines & update labels.

        plotter_click(tk.Event) -> None
        """
        if self._data.get_stations():
            self._select_year=self._coordinate.get_year(event.x)
            if self._select_year>self._data._st_max_year:       #Avoid out of range
                self._select_year=self._data._st_max_year
            if self._select_year<self._data._st_min_year:       #Avoid out of range
                self._select_year=self._data._st_min_year                
            self.label_change()
            self.draw()

    def plotter_press(self,event):
        """Updates best fit line year start year & end year variables when user press any key
        and redraw lines.

        plotter_press(tk.Event) -> None
        """
        if self._data.get_stations():
            if self._new_line==True and self._fit_line==False:
                self._year2=self._select_year
                self._fit_line=True
                self._new_line=False
                self.draw()             
            else:
                self._fit_line=False
                self._year1=self._select_year
                self._new_line=True
                self.draw()

    def label_change(self):
        """Updates labels according to selected year, selected flags and temperature data.

        label_change(None) -> None
        """     
        if self._select_year:
            self._dataframe._label0.config(text="Data for {0}: ".format(self._select_year))
            for i in range(0,8):
                if self._data.is_selected(i) \
                    and self._select_year>=self._data.get_data()[self._data.get_stations()[i]]._min_year \
                    and self._select_year<=self._data.get_data()[self._data.get_stations()[i]]._max_year:
                    self._dataframe._label_list[i].config(text="{:.3f}".format(self._data.get_data()[self._data.get_stations()[i]]._data[self._select_year]))
                else:
                    self._dataframe._label_list[i].config(text="")                

    def draw(self):
        """Updates plotter. Including erasing previous drawings, drawng temperature line
        and best line fit for each station, drawing selected year vertical line.

        draw(None) -> None
        """ 
        self._plotter.delete(tk.ALL)
        
        min_year=self._data.get_ranges()[0]
        max_year=self._data.get_ranges()[1]
        min_temp=self._data.get_ranges()[2]
        max_temp=self._data.get_ranges()[3]

        self._coordinate=CoordinateTranslator(self._plotter._width,self._plotter._height,min_year,max_year,min_temp,max_temp)

        for i,j in enumerate (self._data.get_stations()):
            if self._data.is_selected(i):
                line=[]
                points=self._data.get_data()[j].get_data_points()
                for k in points:
                    line.append(self._coordinate.temperature_coords(k[0],k[1]))
                self._plotter.create_line(line,fill=COLOURS[i])
                
                if self._fit_line==True:  
                    fit_points=[]
                    start=max(min(self._year1,self._year2),self._data.get_data()[j]._min_year)
                    end=min(max(self._year1,self._year2),self._data.get_data()[j]._max_year)
                    if start!=end:
                        for m in range(start,end+1):
                            fit_points.append(self._coordinate.temperature_coords(m,self._data.get_data()[j]._data[m]))
                        self._plotter.create_line(best_fit(fit_points),fill=COLOURS[i],width=2)

        if self._select_year:
            selected_point_x=self._coordinate.temperature_coords(self._select_year,1)[0]
            self._plotter.create_line([(selected_point_x,0),(selected_point_x,self._plotter._height)])
            
        if self._new_line==True:        #Draw a grey line to indicate user have set a "best fit line" start point
                    line_start_x=self._coordinate.temperature_coords(self._year1,1)[0]
                    self._plotter.create_line([(line_start_x,0),(line_start_x,self._plotter._height)],fill="lightgrey")    

##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
###################################################

def main():
    root = tk.Tk()
    app = TemperaturePlotApp(root)
    root.geometry("800x400")
    root.mainloop()

if __name__ == '__main__':
    main()
