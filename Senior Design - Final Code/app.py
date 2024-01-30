from flask import Flask, render_template, redirect, url_for, request, make_response, session
import seniordesigncode
import os

app = Flask(__name__)
app.static_folder = 'static'

result = DomainReason = GrammerReason = DKIMReason = SPFReason = DMARCReason = ""

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
    global result, DomainReason, GrammerReason, DKIMReason, SPFReason, DMARCReason
    
    if any(value != " " for value in [result, DomainReason, GrammerReason, DKIMReason, SPFReason, DMARCReason]):
        result = DomainReason = GrammerReason = DKIMReason = SPFReason = DMARCReason = ""
        
    return render_template('CheckEmail.html')

@app.route('/CheckEmailUpload.html')
def CheckEmailTemplate():
    response = make_response(render_template('CheckEmailUpload.html', result=result, DomainReason=DomainReason, GrammerReason=GrammerReason, DKIMReason=DKIMReason, SPFReason=SPFReason, DMARCReason=DMARCReason))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/CheckEmailUpload/upload', methods=['POST'])
def upload():
    global result, DomainReason, DKIMReason, SPFReason, DMARCReason
    
    if 'file' in request.files:
        file = request.files['file']
        file_path = 'uploads/' + file.filename
        file.save(file_path)
        
        try:
            CheckingResult = seniordesigncode.read_email(file_path)
            Sender = seniordesigncode.GetHeaderForOutput(file_path)
            EmailHeaders = seniordesigncode.CheckEmailHeaders(file_path)
            DKIMResult, SPFResult, DMARCResult = EmailHeaders[:3]
            
            DomainReasonMessages = {
                1: "The email domain: '{}' appears in our blocklist",
                2: "The domain: '{}' is a legitimate insurance address",
                3: "The domain: '{}' is a legitimate company address",
                4: "The domain: '{}' is from a legitimate domain, but not a registered company",
                5: "The domain: '{}' is a legitimate bank",
                6: "The domain: '{}' is not found in our database"
            }
            DKIMMessages = {
                1: "Message has not been tampered with.",
                2: "Message has been tampered with!",
                0: "Missing DKIM header.",
            }
            SPFMessages = {
                1: "Email was authorized to be sent.",
                2: "Email was not authorized to be sent!",
                0: "Missing SPF header.",
            }
            DMARCMessages = {
                1: "Authentication mechanisms passed.",
                2: "Authentication mechanisms failed!",
                0: "Missing DMARC header.",
            }
            DomainReason = DomainReasonMessages.get(CheckingResult, "").format(Sender)
            DKIMReason = DKIMMessages.get(DKIMResult, "")
            SPFReason = SPFMessages.get(SPFResult, "")
            DMARCReason = DMARCMessages.get(DMARCResult, "")
            
            if CheckingResult not in {1, 6, 4} and DKIMResult == 1 and SPFResult == 1 and DMARCResult == 1:
                result = "Email is likely safe"
            elif CheckingResult == 1 or DKIMResult == 2 or SPFResult == 2 or DMARCResult == 2:
                result = "Email is dangerous!"
            elif CheckingResult in {6, 4} and DKIMResult not in {2} and SPFResult not in {2} and DMARCResult not in {2}:
                result = "Email is suspicious, procede with caution"
            else:
                result = "Email is suspicious, avoid if possible"
            
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

    header = request.json.get('Header')
    print("Email Header:", header)

    GrammerResult = seniordesigncode.GrammerChecker(content)
    BlockListResult = seniordesigncode.BlockList(header)

    global result, DomainReason, GrammerReason
    
    DomainReasonMessages = {
                1: "The email domain: '{}' appears in our blocklist",
                2: "The domain: '{}' is a legitimate insurance address",
                3: "The domain: '{}' is a legitimate company address",
                4: "The domain: '{}' is from a legitimate domain, but not a registered company",
                5: "The domain: '{}' is a legitimate bank",
                6: "The domain: '{}' is not found in our database"
            }
    GrammerReasonMessages = {
                1: "This email contains grammer errors",
                2: "This email contains no grammer errors",
                3: "No email content found"
    }
    
    DomainReason = DomainReasonMessages.get(BlockListResult, "").format(header)
    GrammerReason = GrammerReasonMessages.get(GrammerResult, "")
    
    if BlockListResult not in {1, 6, 4} and GrammerReason == 2 or GrammerReason == 3:
        result = "Email is likely safe"
    elif BlockListResult == 1 or GrammerReason == 1:
        result = "Email is dangerous!"
    else:
        result = "Email is suspicious, procede with caution."
        
    return("Success!")
                
                


if __name__ == '__main__':
    app.run(debug=True)