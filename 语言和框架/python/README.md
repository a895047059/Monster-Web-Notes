<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 大数据量的去重
### 说明
> 需求是对一亿以上的数据量进行重复判断，而且要满足时间需求  
> 算了下， 32位的hash， 存在redis里面的话至少需要 `32*100000000/1024/1024=3052M` 
> 至少需要3G的内存才能存的下  
> 在查询了许多资料以后，决定用 `布隆过滤器` ，具体关于布隆过滤器
> 的解释网上可以搜到，已经实现python库 `pybloom` , 但是不满足持久化的需求  
> 后来看到大神大神崔庆才针对scrapy写的 `Scrapy-Redis-BloomFilter` 以后，
> 本着拿来主义的原则，小改了一下集成到了项目里，好用！  
> 代码在这里[代码](./utils/bloomfilter.py)

### 使用方式
```text
import redis
from bloomfilter import BloomFilter

conn = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])
f = BloomFilter(server=conn, key='bloomfilter', bit=32, hash_number=6)

```
然后调用f.exists()和f.insert()即可

# python中的单例  

- #### 使用模块  
>  Python 的模块就是天然的单例模式  
```
class Singleton(object):
    pass


singleton = Singleton()
```
其他模块引入下面的
```shell script
from a import singleton
```
- #### 使用装饰器
```shell script
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
```
装饰器调用即可
```shell script
@Singleton
def demo():
    pass
```

- #### 使用类
```shell script
import threading

class Singleton(object):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with Singleton._instance_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance
```
通过如下方式调用
```shell script
obj = Singleton.instance()
```

- #### 以上方法升级， 基于__new__
```shell script
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass


    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instance
```
采用`obj = Singleton()`调用即可
