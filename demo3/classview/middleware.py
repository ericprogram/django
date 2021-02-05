
# 中间件
def my_middeware(get_response):
    print("init 被调用")


    def middleware(request):
        print("request 被调用")
        response = get_response(request)
        print("after response 被调用")
        return response
    return middleware


def my_middeware2(get_response):
    print("init2 被调用")


    def middleware2(request):
        print("request2 被调用")
        response = get_response(request)
        print("after response2 被调用")
        return response
    return middleware2