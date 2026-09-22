# 4420-Assignment
# Repository for ACIT4420 assignment 1, smart fitness analyzer

# Preface
I decided to make this program pretty simple as i am not very experienced in scripting with python, i therefore took it more as a learning experience. Please give me feedback if there is something i should do differently! More of the code is explained in the code itself by comments.

# Very simple program for running the fitness texts, and outputs them giving them a category for the amount of activity. 

# How to run:
To run this program nothing extra is required, it should work by cloning the code and running the main.py file in your environment. It uses standard python libraries and the data_generator file, which was given in the assignment. 

# Reasons for writing the code as it is
My program uses the generated data given, validating, summarizing and classifying it. The flow of the program is get data -> session -> validate -> summarize -> print.

**Participant**
Holds the persons data like the heart rate etc. Gives the program a class i can reuse in other parts of the program if i need data such as this.

**Observation**
Is one sensor reading at a given timestamp, i made it so it is in general looking for valid data, if not it invalidates them and gives the error. 

**Session**
The part of my code that does the most and uses the other classes. Firstly it validates the data to see if it is correct, then averages the valid observations, and classifies the activity based on the results.

**Session report**
Final class that dont really do anything else than to print whatever the program tells it. So if the data is valid it prints that, and if not it prints invalid.


I built the program like this so it was easier for me to understand python. I probably could have made it more advanced or ran multiple sessions at once generating more results but that was too complicated. It is a bit dumb of a program in it self but i learned alot by writing it and getting familiar with class structures and definitions.
