"""Best-effort, unauthenticated access to the exact supplementary reference URL.
No executable content, credentials, login bypass or third-party mesh import.
Failure is recorded and does not prevent the independent bpy reconstruction.
"""
import urllib.request
import urllib.error
import json
import re
import html

URL='https://makerworld.com.cn/zh/models/900011-la-pu-lan-de-wu-qi-dao-ju-1-08mi-la-gou-cosdao-ju'

def probe(output):
    record={'url':URL,'third_party_mesh_imported':False,'license_verified':False}
    try:
        request=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(request,timeout=15) as response:
            body=response.read(2000000).decode('utf-8','replace')
            record['http_status']=response.status
            title=re.search(r'<title[^>]*>(.*?)</title>',body,re.I|re.S)
            record['page_title']=html.unescape(title.group(1)) if title else None
            record['page_bytes_read']=len(body.encode('utf-8'))
            record['public_page_read']=True
            urls=re.findall(r'<meta[^>]+(?:property|name)=[\"\']og:image[\"\'][^>]+content=[\"\']([^\"\']+)',body,re.I)
            record['preview_urls']=[html.unescape(x) for x in urls]
            record['note']='HTML metadata only. No model was downloaded, imported or redistributed.'
    except Exception as exc:
        record['public_page_read']=False
        record['error']=str(exc)
        record['note']='Access failed. The supplementary model could not be inspected through this route.'
    (output/'supplementary_reference_access.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    print('SUPPLEMENTARY_REFERENCE_ACCESS '+json.dumps(record,ensure_ascii=False))
