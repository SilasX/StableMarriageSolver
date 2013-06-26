#!/usr/bin/python

import sys
from helpers import extract_int

# Solution for the student-school matching problem, a generalized version of the Stable Marriage Problem

SCHOOL_CHARACTER = 'U'
STUDENT_CHARACTER = 'S'
INPUT_FILE_NAME = "input/input.txt"
OUTPUT_FILE_NAME = "output/solution.txt"
NUM_FACTORS = 3  # number of factors: 3 for this setup

class DebugWriter(object):

    def __init__(self, is_write=True, fd=sys.stdout):
        self.is_write = is_write
        self.fd = fd

    def write_debug(self, debug_str):
        """Utility function for writing output (or not) to file object fd"""
        if self.is_write:
            self.fd.write("{debug_str}\n".format(debug_str=debug_str))


class School(object):

    def __init__(self, name, scores):
        self.name = name  # identifier for this school (C1, 2, ...)
        self.scores = scores
        self.students = []  # initialize assigned student list to empty

    def show_students(self):
        return self.name + " " + ", ".join([student.name for student in self.students])
        
    def match_rating(self, student):
        """return the quality of the match, which is dot product of the factors
        """
        return sum([self.scores[i] * student.scores[i] for i in range(NUM_FACTORS)])

    def match_string(self):
        """returns list of students it has attached and their match ratings
        """
        return self.name + " " + ", ".join([student.match_string() for student in self.students])

    def attach(self, new_student):
        """key algorithm: students all "attach" themselves to their most favorite school that hasn't rejected them, and are added in the order of the quality of their match with the school; if that student (or the one that must be bumped if any) is a worse match and there is no room, that student is returned so they can be added to the unassigned pool.  Returns None on successful assignment to this school.
        """
        WRITER.write_debug("Student {student} now wants to be with school {school}".format(student=new_student.name, school=self.name))
        if self.students == []:
            # if empty, initialize to one-element list with new_student
            self.students = [new_student]
            WRITER.write_debug("School {school} accepts new student, {student}".format(school=self.name, student=new_student.name))
            WRITER.write_debug("... and now has 1 student")
            return None
        else:
            # insert student in decreasing order of match rating
            # save value of new_student match rating to avoid recomputing
            new_student_rating = self.match_rating(new_student)
            num_in_school = len(self.students)
            for i in range(num_in_school):
                # if better than current, insert ahead of current and exit
                if new_student_rating > self.match_rating(self.students[i]):
                    WRITER.write_debug("School {school} accepts new student, {student}".format(school=self.name, student=new_student.name))
                    WRITER.write_debug("... and now has {count} students".format(count=num_in_school + 1))
                    self.students.insert(i, new_student)
                    WRITER.write_debug(self.show_students())
                    # if more than STUDENTS_PER_SCHOOL, bump the last one on the list
                    if num_in_school + 1 > STUDENTS_PER_SCHOOL:
                        bumped_student = self.students[-1]
                        del self.students[-1]  # remove from list
                        WRITER.write_debug("... so school {school} bumps student {student}".format(school=self.name, student=bumped_student.name))
                        return bumped_student
                    else:
                        return None  # successful assignment
            # if control reaches this point, student was worse than those already assigned
            # if list is full, student is rejected and must be assigned to next-favorite
            if num_in_school + 1 > STUDENTS_PER_SCHOOL:
                WRITER.write_debug("... but school {school} already has enough better-matched students".format(school=self.name))
                return new_student
            else:
                WRITER.write_debug("School {school} accepts new student, {student}".format(school=self.name, student=new_student.name))
                WRITER.write_debug("... and now has {count} students".format(count=num_in_school + 1))
                self.students.append(new_student)
                WRITER.write_debug(self.show_students())
                return None

