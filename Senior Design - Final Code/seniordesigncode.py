import language_tool_python
import app, re, email.utils

#First read to look for the domain in our blocklist
def read_email(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'From:\s*(?:.*<([^>\d]+)>)', line)
            match2 = re.search(r'From: .*?<(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>', line)
            match3 = re.search(r'From: .*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
            if match or match2 or match3:
                if match:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match.group(1))
                elif match2:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match2.group(1))
                elif match3:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match3.group(1))
                if Email_Sender:
                    Email_Sender = Email_Sender.group()
                    return BlockList(Email_Sender)

#Gets the header again so that it can be output
def GetHeaderForOutput(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'From:\s*(?:.*<([^>\d]+)>)', line)
            match2 = re.search(r'From: .*?<(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>', line)
            match3 = re.search(r'From: .*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
            if match or match2 or match3:
                if match:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match.group(1))
                elif match2:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match2.group(1))
                elif match3:
                    Email_Sender = re.search(r'[\w\.-]+@[\w\.-]+', match3.group(1))
                if Email_Sender:
                    Email_Sender = Email_Sender.group()
                    return(Email_Sender)

#Gets the subjectline to check for grammer
def CheckSubjectGrammer(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            Email_Subject = re.search(r'Subject: (.*)', line)
            if Email_Subject:
                Email_Subject = Email_Subject.group(1)
                return GrammerChecker(Email_Subject)

def CheckEmailHeaders(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        DKIMValues = [] 
        SPFValues = []
        DMARCValues = []
        DKIMStatus= re.findall(r'dkim=(pass|fail)', content, re.DOTALL)
        SPFStatus = re.findall(r'spf=(pass|fail)', content, re.DOTALL)
        DMARCStatus = re.findall(r'dmarc=(pass|fail)', content, re.DOTALL)
        if DKIMStatus:
            for match in DKIMStatus:
                DKIMValues.append(match)
        if SPFStatus:
            for match in SPFStatus:
                SPFValues.append(match)
        if DMARCStatus:
            for match in DMARCStatus:
                DMARCValues.append(match)
                
        if "fail" in DKIMValues:
            DKIMStatus = 2
        elif not DKIMValues:
            DKIMStatus = 0  
        else:
            DKIMStatus = 1
            
        if "fail" in SPFValues:
            SPFStatus = 2
        elif not SPFValues:
            SPFStatus = 0
        else:
            SPFStatus = 1 

        if "fail" in DMARCValues:
            DMARCStatus = 2
        elif not DMARCValues:
            DMARCStatus = 0
        else:
            DMARCStatus = 1
        
        return DKIMStatus, SPFStatus, DMARCStatus

def GrammerChecker(emailcontents):
    tool = language_tool_python.LanguageTool('en-US')
    Grammer = tool.check(emailcontents)
    if not emailcontents:
        return 3
    elif len(Grammer) >= 2:
        return 1
    else:
        return 2

def BlockList(emailheader):
    domain = emailheader.split("@")[1]
    with open('disposable_email_blocklist.conf') as BlockList:
        BlockList_content = {line.rstrip() for line in BlockList.readlines()}
    with open('insurance_database.conf') as Insurance:
        Insurance_content = {line.rstrip() for line in Insurance.readlines()}
    with open('shipping_companies.conf') as Shipping:
        Shipping_content = {line.rstrip() for line in Shipping.readlines()}
    with open('Trusted-domains.conf') as Trusted:
        Trusted_content = {line.rstrip() for line in Trusted.readlines()}
    with open('bank_database.conf') as Bank:
        Bank_content = {line.rstrip() for line in Bank.readlines()}
    if domain in BlockList_content:
        print("Email found to be a throwaway!")
        return 1
    elif emailheader in Insurance_content:
        print("Email found to be Insurance")
        return 2
    elif emailheader in Shipping_content:
        print("Email found to be shipping")
        return 3
    elif emailheader in Trusted_content:
        print("Trusted Domain Found")
        return 4
    elif emailheader in Bank_content:
        print("Banking Domain Found")
        return 5
    else:
        return 6