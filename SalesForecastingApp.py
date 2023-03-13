from tkinter import *
from tkinter import messagebox, filedialog, messagebox, ttk
from PIL import ImageTk, Image
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#new
# Data and Starting App
data = {
    'Months': ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'Year_Sales_2021': ['-','-','-','-','-','-','-','-','-','-','-','-'],
    #for MAD error calculations
    '2022_Actual_Sales': ['-','-','-','-','-','-','-','-','-','-','-','-']
}
df = pd.DataFrame(data= data)

root = Tk()
root.title("Sales Forecasting Device")

Title_Label = Label(root, bg="gray", padx=90, text="Sales Forecasting Device")
Title_Label.grid(row=0, column=0, columnspan = 5)

Window_Size_After_Inputs = "975x560"

#Global Frames (put here so that it can be errased off the tab if needed)
Input_Sales_Frame = LabelFrame(root, pady= 6, padx=15)
Input_Error = Label(Input_Sales_Frame, text="Input all fields as correct number \n(not a string or a negative number)", fg="red", bg="lightgray")
Empty_Label = Label(Input_Sales_Frame, text="")
Naive_Frame = LabelFrame(root, pady= 6, padx=15)
MA_Frame = LabelFrame(root, pady= 6, padx=15)


Display_Data_Frame = LabelFrame(MA_Frame, text="Data Display")
Graph_Comparison_Button = Button(MA_Frame, text="Graph Real 2022 vs Forecasted 2022 Data", bg="lightblue", command= lambda: MACompareGraph()) 
MA_MAD_Label = Label(MA_Frame, text= "edit this down below", font= ('Helvetica 13 underline'))
tv2 = ttk.Treeview(Display_Data_Frame, height = 12)


############################################################################
NavBar_Frame = LabelFrame(root)
#Displays select forecast text only when no forecast option is selected
Select_Option_Label = Label(NavBar_Frame, text="Please Select One of the Above Forecasting Options", pady=30, font= ('Helvetica 13 bold'))
def NavBarSection():
    NavBar_Frame.grid(row=1, column=0, columnspan = 5)
    #Makes Navbar Buttons
    Input_Sales_Button = Button(NavBar_Frame, text= "Reset Inputs", width=23, command= lambda: [InputSalesSection()])
    Naive_Forecast = Button(NavBar_Frame, text= "Naive", width=23, command= NaiveSection)
    MA_Forecast = Button(NavBar_Frame, text= "Moving Average", width=23, command= MASection)
    #Display it
    Input_Sales_Button.grid(row=1, column=0)
    Naive_Forecast.grid(row=1, column=1)
    MA_Forecast.grid(row=1, column=2)
    
    #displays select forecast text
    Select_Option_Label.grid(row= 20, column= 0, columnspan = 5)

