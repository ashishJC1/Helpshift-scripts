#----------------------------------------------------------------------
#----------------------------------------------------------------------
# test_tick: Mostly responsible for making API calls to HelpShift and 
#  confirming if the email exists

#  Author: Ashish Kumar 
#         ( Github: Axeish) 
#         ( Github URL:---)
#
#  Project entry point : __main__
#  Dependency : CSV file as input
#----------------------------------------------------------------------

#My Library


#Python Library
from datetime import datetime, time, timedelta, timezone
import requests
import json
import base64
import sys
import logging
import csv
from csv import writer
from csv import reader
from csv import DictReader
from csv import DictWriter
 
 
def add_column_in_csv(input_file, output_file, transform_row):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)
 



def check_mate_me(email):
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic amFtY2l0eV9hcGlfMjAxODA1MjQyMjI4NTQ1MTQtNDNkZmJjY2Q5ZDJiMzdk',}
    email_param =  '{"or" : ["jagaloo@jol.com" , "%s"] , "exists" : "true"}'%(email)

    params = (
    ('author_emails', email_param ),)

    response = requests.get('https://api.helpshift.com/v1/jamcity/issues', headers=headers, params=params) 
    hold= response.json()
    print(email)
    return hold["total-hits"]







def request_call(email, uid, message, game, comment):
    headers = {
    
    'Accept': 'application/json',
    'Authorization': 'Basic amFtY2l0eV9hcGlfMjAxODA1MjQyMjI4NTQ1MTQtNDNkZmJjY2Q5ZDJiMzdk',
    }

    cif = '{"client_id":{"type":"singleline","value":"%s"}, "game":{"type":"dropdown","value":"%s"},"insider":{"type":"checkbox","value":"true"}}'%(uid,game),
              
    payload = {"email": email,
                 "platform-type":"web",
                 "message-body": "%s issues mass_created"%comment+ '\n\n'+ message,
                 "title": "%s issues mass_created"%comment,
                 "custom_fields":cif,  "tags":'["insiders_initiative"]'}

    response = requests.post('https://api.helpshift.com/v1/jamcity/issues', headers=headers, data=payload)
    


if __name__ == "__main__":
  filename = sys.argv[1]
  outfile = sys.argv[2]
  add_column_in_csv(filename, outfile, lambda row, line_num: row.append(check_mate_me(row[0])))

  with open(outfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
 
            if row[5]=='0':
                print(f'\t{row[0]} :{row[1]} added to {row[3]}...')
                line_count += 1
                request_call(row[0],row[1],row[2],row[3],row[4])
            else:
                print(f'\t{row[0]} Already exists')


   

    print(f'Processed {line_count} lines.')



  	