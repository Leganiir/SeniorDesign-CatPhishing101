
def blacklist(email):
    blacklist = ["wermink.com", "beaconmessenger.com", "lyft.live", "socam.me", "tutuapp.bid", "yogrow.co", "afia.pro", "clout.wiki",
                 "hexi.pics", "wisnick.com", "weirby.com"
    ]
    domain = email.split("@")[1]
    
    #Searches through the blacklist database, it the domain is a match, it returns a boolian true, otherwise it returns a false.
    for domains in blacklist:
        if domain == domains:
            blacklist = True
            break
        else:
            blacklist = False 
            
    return blacklist
    
#This code is just for testing, can ignore.
test = blacklist("fotapek847@wisnick.com")
print(test)
test = blacklist("isaacleganik@gmail.com")
print(test)







#################
Edited by zaid

def blacklist(email):
    blacklist = ["wermink.com", "beaconmessenger.com", "lyft.live", "socam.me", "tutuapp.bid", "yogrow.co", "afia.pro", "clout.wiki",
                 "hexi.pics", "wisnick.com", "weirby.com"]
    
    domain = email.split("@")[1]
    
    # Searches through the blacklist database, if the domain is a match, it returns a boolean True, otherwise it returns a False.
    for domains in blacklist:
        if domain == domains:
            return True
    
    return False

# Input email address from the user
user_email = input("Enter your email address: ")

# Call the blacklist function and print the result
is_blacklisted = blacklist(user_email)

if is_blacklisted:
    print("The email domain is blacklisted.")
else:
    print("The email domain is not blacklisted.")
