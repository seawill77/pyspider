
# coding: utf-8

# In[1]:


#Spider Project Test   Panda TV    top youtuber rank list


# In[36]:


import re

from urllib import request

class Spider():
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<i class="ricon ricon-eye"></i>([\s\S]*?)</span>'
    #find name and number location
    
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        #bytes
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

        
    def __analysis(self, htmls):
        #find name and number
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            anchors.append(anchor)
        #print(anchors)
        return anchors
    
    def __refine(self, anchors):
        #refine  remove useless itmes  like ''*~=+>+?>>&%''
        l = lambda anchor: {
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l, anchors)
    
    def __sort(self, anchors):
        #filter sort name in numebr order
        anchors = sorted(anchors, key = self.__sort_seed, reverse = True )
        return anchors
    
    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number
    
    def __show(self, anchors):
        for anchor in anchors:
            print(anchor['name'] + '------' + anchor['number'])
    
    def go(self):
        #go
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        anchors = self.__show(anchors)
        
spider = Spider()
spider.go()

