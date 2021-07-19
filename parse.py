import json

def parseUsersJsonToCSV(filename): 
    f = open(filename, 'r')
    data = json.load(f)
    print("samAccountName,displayName,description,dn,groupcount,groups,lastLogonTimestamp")
    for item in data: 
        if "sAMAccountName" in item["attributes"]: 
            samAccountName = item["attributes"]["sAMAccountName"][0]
        else: 
            samAccountName = ""
        if "displayName" in item["attributes"]: 
            displayName = item["attributes"]["displayName"][0]
        else: 
            displayName = ""
        if "description" not in item["attributes"]: 
            description = ""
        else: 
            description = item["attributes"]["description"][0]
            # escape sequences to make CSV parsable
            description = description.replace('"', '""')
            description = description.replace('\r\n', '. ')
            description = description.replace('\n', '. ')
        
        if "memberOf" not in item["attributes"]: 
            groups = ""
            groupcount=0
            grouplist=""
        else: 
            groups = item["attributes"]["memberOf"]
            groupcount = len(groups)
            grouplist = []
            for group in groups: 
                grouplist.append(group.split(',')[0].split('=')[1])
        dn = item["dn"]
        
        if "lastLogonTimestamp" in item["attributes"]: 
            lastLogonTimestamp = item["attributes"]["lastLogonTimestamp"][0]
        else: 
            continue # never logged in before, probably dont care
        print('"{}","{}","{}","{}","{}","{}","{}"'.format(samAccountName,displayName,description,dn,groupcount,', '.join(grouplist),lastLogonTimestamp))

def parseGroupsJsonToCSV(filename):
    f = open(filename, 'r')
    data = json.load(f)
    print("cn,description,membercount,memberlist,dn")
    for item in data: 
        if "member" not in item["attributes"]: #no members
            continue #we dont care about this group if there are no members

        cn = item["attributes"]["cn"][0]
        if "description" in item["attributes"]: 
            description = item["attributes"]["description"][0]
            description = description.replace('"', '""')
            description = description.replace('\r\n', '. ')
            description = description.replace('\n', '. ')
        else: 
            description = ""
        dn = item["dn"]
        members = item["attributes"]["member"]
        membercount = len(members)
        memberlist = []
        for member in members: 
            memberlist.append(member.split(',')[0].split('=')[1])
        if len(memberlist) > 3000: 
            memberlist = ""
        print('"{}","{}","{}","{}","{}"'.format(cn,description,membercount,', '.join(memberlist),dn))

def parseComputersJsonToCSV(filename):
    f = open(filename, 'r')
    data = json.load(f)
    print("cn, ")

parseUsersJsonToCSV("users.json.6")
#parseGroupsJsonToCSV("groups.json.3")

