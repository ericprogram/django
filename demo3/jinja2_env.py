from jinja2 import Environment


# def environment(**options):
#     env = Environment(**options)
#     # 将自定义的过滤添加到环境中
#     env.filters["do_listreverse"] = do_listreverse
#     return env

def environment(**options):
    env = Environment(**options)
    env.filters['listreverse'] = listreverse

    return env


# 自定义过滤器
def listreverse(lst):
    # list.reverse()
    if lst == "B":
        return "哈哈"