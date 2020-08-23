#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect

import os, json

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
# app.config.from_object('config')


@app.route('/', methods=['POST','GET'])
def uploadimg():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
        	file.save(os.path.join('./static/upload/', file.filename))
        	return render_template('annotation.html',res=json.dumps({'file': '../static/upload/'+file.filename}))
    else:
        return render_template('uploadimg.html')

@app.route('/processData', methods=['POST','GET'])
def processData():
    if request.method == 'POST':
        data = dict(request.form)
        print(data)
        return 'data processed'



#****************************************************************






# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