class Student(object):

    def __init__(self, name, scores, school_prefs):
        self.name = name  # in the form J[integer]
        self.scores = scores  # length-3 list of H/E/P scores
        self.school_prefs = school_prefs  # school (object)s in order of preference, highest to lowest
        self.num_prefs = len(school_prefs)  # number of schools specified in preference listing
        self.ischool = None  # array index of school student is currently assigned to; initialize to None

    def match_string(self):
        """write the match ratings for student over each school in self.school_prefs list
        """
        return self.name + " " + " ".join(["{school_name}:{score}".format(
            school_name=school.name,
            score=school.match_rating(self)
        ) for school in self.school_prefs[:self.num_prefs]])  # limit the output to preferences specified

    def take_next_choice(self):
        # reassigns student to next school and returns that school object
        if self.ischool == None:
            WRITER.write_debug("Student {student} initiates a school join.".format(student=self.name))
            # if unassigned, start with first
            self.ischool = 0
        else:
            self.ischool += 1
            if self.ischool >= len(self.school_prefs):  #NUM_SCHOOLS:
                WRITER.write_debug("Uh oh! This student exhausted their preference list!  Let's revert back to the school's preferences, which are actually defined for the entire input set.")
                # generate student preference over rest of schools based on school match score
                other_schools = [school for school in all_schools if school not in self.school_prefs]
                other_schools = sorted(other_schools, reverse=True, key=lambda school: school.match_rating(self))
                WRITER.write_debug("Remaining preferences:")
                WRITER.write_debug(" ".join([school.name for school in other_schools]))
                self.school_prefs += other_schools
        return self.school_prefs[self.ischool].attach(self)


class SMProblem(object):
    """Container class for an instance of the (generalized) Stable Marriage Problem
    """

    def __init__(self, schools, students):
        self.schools = schools  # array of school objects
        self.students = students  # array of student objects
        self.unmatched_students = students  # students still to be assigned

    def solve(self):
        while self.unmatched_students != []:
            # remove the last student on the list and have them attempt to attach to their next choice
            # (both are done with the pop operation);
            # has side effect of incrementing student's current "best option"
            freed_student = self.unmatched_students.pop()
            freed_student = freed_student.take_next_choice()  # returns bumped student if any
            if freed_student != None:
                self.unmatched_students.append(freed_student)

    def write_debug_solution(self, fd=sys.stdout):
        if self.unmatched_students != []:
            fd.write("Solution not found yet.\n")
        else:
            for school in self.schools:
                fd.write(school.match_string())
                fd.write("\n")


# main loop of program
if __name__ == "__main__":
    if len(sys.argv) > 1:  # if user passed an argument
        # make that the input file instead
        INPUT_FILE_NAME = sys.argv[1]
    INPUT_FDO = open(INPUT_FILE_NAME, "r")
    NUM_STUDENTS = 0
    NUM_SCHOOLS = 0
    all_schools = []
    all_students = []
    WRITER = DebugWriter(False)
    # iterate over lines in input file and parse them
    for line in INPUT_FDO:
        cur_line = line.strip().split(" ")
        if cur_line[0] == SCHOOL_CHARACTER:
            # parse school line
            # format: U U0 A:7 B:3 C:10
            school_name = cur_line[1]
            score_list = [extract_int(cur_line[line_index]) for line_index in range(2, 2 + NUM_FACTORS)]
            all_schools.append(School(school_name, score_list))
            NUM_SCHOOLS += 1
            WRITER.write_debug("finished entering school {school_name}".format(school_name=school_name))
        elif cur_line[0] == STUDENT_CHARACTER:
            # parse student line
            # format: S S0 A:3 B:9 C:2 U2,U0,U1
            student_name = cur_line[1]
            score_list = [extract_int(cur_line[line_index]) for line_index in range(2, 2 + NUM_FACTORS)]
            # ASSUME that schools were entered in order of name, and thus name matches index
            pref_indexes = [int(school[1:]) for school in cur_line[-1].split(",")]
            # turn into list of School objects for Student object creation
            pref_objects = [all_schools[index] for index in pref_indexes]
            all_students.append(Student(student_name, score_list, pref_objects))
            NUM_STUDENTS += 1
    INPUT_FDO.close()
    # with data parsed, set up SMProblem object with school and object list
    # iterate over student list and attach each one, which triggers reassignments as necessary
    STUDENTS_PER_SCHOOL = NUM_STUDENTS / NUM_SCHOOLS
    if STUDENTS_PER_SCHOOL * NUM_SCHOOLS != NUM_STUDENTS:
        WRITER.write_debug("You promised that the number of schools would evenly divide the students.  Um, {num_students} students and {num_schools} schools isn't exactly what I'd call 'evenly divided'".format(num_students=NUM_STUDENTS, num_schools=NUM_SCHOOLS))
        sys.exit(1)
    problem_instance = SMProblem(all_schools, all_students)
    problem_instance.solve()
    # with all assignments made, now print out results
    with open(OUTPUT_FILE_NAME, "w") as f:
        problem_instance.write_debug_solution(f)
    
