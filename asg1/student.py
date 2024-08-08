# student.py  
# VM

# inspired by shop.py
# -------
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


class Student:

    def __init__(self, name, courseUnits):
        """
            name: Name of the student

            courseUnits: Dictionary with keys as course
            strings and units for values e.g.
            {'math':4.0, 'science': 3.0, 'art':2.0}
        """
        self.courseUnits = courseUnits
        self.name = name
        print('Student %s registered' % name)

    def getCourseUnits(self, course):
        """
            course: Course string
        Returns units of 'course', assuming 'course'
        is in courseUnits dictionary or None otherwise
        """
        if course not in self.courseUnits:
            print("Student not registered for", course)
            return None
        else:
            return self.courseUnits[course]

    def getGPA(self, gradeList):
        """
            gradeList: List of (course, grade) tuples

        Returns GPA given gradeList, only including the grades of
        courses that this student has registered for
        """
        totalUnits = 0
        totalGP = 0
        for grade in gradeList:
            courseUnit = self.getCourseUnits(grade[0])
            if courseUnit:
                totalGP += grade[1] * courseUnit
                totalUnits += courseUnit
        return totalGP / totalUnits

    def getName(self):
        return self.name

    def __str__(self):
        return "<Student Name: %s>" % self.getName()

    def __repr__(self):
        return str(self)
