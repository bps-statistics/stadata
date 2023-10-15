import requests

class Material(object):
    def __init__(self, data):
        self.DATA = data

        # Download pdf
        response = requests.get(data['pdf'])
        # get pdf content
        self.CONTENT = response.content
        
    def desc(self):
        """
        Show material description
        """
        return self.DATA

    def download(self, url: str):
        """
        Download pdf file
        :param url: url to save pdf file
        """
        # open file in the url for writing
        with open(f"{url}/{self.DATA['title']}.pdf", 'wb') as pdf:
            # write pdf content to file
            pdf.write(self.CONTENT)
            
        print("Download content success")