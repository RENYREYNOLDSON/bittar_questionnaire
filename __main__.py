#######
#######
####### Python File for questionnaire software for Lucas Bittar 2024 reynoldson2002@gmail.com
#######
#######
#######
import customtkinter as tk
import pandas as pd
import os
from functools import partial

#FONTS
label_font = ("Arial",20)
question_font = ("Arial",50)
mid_font = ("Arial",30)


class DynamicLabel:
    def __init__(self,master,font,text):
        self.master = master
        self.font = font
        self.text = text

        self.frame = tk.CTkFrame(master=master,fg_color="transparent")

        self.max_chars = 40
        self.labels = []
        self.set_text(self.text)
        
    #Add all of the other texts with pack
    def pack(self):
        self.frame.pack(pady=(0,100))

    def small_pack(self):
        self.frame.pack(pady=(0,5))

    def pack_forget(self):
        self.frame.pack_forget()


    def set_text(self,text):
        #Reset previous
        for i in self.labels:
            i.pack_forget()
        self.labels = []
        self.text = text
        text = self.text.split(" ")

        new_label = ""
        for word in text:
            if len(str(new_label)+" "+str(word))<self.max_chars:
                new_label = str(new_label)+" "+str(word)
            else:
                lbl = tk.CTkLabel(master=self.frame,text=new_label,font=question_font)
                self.labels.append(lbl)
                new_label=""

        for i in self.labels:
            i.pack()

class Question:
    def __init__(self,title,q_type,options=None):
        self.title = title
        self.q_type = q_type
        self.score = 3
        self.options = options
        if self.options!=None:
            self.score=0

    def reset(self):
        self.score = 3
        if self.options!=None:
            self.score=0

class ButtonArrayFrame(tk.CTkFrame):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.options = []
        self.current = 0
        for i in range(8):
            q1 = tk.CTkButton(master=self,text="Placeholder",command=partial(self.select,i),hover=False)
            q1.pack(fill="x",expand=True,padx=100,pady=2)
            self.options.append(q1)

    def set_options(self,options):
        c=0
        for i in self.options:
            i.configure(text=options[c])
            c+=1
        
    def select(self,index):#['#3B8ED0', '#1F6AA5']
        self.current = index
        for i in range(len(self.options)):
            if i!=index:
                self.options[i].configure(fg_color='#1F6AA5')
            else:
                self.options[i].configure(fg_color='#809fff')

#Question Frame
class QuestionFrame(tk.CTkFrame):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.prev = None

        self.content_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.content_frame.place(relx=0.5,rely=0.5,anchor="center",relw=0.9)

        self.exit = tk.CTkButton(master=self,text="Exit",command=self.master.exit)
        self.exit.place(relx=0.02,rely=0.03,anchor="nw")

        #TITLE
        self.title = DynamicLabel(master=self.content_frame,font=question_font,text="")

        #SLIDER
        self.slider = tk.CTkSlider(master=self.content_frame,
                                   from_=1,
                                   to=5,
                                   number_of_steps=4,
                                   height=30,
                                   border_width=10)
        
        self.slider_labels = tk.CTkFrame(master=self.content_frame,height=20,fg_color="transparent")


        new = tk.CTkLabel(master=self.slider_labels,text="Discordo",anchor="center")
        new.place(rely=0.5,relx=0.055,anchor="w")
        new = tk.CTkLabel(master=self.slider_labels,text="Discordo fortemente",anchor="center")
        new.place(rely=0.5,relx=0.29,anchor="center")
        new = tk.CTkLabel(master=self.slider_labels,text="Neutro",anchor="center")
        new.place(rely=0.5,relx=0.5,anchor="center")
        new = tk.CTkLabel(master=self.slider_labels,text="Concordo",anchor="center")
        new.place(rely=0.5,relx=0.71,anchor="center")
        new = tk.CTkLabel(master=self.slider_labels,text="Concordo fortemente",anchor="center")
        new.place(rely=0.5,relx=0.97,anchor="e")

        #BUTTON ARRAY
        self.button_array_frame = ButtonArrayFrame(master=self.content_frame)



        #Submit and back
        self.submit = tk.CTkButton(master=self,text="Next",font=label_font,width=140,height=40,command=master.next)
        self.submit.place(relx=0.6,rely=0.9,anchor="center")
        self.back = tk.CTkButton(master=self,text="Back",font=label_font,width=140,height=40,command=master.back)
        self.back.place(relx=0.4,rely=0.9,anchor="center")

        self.indicator = tk.CTkLabel(master=self,text="0/33",font=label_font)
        self.indicator.place(relx=0.02,rely=0.98,anchor="sw")



    def render_question(self,question):
        #Do not redraw stuff if not needed, just set

        #Q1 and Q2
        if question.q_type=="slider":
            if self.prev=="slider":
                #configure
                self.title.set_text(question.title)
                self.slider.set(question.score)
            else:
                #redraw
                #Remove other objects
                self.button_array_frame.pack_forget()
                self.title.pack_forget()
                self.title.set_text(question.title)
                self.title.pack()
                self.slider_labels.pack(fill="x",expand=True)
                self.slider.set(question.score)
                self.slider.pack(fill="both",expand=False,padx=75)
                
        else:#Q3
            #Redraw
            self.button_array_frame.pack_forget()
            self.title.pack_forget()
            self.title.small_pack()
            self.title.set_text(question.title)
            self.slider_labels.pack_forget()
            self.slider.pack_forget()
            self.button_array_frame.set_options(question.options)
            self.button_array_frame.select(question.score)
            self.button_array_frame.pack(expand=True,fill="x")
        

        self.prev = question.q_type

    def get_score(self):
        if self.prev=="slider":
            return int(self.slider.get())
        else:
            return int(self.button_array_frame.current)


