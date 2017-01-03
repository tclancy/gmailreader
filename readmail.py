import gmail

try:
    from credentials import username, password
except ImportError:
    print "You need to create a file named 'credentials.py' in this folder with two variables: username and password"

if __name__ == '__main__':
    g = gmail.login(username, password)
    print g.inbox().mail()
