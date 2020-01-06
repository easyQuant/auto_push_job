import requests
import time

headers = {
	'Accept':'*/*',
	'Origin':'https://www.zhipin.com',
	'Referer':'https://www.zhipin.com/web/geek/recommend',
	'Sec-Fetch-Mode':'cors',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:71.0) Gecko/20100101 Firefox/71.0'
}

# 获取个人信息
# https://www.zhipin.com/wapi/zpuser/wap/getUserInfo.json
user_info = 'https://www.zhipin.com/wapi/zpuser/wap/getUserInfo.json'

# 最新筛选列表
job_list = 'https://www.zhipin.com/wapi/zpgeek/recommend/job/list.json?expectId=2524633&sortType=2&salary=406&degree=&experience=106&stage=&scale=302&districtCode=&businessCode=&page={}'

# 职位详情
job_info = 'https://www.zhipin.com/job_detail/{}.html?ka=new_list_job_0'

# 开始沟通
job_send = 'https://www.zhipin.com/wapi/zpgeek/friend/add.json?jobId={}'

# 每天投递数量
COUNT = 30

# 默认投递页数 
PAGE_COUNT = 4

# 过滤字段
FILTER_STAGE_LIST = ['已上市', 'C轮', 'D轮', '未融资']

FILTER_SCALE_LIST = ['500-999人', '100-499人', '1000-9999人']

# 开始投递 每日09:55定时执行
def init():

    # 格式化cookie
    cookies = _parse('__c=1578291478; __g=-; _bl_uid=aykXC51L20X1v5z47wte5mF6s6Um; lastCity=101010100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1578288018; __l=r=https%3A%2F%2Flogin.zhipin.com%2F%3Fka%3Dheader-login&l=%2Fuser%2Flogin.html%22&friend_source=0&friend_source=0; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1578293032; t=KhzvIi7AkhVu2n9s; wt=KhzvIi7AkhVu2n9s; __zp_stoken__=e768eumgz23yqC1Dk%2BJRyC1XbLTHINQ0coweJhxEu6ivatqyJIlY1Qluya%2BpAzEycINclR%2Fe2aXv1%2FRr%2B07rA8PWDciHBtKxJcn2PtgByng%2FOvz8iNrAyyrc%2F1TiKYKVq%2F0L; __a=48816663.1578291477.1578291477.1578291478.16.2.15.16')

    # 保存职位id列表
    ids = []

    # 通过筛选的投递数量
    success_count = 0

    # 排除的投递数量
    fail_count = 0

    result = requests.get(user_info, cookies = cookies, headers = headers).json()
    check_login_status = result['message']
    print('登录状态 {}'.format(check_login_status))
    
    # 如果登录状态ok
    # 开始遍历列表
    if check_login_status == 'Success':

        # 遍历页数
        for page_count in range(1, PAGE_COUNT + 1):
            
            result = requests.get(job_list.format(page_count), cookies = cookies, headers = headers).json()
            page_count = page_count + 1
            print('公司列表请求状态 {}'.format(result['message']))

            if result['message'] == 'Success':
                _list = result['zpData']['jobList']

                for item in _list:

                    if len(ids) >= COUNT:
                        print('### 今日投递数量满足每日投递上限 {} 停止投递 ###'.format(COUNT))
                        break

                    # 不是c轮以上 同时人数小100则投递
                    # 大公司没发展空间
                    if item['brandStageName'] not in FILTER_STAGE_LIST and item['brandScaleName'] not in FILTER_SCALE_LIST:
                        print('公司名称 {}'.format(item['brandName']))
                        # print('当日投递数量 {}'.format(len(ids)))

                        # 获得符合条件的职位id并添加
                        ids.append(item['encryptJobId'])
                        success_count = success_count + 1
                    else:
                        fail_count = fail_count + 1

            time.sleep(30)
    else:
        print('### 请重新登录 状态已失效 ###')

    print('### 准备开始批量沟通 ###')

    for _id in ids:
        time.sleep(10)
        print('_id {}'.format(_id))
        result = requests.get(job_send.format(_id), cookies = cookies, headers = headers).json()
        print('### 沟通状态 {}'.format(result['message']))

    print('### 今日投递完成 准备等待hr姐姐们的回复 ###')
    print('### 通过条件筛选的公司数量 {} ###'.format(success_count))
    print('### 未通过条件筛选的公司数量 {} ###'.format(fail_count))

def _parse(cookie):
    return dict([l.split("=", 1) for l in cookie.split("; ")])

init()

