from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    # 将自定义的过滤添加到环境中
    env.filters["do_listreverse"] = do_listreverse
    return env


# 自定义过滤器
def do_listreverse(lst):
    if lst == "B":
        return "哈哈"
    else:
        return "不成立"