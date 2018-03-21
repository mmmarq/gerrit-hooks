import re
import subprocess
from suds.client import Client

MANTIS_URL = "http://mantis.raspberry.pi/mantisbt/api/soap/mantisconnect.php?wsdl"
MANTIS_USER = "admin"
MANTIS_PASSWORD = "raspberry"
MANTIS_ASSIGNED_STATUS = 50

# CHECK IF BUG STATUS IS 50 (ASSIGNED)
def check_bug_assigned_status(bugid):
   client = Client(MANTIS_URL)
   bugdata = client.service.mc_issue_get(MANTIS_USER,MANTIS_PASSWORD,bugid)
   if bugdata.status.id == MANTIS_ASSIGNED_STATUS:
      return True
   else:
      return False

# ADD GERRIT CHANGE URL INTO MANTIS CUSTOM FIELD
def add_gerrit_change_url(bugid,fieldid,changeUrl):
   client = Client(MANTIS_URL)
   bugdata = client.service.mc_issue_get(MANTIS_USER,MANTIS_PASSWORD,bugid)
   if bugdata.status.id == MANTIS_ASSIGNED_STATUS:
      t_field = None
      for custom_field in bugdata.custom_fields:
         if custom_field.field.id == fieldid:
            t_field = custom_field
      bugdata.custom_fields = []
      if not t_field == None:
         if t_field.value == None:
            t_field.value = ''
         if re.search(changeUrl,t_field.value) == None:
            value = t_field.value + ' ' + changeUrl
            lvalue = value.split()
            lvalue.sort(key=lambda link: int(link.split('/')[-1]))
            t_field.value = ' '.join(lvalue)
            bugdata.custom_fields.append(t_field)
            client.service.mc_issue_update(MANTIS_USER,MANTIS_PASSWORD,bugid,bugdata)
         return True
      else:
         print "Gerrit custom field not found"
         return False
   else:
      print "CR not in Assigned status"
      return False

# REMOVE GERRIT CHANGE URL INTO MANTIS CUSTOM FIELD
def remove_gerrit_change_url(bugid,fieldid,changeUrl):
   client = Client(MANTIS_URL)
   bugdata = client.service.mc_issue_get(MANTIS_USER,MANTIS_PASSWORD,bugid)
   if bugdata.status.id == MANTIS_ASSIGNED_STATUS:
      t_field = None
      for custom_field in bugdata.custom_fields:
         if custom_field.field.id == fieldid:
            t_field = custom_field
      bugdata.custom_fields = []
      if not t_field == None:
         if t_field.value == None:
            t_field.value = ''
         if re.search(changeUrl,t_field.value) != None:
            value = t_field.value.replace(changeUrl, '')
            lvalue = value.split()
            lvalue.sort(key=lambda link: int(link.split('/')[-1]))
            t_field.value = ' '.join(lvalue)
            bugdata.custom_fields.append(t_field)
            client.service.mc_issue_update(MANTIS_USER,MANTIS_PASSWORD,bugid,bugdata)
         return True
      else:
         print "Gerrit custom field not found"
         return False
   else:
      print "CR not in Assigned status"
      return False

# ADD MANTIS NOTE
def add_gerrit_note(bugid,note):
   client = Client(MANTIS_URL)
   user = client.service.mc_login(MANTIS_USER,MANTIS_PASSWORD)
   note_field = client.factory.create('IssueNoteData')
   note_field.text = note
   note_field.reporter = user.account_data
   client.service.mc_issue_note_add(MANTIS_USER,MANTIS_PASSWORD,bugid,note_field)

# GET CURRENT COMMIT MESSAGE
def get_commit_message(gitDir,sha1):
   command = "git --git-dir=" + gitDir + " log " + sha1 + " --oneline -1"
   p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   cmd_out, cmd_p = p.communicate()
   return ' '.join(cmd_out.split(' ')[1:])

# GET LIST WITH ALL GERRITS
def get_gerrit_list(bugid,fieldid):
   client = Client(MANTIS_URL)
   bugdata = client.service.mc_issue_get(MANTIS_USER,MANTIS_PASSWORD,bugid)
   if bugdata.status.id == MANTIS_ASSIGNED_STATUS:
      t_field = None
      for custom_field in bugdata.custom_fields:
         if custom_field.field.id == fieldid:
            t_field = custom_field
      if not t_field == None:
         return t_field.value.split()
      else:
         print "Gerrit custom field not found"
         return []
   else:
      print "CR not in Assigned status"
      return []

# CHECK IF BUG EXISTIS
def check_if_bug_exist(bugid):
   client = Client(MANTIS_URL)
   bugdata = client.service.mc_issue_exists(MANTIS_USER,MANTIS_PASSWORD,bugid)
   return bugdata