#Landing Frame
class LandingFrame(tk.CTkFrame):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)



        self.info_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.info_frame.place(relx=0.5,rely=0.5,anchor="center")


        self.load_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.load_frame.place(relx=0.05,rely=0.46,anchor="w",relh=0.8,relw=0.2)
        load_label = tk.CTkLabel(master=self.load_frame,text="Load",font=label_font,anchor="w")
        load_label.pack(fill="x",padx=20,pady=5)
        self.scroll_frame = tk.CTkScrollableFrame(master=self.load_frame)
        self.scroll_frame.pack(fill="both",expand=True)

        self.id_label = tk.CTkLabel(master=self.info_frame,text="Unique Code",anchor="w",font=label_font)
        self.id_label.pack(fill="x",expand=True,pady=(0,5))
        self.id = tk.CTkEntry(master=self.info_frame,placeholder_text="Unique Code",width=300)
        self.id.pack(pady=(0,20))

        self.name_label = tk.CTkLabel(master=self.info_frame,text="Name",anchor="w",font=label_font)
        self.name_label.pack(fill="x",expand=True,pady=(0,5))
        self.name = tk.CTkEntry(master=self.info_frame,placeholder_text="Name",width=300)
        self.name.pack(pady=(0,20))


        self.start = tk.CTkButton(master=self.info_frame,text="Start",font=label_font,width=140,height=40,command=master.start)
        self.start.pack()


        ##OPEN QUESTIONS BUTTON
        self.open_questions = tk.CTkButton(master=self,text="⏎ Open Questions File",fg_color="transparent",font=label_font,hover=False,command=self.master.open_file)
        self.open_questions.place(relx=0.02,rely=0.98,anchor="sw")

    def reload_previous(self):
        for c in self.scroll_frame.winfo_children():
            c.destroy()
        #Open saves
        file = os.path.join(os.path.dirname(__file__),"results.xlsx")
        df = pd.read_excel(file,dtype={'ID': str,"name":str})

        #Add buttons
        for index,row in df.iterrows():
            new_button = tk.CTkButton(master=self.scroll_frame,
                                      text=str(row["id"])+" "+str(row["name"]),
                                      fg_color="transparent",
                                      corner_radius=0,
                                      command=partial(self.master.load,row))
            new_button.pack(fill="x")

            #self.scroll_frame


