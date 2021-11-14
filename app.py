from flask import Flask, request, render_template
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField 
import numpy as np

data = pd.read_csv('./data.csv')
data2 = pd.read_csv('./data2.csv')
data2 = data2[data2['Admitted Round'] == 2]

colleges = data['Allotted Institute'].unique()
colleges = np.sort(np.array(colleges))

colleges2 = data2['Institute'].unique()
colleges2 = np.sort(np.array(colleges2))

def get_open_close(d):
  if len(d) == 0:
    return "NA","NA"
  return d[0], d[-1]

def open_close(cd):
  info = {}
  categories = cd['Alloted Category'].unique()
  for category in categories:
    cat_data = cd[cd['Alloted Category'] == category]
    o, c = get_open_close(cat_data['Rank'].values)
    info[category] = {
        "total": len(cat_data),
        "opening": o,
        "closing": c,
    }
  return info

def open_close2(cd):
  info = {}
  categories = cd['Allotted Category'].unique()
  for category in categories:
    cat_data = cd[cd['Allotted Category'] == category]
    o, c = get_open_close(cat_data['AIR'].values)
    info[category] = {
        "total": len(cat_data),
        "opening": o,
        "closing": c,
    }
  return info

op_data = {}
for college in colleges:
  college_data = data[data['Allotted Institute'] == college]
  info = open_close(college_data)
  op_data[college] = info

op_data2 = {}
for college in colleges2:
  college_data = data2[data2['Institute'] == college]
  info = open_close2(college_data)
  op_data2[college] = info

def get_oc(col):
  return op_data[col]

def get_oc2(col):
  return op_data2[col]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

class Form(FlaskForm):
	college = SelectField("college", choices = colleges)
	roundno = SelectField("roundno", choices = [1, 2])

@app.route('/', methods=["GET", "POST"])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	form = Form()

	oc = {}
	cats = []
	if request.method == "POST":
		print("a post method", form.data)
		col = form.data["college"]
		rnd = form.data["roundno"]
		if rnd == "1":
			oc = get_oc(col)
		elif rnd == "2":
			oc = get_oc2(col)
		cats = [c for c in oc.keys()]


	
	return render_template("./main.html", form=form, oc=oc,cats=cats)


# main driver function
if __name__ == '__main__':
    app.run(debug=True)
