import language_tool_python

 

def check_grammar(email_text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(email_text)

 

    total_words = len(email_text.split())
    grammar_mistake_percentage = (len(matches) / total_words) * 100

 

    print(f"Grammar mistake percentage: {grammar_mistake_percentage:.2f}%")

    if grammar_mistake_percentage > 5.0:  # Adjust the threshold as needed
        print("The email has a high percentage of grammar mistakes.")
        for match in matches:
            print(f"Message: {match.message}")
            print(f"Replacements: {match.replacements}")
    else:
        print("The email has an acceptable grammar percentage.")

 

if __name__ == "__main__":
    email = input("Please paste the email content here: ")
    check_grammar(email)
