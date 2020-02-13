
# weibo_api 使用flask框架

## 安装依赖

``` bash
pip install -r requirements.txt
```

## API List

### `/weibo/topdata`

1. 变量含义
    - `by`：查询方法
      - `1`：按时间区间查询
        - 仅有`from`参数，为查询在`from`之后的数据
        - 仅有`to`参数，为查询在`to`之前的数据
        - `from`和`to`参数都有，为查询区间内的数据
        - `from`和`to`参数都没有，为查询最新的50条数据
      - `2`：按热搜位置区间查询
        - 仅有`from`参数或仅有`to`参数，为查询热搜位置是`from`或`to`的数据
        - `from`和`to`参数都有，为查询区间内的数据
      - `3`：按热搜名字查询
      - `4`：按热搜热度区间查询
        - 仅有`from`参数，为查询热度大于`from`的数据
        - 仅有`to`参数，为查询热度小于`to`的数据
        - `from`和`to`参数都有，为查询热度在区间内的数据
    - `from`：区间起始值
      - `by=1` 时为精确到秒的Unix时间戳
      - `by=2` 时取值为1-50
      - `by=3` 时无效
      - `by=4` 时为热搜热度值（整数）
    - `to`：区间结束值
      - 同 `from`
    - `name`：热搜名字
      - 仅 `by=3` 时有效

2. 示例
    - 按时间查询
      - 最新50条数据

        `/weibo/topdata?by=1`

      - 1581051600（2020年2月7日13时）之前的数据

        `/weibo/topdata?by=1&to=1581051600`

    - 按位置查询
      - 热搜第1的所有数据

        `/weibo/topdata?by=2&from=1` 或 `/weibo/topdata?by=2&to=1`

    - 按名字查询

      `/weibo/topdata?by=3&name=口罩猫`

    - 按热度值查询
      - 大于4000000热度的热搜

        `/weibo/topdata?by=4&from=4000000`

3. 返回数据
    - `code`：返回数据状态代码
      - `0`：成功返回
      - `1`：未知错误
      - `2`：数据库错误
      - `3`：查询结果为空
      - `4`：请求参数错误
    - `data`：数据列表
      - `id`：序号，无实际意义
      - `time`：时间，精确到秒的Unix时间戳
      - `pos`：热搜榜位置，范围1~50
      - `desc`：热搜的名字
      - `desc_extr`：热搜的热度
    - `msg`：状态描述
      - `ok`
      - `unkonwn error`
      - `the database is wrong`
      - `the result of your query is null`
      - `your params are error`
    - 示例

      ```json
      {
        "code": 0,
        "data": [
          {
            "desc": "\u4e0d\u5f97\u5f3a\u884c\u8981\u6c42\u5b66\u751f\u6bcf\u5929\u4e0a\u7f51\u6253\u5361",
            "desc_extr": 3756142,
            "id": 51,
            "pos": 1,
            "time": "2020-02-11 23:58:02"
          },
          {
            "desc": "\u5f3a\u884c\u8981\u6c42\u6240\u6709\u6559\u5e08\u5f55\u64ad\u8bfe\u7a0b\u5fc5\u987b\u5236\u6b62",
            "desc_extr": 2984199,
            "id": 51,
            "pos": 2,
            "time": "2020-02-11 23:58:02"
          },
        ],
        "msg": "ok"
      }
      ```
