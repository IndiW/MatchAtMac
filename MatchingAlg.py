#Match at Mac algorithm using match scoring and stable marriage 
import csv
import random
from operator import itemgetter
from checkmatch import check_match

FREE = 0
ENGAGED = 1
conv_relationship = ["blank","platonic", "monogamous", "casual","open"]
conv_gender = ["blank","cismale", "cisfemale", "transmale", "transfemale", "nonbinary", "not listed"]
conv_gender_seeking = ["cismale","cisfemale", "transmale", "transfemale", "nonbinary", "not listed"]
conv_orient = ["blank","heterosexual","homo","bi","asexual","pan","questioning","other"]
conv_orient_seeking = ["heterosexual","homo","bi","asexual","pan","questioning","other"]

class person:
    '''Person object to store information about each submission'''
    def __init__(self, data, id_num=None):
        self.id = id_num  #integer id for ranking
        self.iskey = False
        self.email = data[0].lower()
        self.first_name = data[1]
        self.last_name = data[2]

        data_1 = list(map(int, data[3:15]))
        data_2 = list(map(int,data[16:20]))
        data_3 = list(map(int,data[21:]))
        self.raw_data = data[0:3] + data_1 + [data[15]] + data_2 + [data[20]] + data_3

        self.ranks = [] #sorted list of match preferences
        self.state = ENGAGED

    def get_relationship_seeking(self):
        #[platonic friend, monogamous, casual, open]
        return self.raw_data[3:7]

    def get_gender(self):
        #1: cis male, 2: cis female, 3: trans male, 4: trans female, 5: non binary, 6: not listed
        return self.raw_data[7]

    def get_gender_seeking(self):
        #[cis male, cis female, trans male, trans female, non binary, not listed]
        return self.raw_data[8:14]
    
    def get_orientation(self):
        # 1: heterosexual, 2: homo sexual, 3: bi sexual, 4: asexual, 5: pansexual, 6:questioning, 7: other
        return self.raw_data[14]

    def get_orientation_text(self):
        return self.raw_data[15]

    def get_orientation_seeking(self):
        #[heterosexual, homosexual, bisexual, asexual, pansexual, questioning,other]
        x = self.raw_data[16:19] + self.raw_data[46:49]
        x.append(self.raw_data[19])
        return x
    
    def get_orientation_seeking_text(self):
        return self.raw_data[20]
    
    def get_data(self):
        return self.raw_data[21:46]

def matchWeight(p1, p2):
    '''Takes two person objects and returns a value corresponding to the 
    similarity match between the two people. Max possible score is 25. Min is 0'''
    matchCount = 0
    for i in range(len(p1.get_data())): #Skip gender and sexuality fields
        if p1.get_data()[i] == p2.get_data()[i]:
            matchCount += 1
    return matchCount

def read_csv_filter(filename, filename2):
    '''Reads 2 csv files containing the submission information and removes already matched'''
    d = {}
    count = 0
    with open(filename2,newline='') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            count +=1 
            if row[0] in d: #remove error repeats
                print(row[0],row[1])
                continue 
            elif row[1] in d:
                print(row[0],row[1])
                continue

            d[row[0]] = True
            d[row[1]] = True

    print(count)
    print("There are ", len(d), " matches in this file")


    people = []
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0].lower() in d:
                continue
            p = person(row)
            people.append(p)
    print("There are ", len(people), " people to be matched")
    return people


def read_csv(filename):
    '''Reads a csv file containing the submission information'''
    people = []
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            p = person(row)
            people.append(p)
    return people

def matching_alg_2(data):
    '''Takes two lists of groups (eg men and women) where each person has a ranked list of their preference and finds stable matches'''
    data1 = data[:len(data)//2]
    data2 = data[len(data)//2:]
    d = {} 
    d2 = {}
    for student in data1:
        for student2 in data2:
            if student is not student2:
                if True:
                #if check_match(student, student2): #check if they can match
                    w = matchWeight(student, student2) #calculate score

                    if student.email in d:
                        d[student.email].append((student2.email,w))
                    else:
                        d[student.email] = []
                        d[student.email].append((student2.email,w))
                    if student2.email in d2:
                        d2[student2.email].append((student.email,w))
                    else:
                        d2[student2.email] = []
                        d2[student2.email].append((student.email,w))

    for key in d.keys():
        d[key] = [val[0] for val in sorted(d[key],key=itemgetter(1),reverse=True)]
    for key in d2.keys():
        d2[key] = [val[0] for val in sorted(d2[key],key=itemgetter(1),reverse=True)]
    return d, d2



def matching_alg(data):
    '''Takes a list of student objects, checks if they are compatible, and saves the data in a dictionary with keys = student email, and values = 
    a list of tuples containing the potential matches email and their weight'''
    resultA = {} #males
    resultB = {} #females

    for ind1, student in enumerate(data):
        for student2 in data[ind1:]:
            if student is not student2:
                if True:
                #if check_match(student, student2): #check if they can match
                    w = matchWeight(student, student2) #calculate score

                    #set a to male student, b to female student
                    #a = student if student.get_gender() == 1 else student2
                    #b = student2 if student2.get_gender() == 2 else student
                    a = student
                    b = student2
                    
                    if True:
                    #if not a.get_gender() == 1 and not a.get_gender() == 2 and not b.get_gender() == 1 and not b.get_gender() == 2: 
                    #if a.get_gender() == 1 and b.get_gender() == 2: #if student1 is a cis male and student2 is a cisfemale
                        if a.email in resultA: #add to group A dictionary
                            resultA[a.email].append((b.email, w))
                            
                        else:
                            if not a.iskey:
                                resultA[a.email] = []
                                resultA[a.email].append((b.email, w))
                                a.iskey = True
                            else:
                                break

                        if b.email in resultB: #add to group B dictionary
                            resultB[b.email].append((a.email,w))

                        else:
                            if not b.iskey:
                                resultB[b.email] = []
                                resultB[b.email].append((a.email,w))
                                b.iskey = True


    retA = {}
    retB = {}
    for key in resultA.keys():
        retA[key] = [val[0] for val in sorted(resultA[key],key=itemgetter(1),reverse=True)]
    for key in resultB.keys():
        retB[key] = [val[0] for val in sorted(resultB[key],key=itemgetter(1),reverse=True)]
    
    return retA, retB


def read_csv_to_dict(filename):
    '''Reads a csv file containing the submission information'''
    people = {}
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            p = person(row)
            people[row[0].lower()] = p
    return people

if __name__ == "__main__":
    #Add Code Here
    print("Match at Mac!")

