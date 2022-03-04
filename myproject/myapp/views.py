from django.http import JsonResponse


"""
普通搜索方法，url 会传过来输入框内的一个值query
"""
def normal_paper_search(request):
    if request.method == 'GET':
        # request.GET.get里面的值最好不要改,是前端url的参数名

        # query参数，就是input框内的输入,应该可以转换成String类型
        print(request.GET.get('query'))


    #返回的响应reponse，返回文章title，作者，abstract等可以继续添加
    response = {}
    papers = []
    try:
        for i in range(0,50):
            paper = {'title': 'Image Super-Resolution Using Deep Convolutional Networks',
                     'authors': 'Chao Dong, Chen Change Loy, Kaiming He, Xiaoou Tang',
                     'abstract': 'We propose a deep learning method for single image super-resolution (SR). Our method ' \
                                 'directly learns an end-to-end mapping between the low/high-resolution images. The ' \
                                 'mapping is represented as a deep convolutional neural network (CNN) that takes the ' \
                                 'low-resolution image as the input and outputs the high-resolution one. We further ' \
                                 'show that traditional sparse-coding-based SR methods can also be viewed as a deep ' \
                                 'convolutional network. But unlike traditional methods that handle each component ' \
                                 'separately, our method jointly optimizes all layers. Our deep CNN has a lightweight ' \
                                 'structure, yet demonstrates state-of-the-art restoration quality, and achieves fast ' \
                                 'speed for practical on-line usage. We explore different network structures and ' \
                                 'parameter settings to achieve trade-offs between performance and speed. Moreover, ' \
                                 'we extend our network to cope with three color channels simultaneously, ' \
                                 'and show better overall reconstruction quality. ',
                     'Year': i}
            # ..可以继续添加返回值
            papers.append(paper)
        response['papers'] = papers

    except Exception as e:
        # 出错情况的返回，
        response['msg'] = str(e)
        response['error_num'] = 1

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

    # 返回的响应reponse，返回文章title，作者，abstract等可以继续添加
    response = {}
    try:
        response['Title'] = ''
        response['Author'] = ''
        response['abstract'] = ''
        # ..可以继续添加返回值
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    # 最好是JsonResponse的返回
    return JsonResponse(response)
