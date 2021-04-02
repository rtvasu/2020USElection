import fire

manPage = """
- List of allowed commands:

1. votes:  tells you number of votes depending on the values specified under options:
    a. county
    b. state
    c. party

2. annotate: allows you to annotate counties as potential future wins or losses. Options:
    a. county
    b. potential: requires a value of win or loss

3. tweets: tells you number of votes depending on the values specified under options:
    a. county
    b. state
    c. party

4. profile: gives you a profile of the voters depending on the values specified under options:
    a. county
    b. state
    c. party
    d. category: requires a value of race, age, gender, income, or employed

5. model: shows you the list of factors that influenced the most influenced the vote to favor
one party over another

6. manual: shows you list of allowed commands and what they do

- Other Notes:

1. How to execute a command: for example, let's say you want to find out the number of votes from 
the Adams county in Nebraska for the Democratic party, you would execute: 
votes adams nebraska democratic

2. Assume options are required unless mentioned otherwise.
"""

class parse(object):
    def __init__(self):
        print("Hello! Execute command 'py -m parse manual' to see list of commands.")

    def manual(self):
        print(manPage)

    def votes(self, county, state, party):
        # put in your relevant sql code here
        print("hi")
    
    def tweets(self, county, state, party):
        # put in your relevant sql code here
        print("hi")
    
    def annotate(self, county, potential):
        # put in your relevant sql code here
        print("hi")
    
    def profile(self, county, state, party, category):
        # put in your relevant sql code here
        print("hi")
    
    def model(self):
        # run model here
        print("hi")

if __name__ == '__main__':
    fire.Fire(parse)