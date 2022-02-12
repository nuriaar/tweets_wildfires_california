'''
Pavan and Jonas

Script to get Twitter Data
'''
import twint
# Configure
c = twint.Config()
c.Username = "MichelleObama"

# Run
twint.run.Search(c)