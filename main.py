import csv
from flask import Flask, request, render_template

DATA_FILE = 'data.csv'
FIELDNAMES = ['id', 'name', 'year', 'summary']

music = []

app = Flask(__name__)

def load_data_file():
  with open(DATA_FILE) as data_file:
    reader = csv.DictReader(data_file)
    for row in reader:
      print(row)
      music.append(row)

def append_data_file(artist):
  with open(DATA_FILE, 'a', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writerow(artist)

def dump_data_file():
  with open(DATA_FILE,'w', newline='') as data_file:
    writer = csv.DictWriter(data_file, FIELDNAMES)
    writer.writeheader()
    for artist in music:
      writer.writerow(artist)
    



@app.route('/music')
def music_index():
  return render_template('index.html', music=music)

@app.route('/music/<id>')
def music_show(id):
  for artist in music:
    if artist['id'] == id:
      return render_template('show.html', artist=artist)

  return { 'error': 'Not Found' }, 404


@app.route('/music', methods=['POST'])
def music_create():
  new_artist = request.get_json()
  music.append(new_artist)
  append_data_file(new_artist)
  return { 'message': 'Music Creadted Successfuly' },201

  
@app.route('/music/<id>', methods=['PATCH'])
def music_update(id):
  updated_fields = request.get_json()

  
  for m in music:
    if m['id'] == id:
      m.update(updated_fields)
      dump_data_file()
      return { 'message': 'Music Updated Successfully' }, 201

  return { 'error': 'Not Found' },404


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

# Write all of your code here
load_data_file()
app.run(host='0.0.0.0')
