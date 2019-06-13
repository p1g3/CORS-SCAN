import requests
from threading import Thread,activeCount
from queue import Queue
from sys import argv

def cors_test(domain):
        if 'http://' or 'https://' not in domain:
                domain = 'http://' + domain.strip()
        try:
                characters = '!@#$%^&*()_+~/*'
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                'Origin': '{}'.format('http://www.abc.com')
                }
                req1 = requests.get(domain,headers=headers,timeout=(5,20),verify=False,allow_redirects=False)
                if "Access-Control-Allow-Origin" and "Access-Control-Allow-Credentials" in req1.headers:
                        if req1.headers['Access-Control-Allow-Origin'] == headers['Origin']:
                                print('[+]Mode 1：CORS Found {} {} {}'.format(domain.replace('http://',''),req1.headers['Access-Control-Allow-Origin'],req1.headers['Access-Control-Allow-Credentials']))
                                with open('cors_success.txt','a+') as f:
                                        f.write('{} {} {} \n'.format(domain.replace('http://',''),req1.headers['Access-Control-Allow-Origin'],req1.headers['Access-Control-Allow-Credentials']))
                        else:
                                headers['Origin'] = domain + '.baidu.com'
                                req2 = requests.get(domain,headers=headers,timeout=(5,20),verify=False,allow_redirects=False)
                                if req2.headers['Access-Control-Allow-Origin'] == headers['Origin']:
                                        print('[+]Mode 2：CORS Found {} {} {}'.format(domain.replace('http://',''),req2.headers['Access-Control-Allow-Origin'],req2.headers['Access-Control-Allow-Credentials']))
                                        with open('cors_success.txt','a+') as f:
                                                f.write('{} {} {} \n '.format(domain.replace('http://',''),req2.headers['Access-Control-Allow-Origin'],req2.headers['Access-Control-Allow-Credentials']))
                                else:
                                        for character in characters:
                                                headers['Origin'] = domain + character + '.baidu.com'
                                                req3 = requests.get(domain,headers=headers,timeout=(5,20),verify=False,allow_redirects=False)
                                                if req3.headers['Access-Control-Allow-Origin'] == headers['Origin']:
                                                        print('[+]Mode 3：CORS Found {} {} {}'.format(domain.replace('http://',''),req3.headers['Access-Control-Allow-Origin'],req3.headers['Access-Control-Allow-Credentials']))
                                                        with open('cors_success.txt','a+') as f:
                                                                f.write('{} {} {} \n').format(domain.replace('http://',''),req3.headers['Access-Control-Allow-Origin'],req3.headers['Access-Control-Allow-Credentials'])
                                                else:
                                                        if req.headers['Access-Control-Allow-Origin']:
                                                                print('[+]maybe CORS Found {} {} {}'.format(domain.replace('http://',''),req3.headers['Access-Control-Allow-Origin'],req3.headers['Access-Control-Allow-Credentials']))

        except Exception as e:
                print('[-]' + domain.replace('http://','') + ' ' +  str(e))
                pass

if __name__ == '__main__':
        try:
                if argv[1]:
                        queue = Queue()
                        filename = open(argv[1],'r+')
                        for url in filename:
                                queue.put(url.strip())
                        filename.close()
                        while queue.qsize()>0:
                                if activeCount()<= 10:
                                        Thread(target=cors_test,args=(queue.get(),)).start()
        except IndexError:
                print('Usage：python3 cors_test.py filename.txt')