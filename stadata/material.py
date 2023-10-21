import requests

class Material(object):
    DATA=None
    CONTENT=None
    
    def __init__(self, data):
        self.DATA=data
        response = requests.get(data['pdf'])
        self.CONTENT = response.content
        
        
    def desc(self):
        return self.DATA

    def download(self,url):
        pdf = open(url+"/"+self.DATA['title']+".pdf", 'wb')
        pdf.write(self.CONTENT)
        pdf.close()
        print("Download content success")