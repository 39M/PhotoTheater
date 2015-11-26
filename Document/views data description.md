# 后台数据说明
  
> 说明：所有date字段均为日期时间，创建和更新时间自动生成；通过image.url属性访问图片，image.name获取文件名
  
- Home
  
```
{
    'album_list': [
        {
            'name': 名称,
            'create_date': 创建日期时间,
            'update_date': 最后更新日期时间,
        },
        ......
    ]
}
```
  
- TimeLine, Map
  
```
{
    'photo_list': [
        {
            'name': 名称,
            'shot_date': 拍摄日期时间（可以为空）,
            'upload_date': 上传日期时间,
            'update_date': 更新日期时间,
            'latitude': 经纬度（可以为空）,
            'longitude': 经纬度（可以为空）,
            'location_text': 文本位置信息（默认为空字符串）,
            'emotion': 心情（默认为空字符串）,
            'source': 最新图片文件，使用url属性访问,
            'origin_source': 原始图片文件,
            'thumb': 缩略图,
        },
        ......
    ]
}
```

- Comment
  
```
    'comment_list': [
        {
            'content': 内容,
            'date': 发布日期时间,
            'update_date': 上传日期时间,
        }
    ]
```
