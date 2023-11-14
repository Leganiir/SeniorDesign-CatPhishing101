import language_tool_python
import app, re

#First read to look for the domain in our blocklist
def read_email(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            Email_Sender = re.search(r'From:\s*(?:.*<([^>]+)>)', line)
            if Email_Sender:
                return receive3(Email_Sender)

#Gets the header again so that it can be output
def GetHeaderForOutput(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            Email_Sender = re.search(r'From:\s*(?:.*<([^>]+)>)', line)
            if Email_Sender:
                return Email_Sender.group(1).split("@")[1]

#Gets the subjectline to check for grammer
def CheckSubjectGrammer(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            Email_Subject = re.search(r'Subject: (.*)', line)
            if Email_Subject:
                Email_Subject = Email_Subject.group(1)
                return GrammerChecker(Email_Subject)
                
#Sends to Grammerchecker        
def receive(content):
    return GrammerChecker(content)

#Gets from manual input and sends to check for blocklist
def receive2(header):
    domain = header.split("@")[1]
    return BlockList(domain)

#Gets from read_email and sends to check for blocklist
def receive3(header):
    domain = header.group(1).split("@")[1]
    return BlockList(domain)

def GrammerChecker(emailcontents):
    tool = language_tool_python.LanguageTool('en-US')
    Grammer = tool.check(emailcontents)
    if len(Grammer) >= 2:
        return 2
    else:
        return 1

def BlockList(emailheader):
    with open('disposable_email_blocklist.conf') as BlockList:
        BlockList_content = {line.rstrip() for line in BlockList.readlines()}
    if emailheader in BlockList_content:
        print("Email found to be a throwaway!")
        return 2
    else:
        return 1
    