class ResultsFrame(tk.CTkFrame):
    #CONSTRUCTOR 
    def __init__(self,master, results,**kwargs):
        super().__init__(master, **kwargs)

        self.options_frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.options_frame.place(relx=0.02,rely=0.03,anchor="nw")
        #Add buttons
        self.exit = tk.CTkButton(master=self.options_frame,text="Exit",command=self.master.exit)
        self.exit.pack(pady=(0,10))
        self.restart = tk.CTkButton(master=self.options_frame,text="Back to Start",command=self.master.restart)
        self.restart.pack(pady=(0,10))
        self.backb = tk.CTkButton(master=self.options_frame,text="Back",command=self.back)
        self.backb.pack(pady=(0,10))
        self.save = tk.CTkButton(master=self.options_frame,text="Save",command=self.master.save,state="disabled")
        self.save.pack(pady=(0,5))

        self.frame = tk.CTkFrame(master=self,fg_color="transparent")
        self.frame.place(relx=0.5,rely=0.5,anchor="center")
        #Title of q1
        #QUESTIONNAIRE 1
        q1_title = tk.CTkLabel(master=self.frame,font=mid_font,text=results["Q1_title"])
        q1_title.pack(pady=(20,0))
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q1_S1_title"])
        q1_s1.pack()
        self.q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q1_s1.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q1_S2_title"])
        q1_s1.pack()
        self.q1_s2 = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q1_s2.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q1_ratio_title"])
        q1_s1.pack()
        self.q1_ratio = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q1_ratio.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q1_result_text"])
        q1_s1.pack()
        self.q1_result = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q1_result.pack()

        #QUESTIONNAIRE 2
        q1_title = tk.CTkLabel(master=self.frame,font=mid_font,text=results["Q2_title"])
        q1_title.pack(pady=(10,0))
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q2_S1_title"])
        q1_s1.pack()
        self.q2_s1 = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q2_s1.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q2_S2_title"])
        q1_s1.pack()
        self.q2_s2 = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q2_s2.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q2_ratio_title"])
        q1_s1.pack()
        self.q2_ratio = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q2_ratio.pack()
        q1_s1 = tk.CTkLabel(master=self.frame,font=label_font,text=results["Q2_result_text"])
        q1_s1.pack()
        self.q2_result = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q2_result.pack()


        q3_title = tk.CTkLabel(master=self.frame,font=mid_font,text=results["Q3_title"])
        q3_title.pack(pady=(10,0))
        self.q3_result = tk.CTkLabel(master=self.frame,font=label_font,text="empty",text_color="#ADD8E6")
        self.q3_result.pack()

    #Add the values
    def fill_values(self,values):
        self.q1_s1.configure(text=str(values["Q1_S1_score"]))
        self.q1_s2.configure(text=str(values["Q1_S2_score"]))
        self.q1_ratio.configure(text=str(round(values["Q1_ratio"],3)))
        self.q1_result.configure(text=str(values["Q1_score"]))

        self.q2_s1.configure(text=str(values["Q2_S1_score"]))
        self.q2_s2.configure(text=str(values["Q2_S2_score"]))
        self.q2_ratio.configure(text=str(round(values["Q2_ratio"],3)))
        self.q2_result.configure(text=str(values["Q2_score"]))

        self.q3_result.configure(text=str(values["Q3_score"]))

    def back(self):
        #return to last question
        self.master.current_q=33
        self.master.back()


#Main Tkinter Window

