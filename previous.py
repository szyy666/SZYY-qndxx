import requests,json
from main import headers,memberlist,ConverMidToXLToken
try:
    with open('result.json','r',encoding='utf8') as origin_file:
        origin=origin_file.read()
        origin=json.loads(origin)
except:
    pass
#往期课程刷积分
#获取季
for member in memberlist:
    try:
        print("=====往期课程打卡=====")
        headers['X-Litemall-Token']=ConverMidToXLToken(member)
        getChapterList = requests.get('https://youthstudy.12355.net/saomah5/api/young/course/list', headers=headers)
        chapterList=json.loads(getChapterList.text).get("data").get("list")
        saveOldHistory_output=''
        for chapter in chapterList:
            #获取期
            #print(chapter['id'])
            params = {
                'pid': chapter['id'],
            }
            getChapterDetail = requests.get('https://youthstudy.12355.net/saomah5/api/young/course/chapter/list', params=params, headers=headers)
            chapterDetail=json.loads(getChapterDetail.text).get('data').get('list')
            for chapterId in chapterDetail:
                data = {
                    'chapterId': chapterId['id'],
                }
                saveOldHistory = requests.post('https://youthstudy.12355.net/saomah5/api/young/course/chapter/saveHistory', headers=headers,data=data)
                print(json.loads(saveOldHistory.text).get('msg'),end="")
                saveOldHistory_output=saveOldHistory_output+json.loads(saveOldHistory.text).get('msg')
        print('\n')
        for result in origin:
            if result['member'] == member:
                result['result']+='<br><b>往期课程打卡：</b>'+saveOldHistory_output
    except:
        for result in origin:
            if result['member'] == member:
                result['result']+='<br><b>往期课程打卡：</b>失败'
    with open('result.json','w+',encoding='utf8') as new_file:
        new_file.write(json.dumps(origin))