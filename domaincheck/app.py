from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from check import full_search

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_domain():
    """
    Accept POST, check domain details for supplied
    domain
    """
    domain = request.form.get('domain')
    if not domain:
        print "form: ", request.form
        return BadRequest('No supplied domain!')
    
    res = full_search(domain)

    if not res['a'] and not res['mx'] and not res['nameservers']:
        return NotFound('No data for domain: %s' % domain)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
