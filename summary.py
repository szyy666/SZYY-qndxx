import requests,json,main,time,os,re
with open('result.json','r',encoding='utf8') as origin_file:
    origin=origin_file.read()
origin=json.loads(origin)
pushdata={}
config=main.config
#推送渠道
pushdata['channel']=config['push']['channel']
pushdata['template']='html'

# 具体请查看pushplus api文档https://www.pushplus.plus/doc/guide/api.html
token=''

if token == '':
    try:
        token=os.environ['PUSHTOKEN']
    except:
        pass
LatestStudy=json.loads(requests.get('https://youthstudy.12355.net/saomah5/api/young/chapter/new',headers=main.headers).text)
StudyId=re.search('[a-z0-9]{10}',LatestStudy['data']['entity']['url']).group(0)
StudyName=LatestStudy['data']['entity']['name']
Finishpage='<a href="'+'https://finishpage.dgstu.tk/?id='+StudyId+'&name='+StudyName+'">（伪）当前期完成页</a><br>'
pushdata['content']=Finishpage

time.sleep(60)#平台统计有延迟
errorcount=0
for member in origin:
    if member['status']== 'error':
        errorcount+=1
        pushdata['content']+='<b>mid或X-Litemall-Token:</b>'+member['member']+'<br><b>状态:</b>'+'执行出错'+'<br>'
        continue
    XLtoken=main.ConverMidToXLToken(member['member'])
    profile=main.GetProfile(XLtoken)
    score_now=profile.score()
    score_add=score_now-member['score']
    if score_now < 100:
        score_need=100-score_now
    elif score_now < 200:
        score_need=200-score_now
    elif score_now < 500:
        score_need=500-score_now
    elif score_now < 1000:
        score_need=1000-score_now
    elif score_now < 5000:
        score_need=5000-score_now
    else:
        score_need=0
    member['result']+='<br>此次执行增加了<b>'+str(score_add)+'</b>积分'+'<br>当前为<b>'+profile.medal()+'</b>，距离下一徽章还需<b>'+str(score_need)+'</b>积分<br>'
    pushdata['content']+='<b>mid或X-Litemall-Token:</b>'+member['member']+'<br><b>名称:</b>'+member['name']+'<br>'+member['result']+'<br>'

#检查token
if ('token' in locals().keys()) == True:
    pass
else:
    exit('+===============+\n| Token未定义! |\n+===============+')

if errorcount!=len(main.memberlist):
    titledone=False
    for i in origin:
        if (i['status']!='error') and (i['status']!='passed'):
            if titledone==False:
                pushdata['title']='['+str(len(main.memberlist)-errorcount)+'/'+str(len(main.memberlist))+']'+i['status']+'啦'
                titledone=True#若有打卡成功的则锁定标题
        else:
            if titledone==False:
                pushdata['title']='['+str(len(main.memberlist)-errorcount)+'/'+str(len(main.memberlist))+']'+'积分任务执行完毕'
else:
    pushdata['title']='任务执行失败'
    pushdata['content']='所有mid或X-Litemall-Token皆打卡失败'

#向pushplus发出推送请求
try:
    if config['push']['push']=='yes':
        pushdata['token']=token
        push=json.loads(requests.post('http://www.pushplus.plus/send/',data=pushdata).text)
        if push['code'] == 200:
            print('推送成功')
        else:
            exit('推送失败：'+push['msg'])
except:
    pass

#Actions Summary
print('正在生成运行结果')
summary='## 执行结果\n#### PS：由于安全性问题，详细结果请使用推送功能\n'+Finishpage+'\n|序号|青年大学习打卡状态|\n|-|-|'
count=0
for i in origin:
    count+=1
    summary+='\n|'+str(count)+'|'
    if i['status'] != 'error':
        summary+='✅|'
    else:
        summary+='❌|'
with open(os.environ['GITHUB_STEP_SUMMARY'],'w+',encoding='utf8') as finaloutput:
    finaloutput.write(summary)