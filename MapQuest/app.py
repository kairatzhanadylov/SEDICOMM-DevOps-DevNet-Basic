from flask import Flask, render_template, request
from DevOps_DevNet.Part5.MapQuest.directions_logic import get_directions 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    directions_data = None
    
    if request.method == 'POST':
        orig = request.form.get('origin')
        dest = request.form.get('destination')
        units = request.form.get('units', 'm')
        
        if orig and dest:
            directions_data = get_directions(orig, dest, units)
        else:
            directions_data = {"error": "Пожалуйста, введите начальное и конечное местоположения."}

    return render_template('index.html', result=directions_data)

if __name__ == '__main__':
    app.run(debug=True)