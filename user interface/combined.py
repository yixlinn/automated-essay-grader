import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import re
import joblib

# grading functions

# loading the model that's been trained previously
model = joblib.load('model.pkl')

# function to count the number of syllables in a word
def count_syllables(word):
    vowels = 'aeiouAEIOU'
    syllable_count = 0
    previous_char_is_vowel = False

    for char in word:
        if char in vowels:
            if not previous_char_is_vowel:
                syllable_count += 1
            previous_char_is_vowel = True
        else:
            previous_char_is_vowel = False

    if word.endswith('e') and len(word) > 1 and word[-2] not in vowels:
        syllable_count -= 1

    return max(1, syllable_count)

# function to calculate the Flesch-Kincaid readability score
def calculate_readability(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    
    if sentence_count == 0:
        return 0
    
    average_length = total_words / sentence_count
    words = text.split()
    total_syllables = sum(count_syllables(word) for word in words)
    average_syllable = total_syllables / total_words
    
    readability_score = 206.835 - (1.015 * average_length) - (84.6 * average_syllable)
    return readability_score

# function to calculate the average sentence length
def calculate_average_sentence_length(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    
    if sentence_count == 0:
        return 0
    
    average_length = total_words / sentence_count
    return average_length

# function to calculate the average word length
def calculate_average_word_length(text):
    text = re.sub(r'[^\w\s\'-]', '', text)
    words = text.split()
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    average_word_length = total_characters / total_words
    return average_word_length

# function to calculate the word count
def calculate_word_count(text):
    word_count = len(text.split())
    return word_count

# function to calculate the sentence count
def calculate_sentence_count(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    return sentence_count

def grade_essay(text):
    features = {
        'word_count': calculate_word_count(text),
        'sentence_count': calculate_sentence_count(text),
        'average_word_length': calculate_average_word_length(text),
        'average_sentence_length': calculate_average_sentence_length(text),
        'flesch_kincaid_score': calculate_readability(text)
    }
     # converting into a DataFrame
    input_df = pd.DataFrame([features])

    # predicting the score using the model
    predicted_score = model.predict(input_df)[0]

    # generate feedback based on the score
    if predicted_score >= 10:
        feedback = "Excellent work! Your writing is clear and well-structured."
    elif predicted_score >= 7:
        feedback = "Good effort! Some improvements could be made in structure or clarity."
    elif predicted_score >= 4:
        feedback = "Fair, but your essay needs better organisation and vocabulary."
    else:
        feedback = "Your essay needs significant improvements in structure and language."

    # return both score and feedback
    return round(predicted_score, 2), feedback

# functions to switch windows

def open_essay_grader():
    grader = tk.Tk()
    grader.title("Automated Essay Grader")
    grader.geometry("1920x1080")

   # having a heading for the text box
    essay_label = tk.Label(grader, text="Enter your essay below:")
    # adding empty space above and below the text
    essay_label.pack(pady=10)
    # determining the size of the text box
    essay_text = tk.Text(grader, height=25, width=100)
    essay_text.pack()

    def upload_file():
        # opens the file explorer window 
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("Microsoft Word Documents", "*.docx"), ("Microsoft Edge PDF Document", "*.pdf")]
    ) 
        # if the file selected isn't an empty object
        if file_path.endswith(".txt"):
            # open the file 
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_path.endswith(".docx"):
            try:
                import docx
                from docx import Document
                from docx.opc.exceptions import PackageNotFoundError
                # loading the file
                doc = docx.Document(file_path)
                content = "\n".join([para.text for para in doc.paragraphs])
            # handles a corrupted file
            except PackageNotFoundError:
                messagebox.showerror("Corrupted File", "The .docx file appears to be corrupted or not a valid Word document")
                return
            except Exception as e:
                # just in case if there are other exceptions
                messagebox.showerror("Error", f"An error occures while reading the word file: {e}")
                return
        
        elif file_path.endswith(".pdf"):
            import PyPDF2
            reader = PyPDF2.PdfReader(file_path)
            content =""
            for page in reader.pages:
                content += page.extract_text()

            # cleans up the extracted PDF text
            # replacing multiple spaces with a single space
            content = re.sub(r'\s+', ' ', content)
            # replacing multiple new lines with a single space
            content = re.sub(r'\n+', ' ', content)
            # removed any trailing or leading whitespace
            content = content.strip()
    
        # error message for an unsupported or corrupted file
        else:
            messagebox.showerror("Unsupported File", "This file type is not supported.")
            return
        if not content.strip():
            raise ValueError("The file appears to be empty or unreadable.")


        # clears any text in the essay input text box
        essay_text.delete("1.0", tk.END)  
        # loads the new essay into the textbox
        essay_text.insert(tk.END, content)

    # adding the uploading file function as a button
    upload_button = tk.Button(grader, text="Upload text file", command=upload_file)
    upload_button.pack(pady=5)

    # function that is called when the "Grade Essay" button is clicked
    def on_grade_button_click():
        # removing whitespace from the text in the essay input box
        text = essay_text.get("1.0", tk.END).strip()
        # error if text box is empty
        if not text:
            messagebox.showerror("Error", "Essay is empty!")
            return
        try:
            # calling the function to get the predicted score and feedback
            score, feedback = grade_essay(text)  
            grade_button.config(text=f"Score: {score}/12\nFeedback: {feedback}")

             # print word count and sentence count to the terminal
            word_count = calculate_word_count(text)
            sentence_count = calculate_sentence_count(text)
        
            print(f"Word count: {word_count}")
            print(f"Sentence count: {sentence_count}")

        except Exception as e:
            # error message if something goes wrong
            messagebox.showerror("Error", f"Something went wrong: {e}")
    
    # grade essay function and links to the above function
    grade_button = tk.Button(grader, text="Grade Essay", command=on_grade_button_click)
    grade_button.pack(pady=10)

    grader.mainloop()

# TEACHER DASHBOARD

def open_teacher_dashboard():
# function to load essays from a folder or file
    def load_essays():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Documents", "*.docx"), ("PDF Files", "*.pdf")])
        if file_path:
            # initialising a variable to store the content of the file
            content = ""
            if file_path.endswith(".txt"):
                # loads the content of the txt file
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            elif file_path.endswith(".docx"):
                try:
                    import docx
                    # loading the .docx file
                    doc = docx.Document(file_path)
                    # joining all the paragraphs into a single string
                    content = "\n".join([para.text for para in doc.paragraphs])
                except Exception as e:
                    # showing an error if there is an issue reading the .docx file
                    messagebox.showerror("Error", f"An error occured while reading the Word file: {e}")
                    return
            elif file_path.endswith(".pdf"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(file_path)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text()
                        # cleaning up multiple spaces
                        content = re.sub(r'\s+', ' ', content)
                        # cleaning up new lines
                        content = re.sub(r'\n+', ' ', content)
                        content = content.strip()
                except Exception as e:
                    # show an error if there is an issue reading the PDF file
                    messagebox.showerror("Error", f"An error occured while reading the PDF file: {e}")
                    return
            else:
                # show an error if unsupported file
                messagebox.showerror("Unsupportef File", "This file type is not supported")
                return
            # show an error if the file content is empty or unreadable
            if not content.strip():
                messagebox.showerror("Error", "The file appears to be empty or unreadable.")
                return
             # adding the essay to the list in dashboard
            essays_listbox.insert(tk.END, content)

    # function to grade a selected essay
    def grade_selected_essay():
        selected_index = essays_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No essay selected!")
            return
    
        essay_text = essays_listbox.get(selected_index)
        score, feedback = grade_essay(essay_text)
        grade_label.config(text=f"Score: {score}/12\nFeedback: {feedback}")
        save_grade_feedback(score, feedback)

    def save_grade_feedback(score, feedback):
        with open("grades_feedback.txt", "a") as file:
            file.write(f"Score: {score}/12\nFeedback: {feedback}\n\n")

    teacher_dashboard = tk.Tk()
    teacher_dashboard.title("Teacher Dashboard")
    teacher_dashboard.geometry("1920x1080")

    # header
    header_label = tk.Label(teacher_dashboard, text="Teacher Dashboard", font=("Arial", 20))
    header_label.pack(pady=20)

    # a box showing the list of loaded essays
    essays_listbox = tk.Listbox(teacher_dashboard, width=100, height=15)
    essays_listbox.pack(pady=10)

    # button for loading the essay
    load_button = tk.Button(teacher_dashboard, text="Load Essays", command=load_essays)
    load_button.pack(pady=10)

    # button to grade a specific essay that is selected
    grade_button = tk.Button(teacher_dashboard, text="Grade Selected Essay", command=grade_selected_essay)
    grade_button.pack(pady=10)

    # displays the score and feedback for the selected essay
    grade_label = tk.Label(teacher_dashboard, text="Score: \nFeedback: ", font=("Arial", 12))
    grade_label.pack(pady=20)

    teacher_dashboard.mainloop()

# counter to track login attempts
login_attempts = 0

# function to check login credentials
def login():
    # so the variable can be modified
    global login_attempts
    username = username_entry.get()
    password = password_entry.get()
    # checking the username and password based on user roles
    if username == "teacher" and password == "teacher123":
        messagebox.showinfo("Login Successful", "Welcome!")
        # closes the login window
        login_window.destroy()
        # opens the teacher dashboard
        open_teacher_dashboard()
    elif username == "student" and password == "student123":
        # closes the login window
        login_window.destroy()
        open_essay_grader()
    else:
        # adds one to the counter
        login_attempts += 1
        # counts down how many attempts are left
        remaining_attempts = 3 - login_attempts
        if remaining_attempts >= 0:
            messagebox.showerror("Login Failed", f"Incorrect username or password. \nAttempts left: {remaining_attempts}")
        else:
            # locked message
            messagebox.showerror("Account Locked", "Too many failed attempts. Account locked.")
            # disables the login button
            login_button.config(state="disabled")

# login window

# creates the window
login_window = tk.Tk()
login_window.title("Login Page")
login_window.geometry("1920x1080")

# creating a section for a login information so that it is placed in the centre
login_frame = tk.Frame(login_window)
login_frame.pack(expand=True)

# defining a font and font size
font_style = ("Arial", 18)

# adding input text boxes for username
username_label = tk.Label(login_frame, text="Username:", font=font_style)
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=font_style, width=30)
username_entry.pack(pady=10)

# adding input text boxes for password
password_label = tk.Label(login_frame, text="Password:", font=font_style)
password_label.pack(pady=10)
# this would hide the input and show * instead
password_entry = tk.Entry(login_frame, font=font_style, show="*", width=30)
password_entry.pack(pady=10)

# login button
login_button = tk.Button(login_frame, text="Login", font=font_style, command=login)
login_button.pack(pady=20)

login_window.mainloop()

