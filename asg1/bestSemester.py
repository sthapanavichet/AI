# bestSemester.py
# VM

# inspired by # shopSmart.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
Here's the intended output of this script, once you fill it in:

Student Jim registered
GPA for semester 1 for Jim is 83.0
Student not registered for sea100
GPA for semester 2 for Jim is 88.09
Student not registered for sea100
The highest achieved term GPA by this student is 88.09
"""

from __future__ import print_function
import student

def highestGPA(semGradeList, astudent):
    """
        semGradeList: List of semesters, each a list of (course, grade) tuples
        astudent: a student
    """
    highest = astudent.getGPA(semGradeList[0])
    for semGrade in semGradeList:
        semGPA = astudent.getGPA(semGrade)
        if semGPA > highest:
            highest = semGPA
    return highest

    


if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
 
    std = student.Student('Jim', {'mth110':4.0, 'sep101': 4.0, 'mec110':6.0, 'mth200': 4.0, 'sep200': 4.0, 'sed200': 3.0} )
    semester1 = [('mth110', 75.0), ('sep101', 82.0), ('mec110', 89.0)]
    semester2 = [('mth200', 80.0), ('sep200', 91.0), ('sed200', 95.0), ('sea100', 50.0)]

    # print GPA for semester 1
    print("GPA for semester 1 for", std.getGPA(semester2))
    print("GPA for semester 2 for", std.getGPA(semester1))

    sems = [semester1, semester2]
    print("The highest achieved term GPA by this student is", highestGPA(sems, std))