import io
from flask import Flask
from flask import request
from flask import render_template, send_file

from virgool import Virgool
from virgoolak import Type1


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/api/v1/tag/virgool', methods=['GET'])
def tag_virgool():
    if request.method == 'GET':
        v = Virgool(request.args.get('url'))
        virgoolak1 = Type1(avatar=v.get_avatar(), 
                           name=v.get_name(), 
                           bio=v.get_bio(), 
                           title=v.get_title(), 
                           poster=v.get_poster())
        return send_file(
            io.BytesIO(virgoolak1.byte_array()),
            mimetype='image/png',
            as_attachment=True,
            attachment_filename='virgoolak.png')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
