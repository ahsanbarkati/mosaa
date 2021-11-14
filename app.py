from flask import Flask, request, render_template
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import SelectField 
import numpy as np

data = pd.read_csv('./data.csv')
data2 = pd.read_csv('./data2.csv')
data2 = data2[data2['Admitted Round'] == 2]
data2['Category'] = data2[['Allotted Category', 'Allotted ph']].apply(lambda x: '-'.join(x), axis=1)

colleges = data['Allotted Institute'].unique()
colleges = np.sort(np.array(colleges))

colleges2 = data2['Institute'].unique()
colleges2 = np.sort(np.array(colleges2))
colleges2 = [c.replace('\n',"") for c in colleges2]

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
  categories = cd['Category'].unique()
  for category in categories:
    cat_data = cd[cd['Category'] == category]
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
  op_data2[college] = open_close2(college_data)

def get_oc(col):
  return op_data[col]

def get_oc2(col):
  return op_data2[col]

cols2 = [k for k in op_data2]
cols2 = np.sort(np.array(cols2))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

class Form(FlaskForm):
	college = SelectField("college", choices = colleges)

class Form2(FlaskForm):
	college = SelectField("college", choices = cols2)

@app.route('/', methods=["GET", "POST"])
def fun():
	return render_template("./home.html")

@app.route('/round1', methods=["GET", "POST"])
def round1():
    form = Form()
    oc = {}
    cats = []
    col = ""
    if request.method == "POST":
        print("a post method", form.data)
        col = form.data["college"]
        oc = get_oc(col)
        cats = [c for c in oc.keys()]
    return render_template("./main.html", form=form, oc=oc, cats=cats, college=col)


@app.route('/round2', methods=["GET", "POST"])
def round2():
	form2 = Form2()
	oc = {}
	cats = []
	col = ""
	if request.method == "POST":
		print("a post method", form2.data)
		col = form2.data["college"]
		oc = get_oc2(col)
		cats = [c for c in oc.keys()]

	return render_template("./main.html", form=form2, oc=oc,cats=cats, college=col)

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
