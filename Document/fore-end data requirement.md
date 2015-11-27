# 前台数据文档

> 说明：前台应用模板继承，和引用。被继承和引用的页面不会直接render。需要渲染的模板已写明，在这些模板中也要给出其继承和引用的模板的变量。 另：调试过程中前台使用了一些占位符等占据了变量的位置，传入数据之后可能不能看到效果。

- gallery 继承[] 引用[]

``` js 

{
    "SlideShow":
    [
        {
            "id":"", //跳转
            "src":"",
            "location":"",
            "description":""
        },
        ...
    ]
    
}

```

- sideBar 继承[] 引用[gallery]

``` js
{
    "runTime":{
        "ViewName":""   // View类名，用于判断显示状态
    }
}
```

- navBar 继承[] 引用[]

``` js
{
    "user":{
        "name":"",
        "head_picture":"url.."
        
    }
}
```

- base 继承[] 引用[sideBar,navBar]

``` js 
{
    "CONFIG":{          // 从配置文件统一配置
        "SITE":{
            "TITLE":""  // 网站名称
        },
    },
    "photo_number_this_month": 本月提交数
    
    "photo_number":共有照片
    "photo_number_uncomment":还未评价
}

```

- home(需展示) 继承[base] 引用[]

``` js 
{
    "photo_list":[
        时间倒序的photo对象
    ]
    
}

```

- html 继承[] 引用[]

``` js 
{
    "CONFIG":{          // 从配置文件统一配置
        "SITE":{
            "TITLE":""  // 网站名称
        },
        
    }
    
}

```

- login,signup 继承[html]


- timeline 继承[base] 引用[]
``` js 
{
    "timeLine":
    [
    {
       时间倒序的photo对象
    }
    ]
}

```

- map (需展示) 继承[base] 引用[]

```

```