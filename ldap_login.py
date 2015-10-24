import ldap
import getpass
import easygui as eg
## first you must open a connection to the server
def login ():

    try:
        rollno=None
        result = False
        l = ldap.open("ldap.iitb.ac.in")
        l.protocol_version = ldap.VERSION3	
    except ldap.LDAPError, e:
        print e
	
	# handle error however you like
    



    msg = "Enter LDAP Credentials"
    title = "Printer Login"
    fieldNames = ["Username * ", "Password * "]
    fieldValues = []  # we start with blanks for the values
    fieldValues = eg.multpasswordbox(msg,title, fieldNames)
 
     # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a mandatory field.' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = eg.multpasswordbox(errmsg, title, fieldNames, fieldValues) 

## The next lines will also need to be changed to support your search requirements and directory
    baseDN = "dc=iitb,dc=ac,dc=in"
    searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
    retrieveAttributes = ["dn"]
    uid=fieldValues[0].strip()
    searchFilter = '(uid='+uid+')'
    dn=None

    try:
        search_output= l.search_s(baseDN, searchScope, searchFilter)
        if not search_output:
            eg.msgbox(title="Invalid credentials", msg='Invalid Username')
        for dne,entry in search_output:
            dn=dne
            rollno=entry['employeeNumber'][0]
            password=fieldValues[1].strip()
            l.bind_s(dn,password)
            result= 'uid='+uid in l.whoami_s()

            print rollno
    except ldap.LDAPError, e:
        #print e
        eg.msgbox(title=e.message.get('desc'), msg='Invalid Password')
    return rollno, result
#[rollno,match]= login()
#print rollno,match