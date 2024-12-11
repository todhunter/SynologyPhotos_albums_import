import requests
import os

#ignore ssl warnings
import warnings
warnings.filterwarnings("ignore")

#error 803 login (bad _sid)

#synology connect data
ip = ''
port = ''
username = ''
password = ''

#folder created by takeout-helper.exe
workDir = "C:\\Google_Photo_Takeout\\"
#src folder on synology /photo/Google_Photo_Takeout/"  
SynFotoFolder = "/Google_Photo_Takeout/"


def make_req(data):
    url = 'https://'+ip+':'+port+'/webapi/entry.cgi'
    response = requests.post(url, data=data, verify=False)
    return response.json()

def login(username, password):
    url = 'https://'+ip+':'+port+'/webapi/auth.cgi'
    data = {
    'api' :'SYNO.API.Auth',
    'version':'3',
    'passwd' : password,
    'account': username,
    'method': 'login'
    }

    response = requests.get(url, params = data, verify=False)
    #requests.post(url, data=data, verify=False)
    #print(response.json())
    return response.json()['data']['sid']
    
def find_folder(SynFotoFolderWanted):
    parent = 0
    found_path = ''
    folder = ''
    for part in SynFotoFolderWanted.strip('/').split('/'):
        data = {
        'api': 'SYNO.FotoTeam.Browse.Folder',
        'method': 'count',
        'offset': '0',
        'version': '2',
        'limit':'5000',
        'id': parent,
        '_sid': _sid
        }
        count_response = make_req(data)
        #print(parent, count_response)

        if count_response['success']:
            count = count_response['data']['count']
            for offset in range(0, count, 5000):
                data = {
                'api': 'SYNO.FotoTeam.Browse.Folder',
                'method': 'list',
                'offset': '0',
                'version': '2',
                'limit':'5000',
                'id': parent,
                '_sid': _sid
                }
                folders_response = make_req(data)
                
                #print("---------")
                #print(folders_response)
                #print("---------")
                #print(parent, found_path, part)

                if folders_response['success']:
                    folder = next(filter(lambda elem: elem['name'] == '%s/%s' % (found_path, part), folders_response['data']['list']), None)
                    if folder:
                        parent = folder['id']
                        found_path = folder['name']
                        #print("partial folder "+str(folder))
    return folder


_sid = login(username, password)
#print(_sid)

workDirPath = workDir.split(os.sep)


SynFotoFolderWanted = ""
SynoFotoAlbumName = ""
i = 0 
for root, dirs, files in os.walk(workDir):
    path = root.split(os.sep)
    
    SynFolderID = None
    SynFileID = None
    SynFileList = None
    SynAlbumID = None
    SynFotoIds = []

    for file in files:
        GPFotoAlbumName = path[len(workDirPath)]
        GFotoPath = path[len(workDirPath)+1:]
        SynFotoFolderWanted = SynFotoFolder + "/".join(GFotoPath)

        #print(SynFotoFolderWanted)
        #print(GPFotoAlbumName)
        if SynFolderID is None:
            SynFolderID = find_folder(SynFotoFolderWanted)
            print('Syno folder id: ',SynFolderID['id'], ' name:',  SynFolderID['name'])
            SynFolderID = SynFolderID['id']
            
        
        if SynFileList is None:
            data = {
            'api': 'SYNO.FotoTeam.Browse.Item',
            'method': 'list',
            'offset': '0',
            'version': '6',
            'folder_id': SynFolderID,
            'additional': '["thumbnail"]',
            'limit':'5000',
            '_sid': _sid
            }
            SynFileList = make_req(data)["data"]["list"]

                    

        GFotoFile = str(file.split(".")[0])
        #print(GFotoPath, GFotoFile)
        #print(SynFileList)
        for SynFile in SynFileList:
            #print(SynFile, " ", GFotoFile)
            if str(SynFile['filename'].split(".")[0]) == GFotoFile:
                if SynAlbumID is None:
                    isAlbumCreated = None
                    
                    data = {
                    'api': 'SYNO.Foto.Browse.Album',
                    'method': 'list',
                    'offset': '0',
                    'version': '5',
                    'limit':'5000',
                    '_sid': _sid
                    }
                    SynAlbumList = make_req(data)

                    for album in SynAlbumList["data"]["list"]:
                        #print(album["name"])
                        if album["name"] == GPFotoAlbumName:
                            isAlbumCreated = True
                            break
                        else:
                            isAlbumCreated = False
                        #print(isAlbumCreated)

                    #print(album)
                    if isAlbumCreated is True:
                        SynAlbumID = str(album["id"])
                        print('Syno album id: ',album["id"], ' name:',  album["name"])
                        
                    elif isAlbumCreated is False:
                        #print(GPFotoAlbumName)
                        #create album
                        data = {
                        'api': 'SYNO.Foto.Browse.NormalAlbum',
                        'method': 'create',
                        'version': '1',
                        'name': '"'+str(GPFotoAlbumName)+'"',
                        '_sid': _sid
                        }

                        album = make_req(data)["data"]["album"]
                        SynAlbumID = str(album["id"])
                        print('Created Syno album id: ',album["id"], ' name:',  album["name"])
                            
                SynFotoIds.append(SynFile["id"])
                #print(GFotoPath, GFotoFile, " -> syn file name: ", SynFile["filename"], " (syn album id: "+ SynAlbumID + " id: "+ str(SynFile["id"]) +" name: "+GPFotoAlbumName +")")
    if SynFotoIds != []:
        #adding to album
        data = {
        'api': 'SYNO.Foto.Browse.NormalAlbum',
        'method': 'add_item',
        'version': '3',
        'id': SynAlbumID,
        'item': str(SynFotoIds),
        '_sid': _sid
        }
        #print(data)
        print(SynFotoIds)
        make_req(data)
