#!/usr/bin/python

#import
import os #global
from flask import (  #web framework
    Flask,
    render_template,
    send_from_directory,
    send_file,
    request,
    redirect,
    url_for,
    request,
    session,
)
from escpos.printer import Usb #printer driver


# create flask app
app = Flask(__name__)
app.secret_key = '4334fdsergsFGSDfsdfgSgfdsgsdsresgdsSERE'.encode('utf8')

# return static files
@app.route('/Semantic-UI-CSS/<path:path>')
def send_js(path):
    return send_from_directory('Semantic-UI-CSS', path)

# return label collection 
@app.route('/label/<path:path>')
def send_label(path):
    return send_from_directory('label', path)

# index page
@app.route('/')
def do_index():
   return redirect(url_for('do_choose'))
   #return render_template('index.html')


# choose page
@app.route('/choose')
def do_choose():
    labels = os.listdir('label') #read all files
    return render_template('choose.html', labels = labels)

# select page
@app.route('/edit', methods=['GET'])
def do_edit():
    try:
        session['labelsvg'] = request.args['labelsvg']
    except Exception as e:
        if session['labelsvg'] == "":
            return(str(e))
    
    return render_template('edit.html')

# preview page
@app.route('/preview', methods=['POST'])
def do_preview():

    session['txt1'] = request.form['txt1']
    session['txt2'] = request.form['txt2']
    session['txt3'] = request.form['txt3']
    session['txt4'] = request.form['txt4']

    return render_template('preview.html')

# preview image
@app.route('/prev_img')
def send_preview_img():
   return send_file(filename_or_fp='img.png',mimetype='image/png')


#print
@app.route('/print', methods=['POST'])
def do_print():
   
    #config printer
    p = Usb(0x4b43, 0x3538,0 ,0xB2, 0x02  )
    #   lsus
    #   lsusb -vvv -d 4b43:3538"b
    #   sudo usermod -a -G dialout user
    #   sudo usermod -a -G tty user
    #   sudo usermod -a -G lp user
    #   ls -la /dev/usb/

   

    # image = 384 x 175  -- print area =  384 x 154 
    p.image("img.png")

    return render_template('index.html')
