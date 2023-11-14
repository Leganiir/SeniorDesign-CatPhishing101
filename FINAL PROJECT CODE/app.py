from flask import Flask, render_template, redirect, url_for, request, make_response
import seniordesigncode
import os

app = Flask(__name__)
app.static_folder = 'static'  # Set the static folder to 'static'
result = " "
DomainReason = " "
GrammerReason = " "

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index2():
    return render_template('index.html')

@app.route('/help.html')
def help():
    return render_template('help.html')

@app.route('/CheckEmail.html')
def CheckEmail():
    return render_template('CheckEmail.html')

@app.route('/CheckEmailUpload.html')
def CheckEmailTemplate():
    response = make_response(render_template('CheckEmailUpload.html', result=result, DomainReason=DomainReason, GrammerReason=GrammerReason))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/CheckEmailUpload/upload', methods=['POST'])
def upload():
    global result
    global DomainReason
    global GrammerReason
    if 'file' in request.files:
        file = request.files['file']
        file_path = 'uploads/' + file.filename
        file.save(file_path)
        
        try:
            CheckingResult = seniordesigncode.read_email(file_path)
            Header = seniordesigncode.GetHeaderForOutput(file_path)
            #SubjectResult = seniordesigncode.CheckSubjectGrammer(file_path)
            if CheckingResult == 2:
                result = "This email is dangerous!"
                DomainReason = "The email domain: '" + str(Header) + "' appears in out blocklist"
            else:
                result = "This email is safe."
                DomainReason = "The domain: '" + str(Header) + "' has matched an indexed address."
            #elif CheckingResult == 1 and SubjectResult == 1:
                #result = "This email is safe."
                #DomainReason = "The domain: '" + str(Header) + "' has matched an indexed address."
                #GrammerReason = "The email returned no subject spelling mistakes"
            #elif CheckingResult == 1 and SubjectResult == 2:
                #result = "This email is suspicious"
                #DomainReason = "The domain: '" + str(Header) + "' has matched an indexed address."
                #GrammerReason = "But there is a spelling mistake in the subject. Procede with caution"
            #elif CheckingResult == 2 and SubjectResult == 2:
                #result = "This email is dangerous!"
                #DomainReason = "The email domain: '" + str(Header) + "' appears in out blocklist"
                #GrammerReason = "There is a spelling mistake in the subject. Procede with caution"
            os.remove(file_path)
            return "Success!"

        except Exception:
            return "Failure!"

@app.route('/CheckEmailManual.html')
def CheckEmailTemplate2():
    response = make_response(render_template('CheckEmailManual.html', result=result, DomainReason=DomainReason, GrammerReason=GrammerReason))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/CheckEmailManual', methods=['POST'])
def submit():
    content = request.json.get('Content')
    print("Email Content:", content)
    # Further processing with the input can be done here
    header = request.json.get('Header')
    print("Email Header:", header)
    # Further processing with the input can be done here
    GrammerResult = seniordesigncode.receive(content)
    BlockListResult = seniordesigncode.receive2(header)

    global result
    result = GrammerResult + BlockListResult
    global DomainReason
    global GrammerReason
    
    if result >= 3:
        result = "This email is suspicious, please proceed with caution due to:"
    elif result >= 4:
        result = "This email is highly likely to be a scam due to:"
    else:
        result = "Email appears safe due to:"
    
    if GrammerResult == 1:
        GrammerReason = "There were no returns on spelling mistakes."
    else:
        GrammerReason = "There was a return on spelling mistakes."
        
    if BlockListResult == 1:
        DomainReason = "The email domain " + str(header) + " appears legitimate"
    else:
        DomainReason = "The email domain " + str(header) + " appears in our blocklist"
        
    return "Success!"


if __name__ == '__main__':
    app.run(debug=True)