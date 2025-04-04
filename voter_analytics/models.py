"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-04-2
Description: Defines Profile and StatusMessage Model
"""
from django.db import models

# Create your models here.

class Voter(models.Model):
    '''Represent data from one voter in Netwon
    First Name, Last Name, Street Number, Street Name,
    Apartment Number, Date of Birth, Party Affiliation,
    Voter Score '''

    # define attributes of Voter object

    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    date_of_birth = models.DateField()

    # political stats
    party_affiliation = models.TextField()
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this Voter object.'''
        return f'{self.first_name} {self.last_name} {self.street_number} {self.street_name} {self.apartment_number} {self.date_of_birth}'

    def load_data():
        '''Function to load data from CSV file into the Django database'''
        Voter.objects.all().delete()

        # Use a path that works on both local and server environments
        import os
        from django.conf import settings

        # Try to find the CSV file in multiple locations
        possible_paths = [
            os.path.join(settings.BASE_DIR, 'newton_voters.csv'),  # Project root
            os.path.join(settings.BASE_DIR, 'static', 'newton_voters.csv'),  # Static folder
            os.path.join(settings.STATIC_ROOT, 'newton_voters.csv'),  # Collected static files
            '/Users/derinellrojas/Desktop/django/static/newton_voters.csv',  # Original hardcoded path
            '/Users/derinellrojas/Desktop/django/newton_voters.csv',  # Alternative path
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'newton_voters.csv'),  # App directory
        ]

        # Try each path until we find the file
        filename = None
        for path in possible_paths:
            if os.path.exists(path):
                filename = path
                print(f"Found CSV file at: {filename}")
                break

        if not filename:
            raise FileNotFoundError("Could not find newton_voters.csv in any of the expected locations. Paths checked: " + str(possible_paths))

        f = open(filename, 'r') #open the file for reading

        # discard headers:
        f.readline() #do nothing with it

        #read several rows
        for line in  f:
                try:
                    fields = line.strip().split(',')
                    # print(fields)
                    # for j in range(len(fields)):
                    #     print(f'fields[{j}] = {fields[j]}')
                    # fields[0] = 10KSA1343001
                    # fields[1] = KIGGEN
                    # fields[2] = SHEILA
                    # fields[3] = 193
                    # fields[4] = OAK ST
                    # fields[5] = 103E
                    # fields[6] = 02464
                    # fields[7] = 1943-10-13
                    # fields[8] = 2016-02-10
                    # fields[9] = D
                    # fields[10] = 1
                    # fields[11] = TRUE
                    # fields[12] = TRUE
                    # fields[13] = FALSE
                    # fields[14] = TRUE
                    # fields[15] = FALSE
                    # fields[16] = 3


                    # create a new instance of Voter object with this record from the CSV file
                    voter = Voter(first_name=fields[2],
                                last_name=fields[1],
                                street_number=fields[3],
                                street_name=fields[4],
                                apartment_number=fields[5],
                                date_of_birth=fields[7],
                                party_affiliation=fields[9],
                                v20state=fields[11],
                                v21town=fields[12],
                                v21primary=fields[13],
                                v22general=fields[14],
                                v23town=fields[15],
                                voter_score=fields[16])
                    voter.save()
                    print(f'Created voter {voter}')
                except Exception as e:
                    print(f"Error processing line: {line}")
                    print(f"Error details: {str(e)}")
                    print(f"Fields: {fields}")
                    continue

        print(f"Done, Created {len(Voter.objects.all())} Voters")