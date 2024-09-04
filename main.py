#This code is for the creation of web data using Python
#imported the data.csv and flask 
import csv
from flask import Flask, request, render_template

#storeded the data.csv into a variable called DATA_FILE and a List
DATA_FILE = 'data.csv'
FIELDNAMES = ['id', 'name', 'year', 'summary']

#created an empty list 
music = []

app = Flask(__name__)

#this code reads out the what was added as you add 
def load_data_file():
  with open(DATA_FILE) as data_file:
    reader = csv.DictReader(data_file)
    for row in reader:
      print(row)
      music.append(row)

#this code writes what you add in the artist category of the list
def append_data_file(artist):
  with open(DATA_FILE, 'a', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writerow(artist)

#this code writes to music to the artist
def dump_data_file():
  with open(DATA_FILE,'w', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writeheader()
    for artist in music:
      writer.writerow(artist)
  


#this creates the music category to JSON and the HTML
@app.route('/music')
def music_index():
  return render_template('index.html', music=music)

#this creates the id number for each line put in
@app.route('/music/<id>')
def music_show(id):
  for artist in music:
    if artist['id'] == id:
      return render_template('show.html', artist=artist)

#returns the error code for page not found
  return { 'error': 'Not Found' }, 404

#this writes to JSON
@app.route('/music', methods=['POST'])
def music_create():
  new_artist = request.get_json()
  music.append(new_artist)
  append_data_file(new_artist)
  return { 'message': 'Music Creadted Successfuly' },201

  
@app.route('/music/<id>', methods=['PATCH'])
def music_update(id):
  updated_fields = request.get_json()

#Created a for loop to interate through and update   
  for m in music:
    if m['id'] == id:
      m.update(updated_fields)
      dump_data_file()
      return { 'message': 'Music Updated Successfully' }, 201

#if not found show error not find
  return { 'error': 'Not Found' },404

#to remove items from the list
@app.route('/music/<id>', methods=['DELETE'])
def music_delete(id):
  found_idx = None

  
 # Find the index of movie to delete
  for i in range(len(music)):
    if music[i]['id'] == id:
      found_idx = i
      break
  
# Delete the movie, if we found the index
  if found_idx != None:
    music.pop(found_idx)
    dump_data_file()
    return { 'message': 'Music deleted successfully' }, 201
    
# If we can't find the index, 404
    return { 'error': 'Not Found' }, 404


load_data_file()
app.run(host='0.0.0.0')