class App(tk.CTkToplevel):
    #CONSTRUCTOR 
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.QUESTIONS,self.RESULT_INFO = open_questions()
        self.current_q = 0
        self.id=0
        self.name=""

        self.minsize(1300,700)
        self.title("Questionnaire Tool")
        self.state("zoomed")

        self.landing_frame = LandingFrame(master=self)
        self.landing_frame.reload_previous()
        self.landing_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)


        self.results_frame = ResultsFrame(master=self,results=self.RESULT_INFO)
        self.question_frame = QuestionFrame(master=self)

    def start(self):
        #Start the quiz
        name = self.landing_frame.name.get()
        id = self.landing_frame.id.get()
        if name!="" and id!="":
            self.name = str(name)
            self.id = str(id)
            self.title("Questionnaire Tool - "+self.id+" "+self.name)
        else:
            return
        
        #Add quiz frame
        self.render_question()
        self.question_frame.indicator.configure(text=str(self.current_q+1)+"/33")
        self.question_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)

        self.landing_frame.place_forget()

    def next(self):
        #Save previous
        self.QUESTIONS[self.current_q].score = self.question_frame.get_score()
        self.current_q+=1
        self.question_frame.indicator.configure(text=str(self.current_q+1)+"/33")
        self.render_question()

    def back(self):
        #Save previous
        if self.current_q==33:
            self.current_q-=1
            self.question_frame.indicator.configure(text=str(self.current_q+1)+"/33")
            self.render_question()
            self.question_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)
            self.results_frame.place_forget()
        else:
            self.QUESTIONS[self.current_q].score = self.question_frame.get_score()
            self.current_q-=1
            self.question_frame.indicator.configure(text=str(self.current_q+1)+"/33")
            self.render_question()

    #FIrst 8
    def add_scores(self,s,e):
        #Add up first 8
        total = 0
        c=0
        for i in range(s,e):
            total+=self.QUESTIONS[i].score
            c+=1
        return total
    
    #Submit the questions
    def submit(self,skip=False):
        #CALCULATE RESULTS
        if skip==False:
            self.QUESTIONS[self.current_q].score = self.question_frame.get_score()
            self.results_frame.save.configure(state="normal")
        Q1_S1_score = self.add_scores(0,8)
        Q1_S2_score = self.add_scores(8,16)
        Q1_ratio = Q1_S1_score/Q1_S2_score
        if Q1_ratio>=2:
            Q1_score = self.RESULT_INFO["Q1_scores"][4]
        elif Q1_ratio>1.25:
            Q1_score = self.RESULT_INFO["Q1_scores"][3]
        elif Q1_ratio>=0.75:
            Q1_score = self.RESULT_INFO["Q1_scores"][2]
        elif Q1_ratio>0:
            Q1_score = self.RESULT_INFO["Q1_scores"][1]
        else:
            Q1_score = self.RESULT_INFO["Q1_scores"][0]

        Q2_S1_score = self.add_scores(16,24)
        Q2_S2_score = self.add_scores(24,32)
        Q2_ratio = Q2_S1_score/Q2_S2_score
        if Q2_ratio>=2:
            Q2_score = self.RESULT_INFO["Q2_scores"][4]
        elif Q2_ratio>1.25:
            Q2_score = self.RESULT_INFO["Q2_scores"][3]
        elif Q2_ratio>=0.75:
            Q2_score = self.RESULT_INFO["Q2_scores"][2]
        elif Q2_ratio>0:
            Q2_score = self.RESULT_INFO["Q2_scores"][1]
        else:
            Q2_score = self.RESULT_INFO["Q2_scores"][0]

        Q3_score = self.RESULT_INFO["Q3_scores"][self.QUESTIONS[-1].score]
        
        #Add all s1
        self.VALUES = {"name":self.name,
                       "id":self.id}



        
        #ADD the individual answers:
        for i in range(0,16):
            self.VALUES["Q1 Question "+str(i+1)] = self.QUESTIONS[i].score

        self.VALUES["Q1_S1_score"]=Q1_S1_score
        self.VALUES["Q1_S2_score"]=Q1_S2_score
        self.VALUES["Q1_ratio"]=Q1_ratio
        self.VALUES["Q1_score"]=Q1_score

        c=0
        for i in range(16,32):
            self.VALUES["Q2 Question "+str(c+1)] = self.QUESTIONS[i].score
            c+=1

        self.VALUES["Q2_S1_score"]=Q2_S1_score
        self.VALUES["Q2_S2_score"]=Q2_S2_score
        self.VALUES["Q2_ratio"]=Q2_ratio
        self.VALUES["Q2_score"]=Q2_score
            
        self.VALUES["Q3"] = self.QUESTIONS[-1].score

        self.VALUES["Q3_score"]=Q3_score



        self.results_frame.fill_values(self.VALUES)
        #PLACE RESULTS FRAME
        self.results_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)
        self.landing_frame.place_forget()
        self.question_frame.place_forget()

    def render_question(self):
        #Get current question
        question = self.QUESTIONS[self.current_q]
        #Set the question in the frame
        self.question_frame.render_question(question)

        #Enable/disable buttons
        if self.current_q==0:
            self.question_frame.back.configure(state="disabled")
        else:
            self.question_frame.back.configure(state="normal",hover=True)

        if self.current_q==32:
            self.question_frame.submit.configure(text="Submit",command=self.submit)
        else:
            self.question_frame.submit.configure(text="Next",command=self.next)

    def exit(self):
        #Return to landing page!
        self.landing_frame.name.delete(0,"end")
        self.landing_frame.id.delete(0,"end")
        self.QUESTIONS,self.RESULT_INFO = open_questions()
        self.id=0
        self.name=""
        self.current_q = 0
        self.landing_frame.reload_previous()
        self.landing_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)
        self.question_frame.place_forget()
        self.results_frame.place_forget()

    def open_file(self):
        file = os.path.join(os.path.dirname(__file__),"questions.xlsx")
        os.startfile(file)

    def save(self):
        #SAVES TO THE RESULTS FILE UNDER THIS UNIQUE ID AND NAME
        #IF ALREADY IN THERE THEN REPLACE
        file = os.path.join(os.path.dirname(__file__),"results.xlsx")
        df = pd.read_excel(file,dtype={'id': str,"name":str})

        new_row = self.VALUES
        if df.empty:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(file, index=False)

        else:
            # Create a boolean mask where both 'ID' and 'Name' match the new row
            mask = (df['id'] == new_row['id']) & (df['name'] == new_row['name'])


            # Check if the combination of ID and Name already exists in the DataFrame
            if mask.any():
                # Replace the existing row
                df.loc[mask, :] = list(new_row.values())
            else:
                # Append the new row
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save the modified DataFrame back to the Excel file
            df.to_excel(file, index=False)

        self.results_frame.save.configure(state="disabled")


    def load(self,data):
        #SET ALL VARIABLES USING THE PROVIDED DATA
        self.QUESTIONS,self.RESULT_INFO = open_questions()

        self.name = str(data["name"])
        self.id = str(data["id"])
        self.title("Questionnaire Tool - "+self.id+" "+self.name)

        #Q1's
        q1 = data.iloc[2:18].tolist()
        for i in range(0,16):
            self.QUESTIONS[i].score = q1[i]
        #Q2's
        q2 = data.iloc[22:38].tolist()
        for i in range(0,16):
            self.QUESTIONS[i+16].score = q2[i]
        #Q3's
        q3 = int(data.iloc[42])
        self.QUESTIONS[32].score = q3

        self.submit(skip=True)

    #Return to the first value
    def restart(self):
        self.question_frame.place(anchor="center",relx=0.5,rely=0.5,relw=0.92,relh=0.9)
        self.results_frame.place_forget()
        #Save previous
        self.current_q = 0
        self.question_frame.indicator.configure(text=str(self.current_q+1)+"/33")
        self.render_question()



