from discover import *
urls=[('https://www.mdpi.com/2073-431X/14/4/128','sms3d.html'),('https://www.mdpi.com/2073-431X/14/5/199','m18k.html'),('https://api.crossref.org/works/10.1016/j.dib.2026.113085','rgbd_metadata.json'),('https://api.crossref.org/works/10.3390/computers14040128','sms3d_metadata.json'),('https://api.crossref.org/works/10.3390/computers14050199','m18k_metadata.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for r in ex.map(lambda p:fetch(*p),urls):print(r)
