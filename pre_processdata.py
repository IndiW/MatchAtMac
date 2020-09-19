import csv

def read_csv(filename, output):
    '''Reads a csv file and save a new file with incorrect emails removed'''
    count = 0
    with open(output,'w') as write_file:
        writer = csv.writer(write_file, delimiter=',')
        with open(filename, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if "@mcmaster.ca" not in row[0]:
                    continue
                writer.writerow(row)
                count += 1
    print("Done writing ", count, " lines")

def check_csv(filename):
    '''Check if there are incorrect emails in csv'''
    count = 0
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if "@mcmaster.ca" not in row[0]:
                count += 1
    print(count, " invalid lines")
    if count != 0:    
        return False
    return True
    

check_csv("processed.csv")