############################################################################
def InputSalesSection():
    #hides anything that isnt for this tab from the screen
    Input_Error.grid_forget()
    Empty_Label.grid_forget()
    Select_Option_Label.grid_forget()
    Naive_Frame.grid_forget()
    MA_Frame.grid_forget()
    
    # changes size of window after inputing data first time
    window_size_after = "590x160"
    if root.geometry().split('+')[0] == window_size_after:
        root.geometry(Window_Size_After_Inputs)
    
    #Input Sales Section
    Input_Sales_Title_Label = Label(Input_Sales_Frame, text="Input every Month's Sales", font= ('Helvetica 10 underline'))
    Input_Sales_Frame.grid(row=2,column=0, columnspan = 5)
    Input_Sales_Title_Label.grid(row=0, column=0, columnspan = 5)
    Input_Sales_2021_Label = Label(Input_Sales_Frame, text="2021 (for forecasting)")
    Input_Sales_2022_Label = Label(Input_Sales_Frame, text="2022 (for MAD)")
    Input_Sales_2021_Label.grid(row=1, column=1, columnspan = 1)
    Input_Sales_2022_Label.grid(row=1, column=2, columnspan = 2)
    ##########################################
        #Input Texts Section
    rowStart = 1
    columnStart = 0
    d_2021 = {}
    d_2022 = {}

    for i in range(len(df["Months"])):

        rowStart = rowStart + 1
        #2021 Inputs
        Months_Label = Label(Input_Sales_Frame, text= df["Months"][i], padx=20)
        Months_Label.grid(row= rowStart+1, column = columnStart)

        d_2021["Months_2021_Input{0}".format(i)] = Entry(Input_Sales_Frame)
        d_2021["Months_2021_Input{0}".format(i)].grid(row= rowStart+1, column = columnStart+1)

        #2022 Inputs
        d_2022["Months_2022_Input{0}".format(i)] = Entry(Input_Sales_Frame)
        d_2022["Months_2022_Input{0}".format(i)].grid(row= rowStart+1, column = columnStart+2)
    ##########################################
    #Submit Section
    
    #choose CSV File
    CSV_File_Name = Label(Input_Sales_Frame ,text="No File Selected")
    def ChooseCSVFile():
        Input_Sales_Frame.filename = filedialog.askopenfilename(initialdir="/C", title="Select CSV File", filetypes=(("CSV Files", "*.csv"),))
        CSV_File_Name["text"] = Input_Sales_Frame.filename
        global File_Path
        File_Path = CSV_File_Name["text"]
        
        #try to read CSV file
        try:
            CSV_Filename = r"{}".format(File_Path)
            global df
            df = pd.read_csv(File_Path)
            df.columns= ["Months", "Year_Sales_2021", "2022_Actual_Sales"]
            months = ['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            for i in range(len(months)):
                df["Months"][i] = months[i]
            
            #checks if values are integers and valid or not
            try:
                for i in range(len(df["Year_Sales_2021"])):
                    float(df["Year_Sales_2021"][i])
                    float(df["2022_Actual_Sales"][i])
                
                Submit_Sales = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
                if Submit_Sales == "ok":
                    root.geometry(window_size_after)
                    NavBarSection()
                    Input_Sales_Frame.grid_forget()
                    
                    #Remove TreeView after changing data
                    Display_Data_Frame.grid_forget()
                    MA_MAD_Label.grid_forget()
                    Graph_Comparison_Button.grid_forget()
                    
            except ValueError:
                Empty_Label.grid(row= 15, column=0, columnspan = 3)
                #displays input error
                Input_Error.config(text="The data inside the CSV is not valid \n (Make sure the data are numbers)")
                Input_Error.grid(row= 16, column=0, columnspan = 3)

                #only changes size of window if its first section of app
                if root.geometry().split('+')[0] == "503x523":
                    root.geometry("503x593")
                else:
                    root.geometry("975x630")
                
        except ValueError:
            #displays Image
            Error_Image = ImageTk.PhotoImage(Image.open("formatExample.jpg"))
            Image_Window = Toplevel()
            Image_Window.wm_transient(root)
            x = root.winfo_x()
            y = root.winfo_y()
            Image_Window.geometry("+%d+%d" % (x + 100, y + 200))
            Error_Image_Label = Label(Image_Window, image= Error_Image)
            Error_Image_Label.pack()
            
            #displays error
            Error_Message = messagebox.showerror("Submission Unsuccessful", "Make sure the CSV File only has 3 Columns with a title and the data similar to this format in the newly opened window")
            if Error_Message == "ok":
                Image_Window.destroy()
                Empty_Label.grid(row= 15, column=0, columnspan = 3)
                #displays input error
                Input_Error.config(text= " The file you have entered is not valid")
                Input_Error.grid(row= 16, column=0, columnspan = 3)
                
                #only changes size of window if its first section of app
                if root.geometry().split('+')[0] == "503x523":
                    root.geometry("503x593")
                    
        except FileNotFoundError:
            Empty_Label.grid(row= 15, column=0, columnspan = 3)
            #displays input error
            Input_Error.config(text= " Could not find File, please try again")
            Input_Error.grid(row= 16, column=0, columnspan = 3)
            
            #only changes size of window if its first section of app
            if root.geometry().split('+')[0] == "503x523":
                root.geometry("503x593")
            else:
                root.geometry("975x630")
        
    def skip():
        Submit_Sales = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
        if Submit_Sales == "ok":
            root.geometry(window_size_after)
            NavBarSection()
            df["Year_Sales_2021"] = np.random.randint(1,200, size=len(df))
            df["2022_Actual_Sales"] = np.random.randint(1,200, size=len(df))
            Input_Sales_Frame.grid_forget()
            
            #Remove TreeView after changing data
            Display_Data_Frame.grid_forget()
            MA_MAD_Label.grid_forget()
            Graph_Comparison_Button.grid_forget()

    #Validates Inputs of Sales if its integer and Submits if successful
    def SaleSubmit():
        try:
            for i in range(len(df["Year_Sales_2021"])):
                Months_Input_Getter_2021 = (d_2021["Months_2021_Input{0}".format(i)]).get()
                Months_Input_Getter_2022 = (d_2022["Months_2022_Input{0}".format(i)]).get()
                df["Year_Sales_2021"][i] = float(Months_Input_Getter_2021)
                df["2022_Actual_Sales"][i] = float(Months_Input_Getter_2022)

            #Submit successsful window
            Submit_Sales = messagebox.showinfo("Submission Successful", "The data has been submitted successfully")
            if Submit_Sales == "ok":
                root.geometry(window_size_after)
                NavBarSection()
                Input_Sales_Frame.grid_forget()
                
                #Remove TreeView after changing data
                Display_Data_Frame.grid_forget()
                MA_MAD_Label.grid_forget()
                Graph_Comparison_Button.grid_forget()

        except ValueError:
            Empty_Label.grid(row= 15, column=0, columnspan = 3)
            #displays input error
            Input_Error.grid(row= 16, column=0, columnspan = 3)
            
            #only changes size of window if its first section of app
            if root.geometry().split('+')[0] == "503x523":
                root.geometry("503x593")
            else:
                root.geometry("975x630")

#         return Months_Input_Getter_2021, Months_Input_Getter_2022, Submit_Sales

    #Actual Displays
    Choose_CSV_Label = Label(Input_Sales_Frame, text="Or")
    Choose_CSV_Label.grid(row= 18, column=0, columnspan = 3)
    Choose_CSV_Button = Button(Input_Sales_Frame, text="Choose Select CSV File", command= ChooseCSVFile)
    Choose_CSV_Button.grid(row= 19, column=0, columnspan = 3)
    
    #Or Random Assortment of numbers
    skip_Label = Button(Input_Sales_Frame, text="Skip Inputting Data", bg="lightblue", command = skip)
    skip_Label.grid(row= 20, column=0, pady=10)
    
    #Submit Button
    Submit_Button = Button(Input_Sales_Frame, text="Submit", bg="lightgreen", command=SaleSubmit)
    Submit_Button.grid(row= 20, column=2, columnspan=2)
    
#displays it at start of app
InputSalesSection()
############################################################################
#Naive section
def NaiveSection():
    root.geometry(Window_Size_After_Inputs)
    #removes anything that isnt for this tab from the screen
    Input_Error.grid_forget()
    Select_Option_Label.grid_forget()
    Input_Sales_Frame.grid_forget()
    MA_Frame.grid_forget()
    
    df["Naive_Forcast"] = df["Year_Sales_2021"]
    #MAD Calculation
    error_df = df.copy()
    error_df["Naive_Error"] = (df["2022_Actual_Sales"] - df["Naive_Forcast"]).abs()
    Naive_MAD = error_df["Naive_Error"].mean()
    
    #Naive Frame
    Naive_Frame.grid(row= 2, column= 0, columnspan= 5)
    
    #frame for TreeView
    Display_Data_Frame = LabelFrame(Naive_Frame, text="Data Display")
    Display_Data_Frame.grid(row= 2, column= 0, columnspan= 5)

    #TreeView Widget
    tv1 = ttk.Treeview(Display_Data_Frame, height = 12)
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["column"]:
        tv1.heading(column, text = column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values= row)
    tv1.grid(row= 100, column= 0)
    
    Empty_Label = Label(Naive_Frame, text=" ")
    Empty_Label.grid(row=3, column= 0, columnspan= 5)
    #   Graphing and MAD Labels                  lambda used to run function later when running to it (throwaway function)
    Graph_Comparison_Button = Button(Naive_Frame, text="Graph Real 2022 vs Forecasted 2022 Data", bg="lightblue", command= lambda: NaiveCompareGraph()) 
    Naive_MAD_Label = Label(Naive_Frame, text= f"Naive MAD: {Naive_MAD}", font= ('Helvetica 13 underline'))
    Naive_MAD_Label.grid(row=4, column= 0)
    Graph_Comparison_Button.grid(row=4, column= 3)
    def NaiveCompareGraph():
        #Naive Compare
        x= np.array([0,1,2,3,4,5,6,7,8,9,10,11])

        plt.figure(figsize=(10,5), dpi=100)
        plt.plot(error_df["2022_Actual_Sales"], marker=".", markersize="12", markeredgecolor="blue", label="Actual Sales 2022")
        plt.plot(error_df["Naive_Forcast"], marker=".", markersize="12", markeredgecolor="orange", label="Naive Forecasting")
        plt.xticks(x, error_df["Months"], rotation=50)

        plt.title("Actual Sales of 2022 vs Naive Forecasted", fontdict={"fontsize": 15})
        plt.xlabel("Month")
        plt.ylabel("Sales")
       
        plt.legend(bbox_to_anchor=(0.85, 1.1), loc='upper left', borderaxespad=0)


        plt.show()
        
    #when done delete Naive_forecast column
    del df["Naive_Forcast"]
############################################################################
#Moving Average Section
def MASection():
    
    root.geometry("1041x560")
    #removes anything that isnt for this tab from the screen
    Select_Option_Label.grid_forget()
    Input_Sales_Frame.grid_forget()
    Naive_Frame.grid_forget()
    
    #MA Frame
    MA_Frame.grid(row= 2, column= 0, columnspan= 5)
    
    #MA Month amount input
    MA_Month_Amount_Label = Label(MA_Frame, text= "Enter the number of Months to be Averaged: ")
    MA_Month_Amount_Label.grid(row = 3, column = 0)
    MA_Month_Amount_Input = Entry(MA_Frame)
    MA_Month_Amount_Input.grid(row = 3, column = 1)
    MA_Val_Submit = Button(MA_Frame, text="Submit", command= lambda: ValidateMA())
    MA_Val_Submit.grid(row = 4, column= 0, columnspan=5)
    
    #Validates Input
    def ValidateMA():
        try:
            MA_Error_Message = Label(MA_Frame, text="Edit this depending on situation", fg="red", bg="lightgray")
            MA_Val = MA_Month_Amount_Input.get()
            MA_Val = int(MA_Val)
            if MA_Val >= 12:
                MA_Error_Message.config(text="Please enter a value between 1-12")
                MA_Error_Message.grid(row=2, column = 0, columnspan= 5)
            #Calculation
            #copy to keep original safe
            MA_df = df.copy()
            
            MA_df["MA_Forecast"] = MA_df["Year_Sales_2021"].rolling(window=MA_Val).mean()
            MA_df["MA_Forecast"] = MA_df["MA_Forecast"].shift(1)
            MA_df["MA_Error"] = (MA_df["2022_Actual_Sales"] - MA_df["MA_Forecast"]).abs()
            MA_MAD = MA_df["MA_Error"].mean()
            
            #frame for TreeView
            Display_Data_Frame.grid(row= 0, column= 0, columnspan= 5)
            #TreeView Widget
            
            tv2.delete(*tv2.get_children())
            
            tv2["column"] = list(MA_df.columns)
            tv2["show"] = "headings"
            for column in tv2["column"]:
                tv2.heading(column, text = column)

            MA_df_rows = MA_df.to_numpy().tolist()
            for row in MA_df_rows:
                tv2.insert("", "end", values= row)
            tv2.grid(row= 100, column= 0)
            
            
            #Buttons After validation

            MA_MAD_Label.config(text= f"Moving Average MAD: {MA_MAD}")
            MA_MAD_Label.grid(row=5, column= 0)
            Graph_Comparison_Button.grid(row=5, column= 3)
            
            global MACompareGraph
            def MACompareGraph():
                #Moving Average Forecasting Graph
                x= np.array([0,1,2,3,4,5,6,7,8,9,10,11])

                plt.figure(figsize=(10,5), dpi=100)
                plt.plot(MA_df["2022_Actual_Sales"], marker=".", markersize="12", markeredgecolor="blue", label="Actual Sales 2022")
                plt.plot(MA_df["MA_Forecast"], marker=".", markersize="12", markeredgecolor="orange", label=" MA Forecast")
                plt.xticks(x,df.Months, rotation=50)

                plt.title(f"Actual Sales of 2022 vs {str(MA_Val)} Month MA Forecasted", fontdict={"fontsize": 15})
                plt.xlabel("Month")
                plt.ylabel("Sales")
                plt.legend()
                plt.legend(bbox_to_anchor=(0.85, 1.1), loc='upper left', borderaxespad=0)

                plt.show()
                
        except ValueError:
            MA_Error_Message.config(text="Please Enter an Integer Input")
            MA_Error_Message.grid(row=2, column = 0, columnspan= 5)
            
############################################################################
root.geometry("503x523")
root.mainloop()