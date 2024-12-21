import requests, re, os, sys
from urllib.request import urlopen

def clear(): os.system('cls' if 'win' in sys.platform.lower() else 'clear')

def Author():
    print('__________.__        __                                 _        ')
    print('\______   \__| _____/  |_  ___________   ____   _______/  |_     ')
    print(' |     ___/  |/    \   __\/ __ \_  __ \_/ __ \ /  ___/\   __\    ')
    print(' |    |   |  |   |  \  | \  ___/|  | \/\  ___/ \___ \  |  |      ')
    print(' |____|   |__|___|  /__|  \_____>__|    \___  >____  > |__|      ')
    print('                  \/                        \/     \/            ')
    print('                            Downloader                           ')
    print('                     Coded By Sidiq Brewstreet                   ')
    print('                                                                 ')

class Pinterest:
    def __init__(self):
        self.ses   = requests.Session()
        self.pinid = []
        self.loop  = 0
        self.ok    = 0
        
    def GetID(self, url):
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
        response = self.ses.get(url, headers=headers).text
        self.ImageID = re.search(r'"pinId":"(\d+)"', str(response)).group(1)
        entryid = re.search(r'"imageSpec_orig":{"url":"(.*?)"', str(response)).group(1)
        self.pinid.append(entryid)
        self.loop +=1
        print('\r~ Mengumpulkan {} Foto '.format(self.loop), end='')
        self.cookies   = ";".join([key+"="+value.replace('"','') for key, value in self.ses.cookies.get_dict().items()])
        self.csrftoken = re.search(r'csrftoken=(.*?);', str(self.cookies)).group(1)

    def GetHASH(self):
        headers = {'Origin': 'https://id.pinterest.com','sec-ch-ua-platform': '"Windows"','Referer': 'https://id.pinterest.com/','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0'}
        response = self.ses.get('https://s.pinimg.com/webapp/app-www-closeup-duplo-UnauthCloseupRelatedPins.id_ID-323f901fe0ab66c0.mjs', headers=headers).text
        self.queryhash = re.findall(r'params:{id:"(.*?)",metadata', str(response))
        self.Dumps(self.queryhash[1], None)

    def Dumps(self, queryhash, nextpage):
        headers   = {'accept': 'application/json','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','content-type': 'application/json','origin': 'https://id.pinterest.com','priority': 'u=1, i','referer': 'https://id.pinterest.com/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.205", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','x-csrftoken': self.csrftoken,'x-pinterest-appstate': 'active','x-pinterest-graphql-name': 'UnauthCloseupRelatedPinsFeedQuery','x-pinterest-pws-handler': 'www/pin/[id].js','x-pinterest-source-url': '/pin/{}/'.format(self.ImageID),'x-requested-with': 'XMLHttpRequest'}
        json_data = {'queryHash': queryhash,'variables': {'pinId': self.ImageID,'count': 50,'cursor': nextpage,'source': None,'searchQuery': None,'topLevelSource': None,'topLevelSourceDepth': None,'contextPinIds': None,'isDesktop': True,'showMultiColumnBoardRecommendationModule': True,'showMultiColumnRelatedIdeasModule': False}}
        try:
            response = self.ses.post('https://id.pinterest.com/_/graphql/', cookies={'cookie': self.cookies}, headers=headers, json=json_data).text
            hashpage = re.search(r'"hasNextPage":(.*?)}}}', str(response)).group(1)
            if 'upstream request timeout' in str(response):
                self.Dumps(queryhash=queryhash, nextpage=endcursor)
            else:
                entryid   = re.findall(r'"url":"https://i.pinimg.com/originals/(.*?)"', str(response))
                for x in entryid:
                    if os.path.basename(x) in self.pinid or x in self.pinid: pass
                    else:
                        self.loop +=1
                        self.pinid.append('https://i.pinimg.com/originals/'+x)
                        print('\r~ Mengumpulkan {} Foto '.format(self.loop), end='')
                endcursor = re.search(r'"endCursor":"(.*?)"', str(response)).group(1)            
                if hashpage == 'true':
                    self.Dumps(queryhash=self.queryhash[0], nextpage=endcursor)
                else:
                    print(f'\r[*] Berhasil Mengumpulkan {len(self.pinid)} Foto', end='')
                    self.Download_Foto()
        except KeyboardInterrupt:
            print(f'\r[*] Berhasil Mengumpulkan {len(self.pinid)} Foto', end='')
            self.Download_Foto()

    def Download_Foto(self):
        path = 'results'
        os.makedirs(path, exist_ok=True)
        print('')
        total = int(input('[?] Berapa Jumlah Foto Yang Ingin Diunduh ? : '))
        print('')
        try:
            for x in self.pinid[:total]:
                foto = urlopen(x).read()
                with open(f'{path}/{os.path.basename(x)}', 'wb') as r:
                    r.write(foto)
                r.close()
                self.ok +=1
                print('\r~ Berhasih Mengunduh {} Foto   '.format(self.ok), end='')
            print('\r[*] Berhasih Mengunduh {} Foto   '.format(self.ok), end='')
            print('')
            print('[*] Foto Tersimpan Di Folder {}   '.format(path), end='')
        except KeyboardInterrupt:
            print('')
            exit('\r[*] Foto Tersimpan Di Folder {}   '.format(path), end='')

if __name__ == '__main__':
    try:
        clear()
        Author()
        print()
        print('[*] Contoh Link "https://id.pinterest.com/pin/28429041392942765/", "https://pin.it/5gNMILbB8"')
        print('[*] 1 Link Bisa Dumps lebih dari 10.000 Foto')
        url = input('[?] Masukan Link Pinterest : ')
        print('')
        print('  Tekan CTRL + C Untuk Berhenti  ')
        print('')
        lo = Pinterest()
        lo.GetID(url=url)
        lo.GetHASH()
    except KeyboardInterrupt: exit()
