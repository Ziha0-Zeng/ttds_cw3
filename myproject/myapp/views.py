import time

from django.http import JsonResponse

from myapp.preprocess.tfidf_generator import InvertIndexGenerator

"""
普通搜索方法，url 会传过来输入框内的一个值query
"""
def normal_paper_search(request):
    if request.method == 'GET':
        # request.GET.get里面的值最好不要改,是前端url的参数名

        # query参数，就是input框内的输入,应该可以转换成String类型
        print(request.GET.get('query'))

    cur_page = 1
    page_size = 10

    start = time.time()
    generator = InvertIndexGenerator()
    # read data from json
    generator.readDocs('localhost', port=27017)
    # calculate inverted index and calculate tfidf values and write into mongodb
    # generator.tfidf_lib()
    query = request.GET.get('query')
    print(request.GET.get('query'))
    # sorted_docs = generator.tfidf_query(query)
    # generator.tfidf_lib()
    sorted_docs = generator.tfidf_query_full(query)
    if len(sorted_docs) == 0:
        papers = []
    else:
        papers = generator.id2dict_search(sorted_docs, cur_page, page_size=100)
    print("sorted_docs", len(sorted_docs))
    
    print("papers", len(papers))
    end = time.time()
    print("time", end - start)


    #返回的响应reponse，返回文章title，作者，abstract等可以继续添加
    response = {}
    # papers = []
    # try:
    #     for i in range(0,50):
    #         paper = {'title': 'Image Super-Resolution Using Deep Convolutional Networks',
    #                  'authors': 'Chao Dong, Chen Change Loy, Kaiming He, Xiaoou Tang',
    #                  'abstract': 'We propose a deep learning method for single image super-resolution (SR). Our method ' \
    #                              'directly learns an end-to-end mapping between the low/high-resolution images. The ' \
    #                              'mapping is represented as a deep convolutional neural network (CNN) that takes the ' \
    #                              'low-resolution image as the input and outputs the high-resolution one. We further ' \
    #                              'show that traditional sparse-coding-based SR methods can also be viewed as a deep ' \
    #                              'convolutional network. But unlike traditional methods that handle each component ' \
    #                              'separately, our method jointly optimizes all layers. Our deep CNN has a lightweight ' \
    #                              'structure, yet demonstrates state-of-the-art restoration quality, and achieves fast ' \
    #                              'speed for practical on-line usage. We explore different network structures and ' \
    #                              'parameter settings to achieve trade-offs between performance and speed. Moreover, ' \
    #                              'we extend our network to cope with three color channels simultaneously, ' \
    #                              'and show better overall reconstruction quality. ',
    #                  'Year': i}
    #         # ..可以继续添加返回值
    #         papers.append(paper)
    response['papers'] = papers

    # except Exception as e:
    #     # 出错情况的返回，
    #     response['msg'] = str(e)
    #     response['error_num'] = 1

    # 最好是JsonResponse的返回
    return JsonResponse(response)

"""
高级搜索方法，url 会传过来四个参数，keywords，authors，开始日期，截止日期
"""
def advanced_paper_search(request):
    if request.method == 'GET':
        print("I have get the request")

        # keyword参数，就是搜索关键字,应该可以转换成String类型
        print(request.GET.get('keyword'))
        # authors参数，作者框内的输入
        print(request.GET.get('authors'))
        # startDate 开始日期
        print(request.GET.get('startDate'))
        # endDate 结束日期
        print(request.GET.get('endDate'))


    query = request.GET.get('keyword')
    # authors参数，作者框内的输入
    author = request.GET.get('authors')
    # startDate 开始日期
    startDate = request.GET.get('startDate')
    # endDate 结束日期
    endDate = request.GET.get('endDate')

    cur_page = 1
    page_size = 10

    start = time.time()
    generator = InvertIndexGenerator()
    # read data from json
    generator.readDocs('localhost', port=27017)
    # calculate inverted index and calculate tfidf values and write into mongodb
    # generator.tfidf_lib()
    query = request.GET.get('keyword')
    # sorted_docs = generator.tfidf_query(query)
    # generator.tfidf_lib()
    sorted_docs = generator.tfidf_query_full(query, startDate, endDate, author, 0)
    print("sorted_docs", len(sorted_docs))
    if len(sorted_docs) == 0:
        papers = []
    else:
        papers = generator.id2dict_search(sorted_docs, cur_page, page_size=100)
    print("papers", len(papers))
    end = time.time()
    print("time", end - start)


    #返回的响应reponse，返回文章title，作者，abstract等可以继续添加
    response = {}
    response['papers'] = papers
    

    # # 返回的响应reponse，返回文章title，作者，abstract等可以继续添加
    # response = {}
    # try:
    #     response['Title'] = ''
    #     response['Author'] = ''
    #     response['abstract'] = ''
    #     # ..可以继续添加返回值
    # except Exception as e:
    #     response['msg'] = str(e)
    #     response['error_num'] = 1

    # # 最好是JsonResponse的返回
    return JsonResponse(response)


def feedback(request):
    if request.method == 'GET':
        print("I have get the request")
        print(request.GET.get('badFeedback'))
        print(request.GET.get('goodFeedback'))
    return JsonResponse({})