#Return a list of all of the questions!
def open_questions():
    #Read the CSV
    # Specify the path to your Excel file
    file_path = os.path.join(os.path.dirname(__file__),"questions.xlsx")

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Display the first few rows of the dataframe
    Q1 = df.iloc[1:17,1]
    Q2 = df.iloc[19:35,1]

    Q3 = df.iloc[38:46,1]
    #Get the data
    questions = []
    for q in Q1:
        questions.append(Question(q,"slider"))
    for q in Q2:
        questions.append(Question(q,"slider"))

    questions.append(Question(Q3.tolist()[0],"option",options=Q3.tolist()))


    #Result data:
    result_info = {
        "Q1_title":df.iloc[0,1],
        "Q1_S1_title":df.iloc[0,3],
        "Q1_S2_title":df.iloc[0,4],
        "Q1_ratio_title":df.iloc[0,5],
        "Q1_result_text":df.iloc[0,8],
        "Q1_scores":df.iloc[1:6,8].tolist(),
        "Q2_title":df.iloc[18,1],
        "Q2_S1_title":df.iloc[18,3],
        "Q2_S2_title":df.iloc[18,4],
        "Q2_ratio_title":df.iloc[18,5],
        "Q2_result_text":df.iloc[18,8],
        "Q2_scores":df.iloc[19:24,8].tolist(),
        "Q3_title":df.iloc[36,1],
        "Q3_scores":df.iloc[38:46,8].tolist()

    }

    #Return the data
    return questions,result_info


#ROOT UTILITY FUNCTION
def check_windows_open():
    c=0
    for w in root.winfo_children():
        c+=1
    if c==0:#Destroy root if no windows left open
        print("ROOT CLOSED AS NO WINDOWS DETECTED")
        root.destroy()
    root.after(1000,check_windows_open)


if __name__ == "__main__":
    #Create main tkinter window

    root=tk.CTk()
    root.withdraw()
    root.after(1000,check_windows_open)
    app = App(root)
    app.mainloop()



#Test, mainly if value ranges etc are correct
#Package and send
