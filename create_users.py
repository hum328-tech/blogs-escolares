"""Requires pip install firebase-admin; GOOGLE_APPLICATION_CREDENTIALS=private/service-account.json python tools/create_users.py"""
import firebase_admin,json,pathlib,secrets,string,unicodedata,re,csv
from firebase_admin import auth,firestore
firebase_admin.initialize_app();db=firestore.client()
root=pathlib.Path(__file__).resolve().parent.parent
rows=json.loads((root/'private'/'import-data.json').read_text(encoding='utf-8'))
chars=string.ascii_letters+string.digits+'!@#'
creds=[]
for row in rows:
 username=row['id'][:40];password=''.join(secrets.choice(chars) for _ in range(14));email=username+'@alumnos.blogs.invalid'
 try:user=auth.get_user_by_email(email);print('Existing account',username,'(password unchanged)');continue
 except auth.UserNotFoundError:pass
 user=auth.create_user(email=email,password=password,display_name=row['name'])
 db.collection('users').document(user.uid).set({'name':row['name'],'username':username,'blogId':row['id'],'role':'student','active':True})
 creds.append({'name':row['name'],'username':username,'password':password})
with (root/'private'/'credentials.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=['name','username','password']);w.writeheader();w.writerows(creds)
print('Created',len(creds),'accounts. Keep private/credentials.csv secret.')
