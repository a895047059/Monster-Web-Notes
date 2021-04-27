[toc]
## 大数据量的去重
###说明
> 需求是对一亿以上的数据量进行重复判断，而且要满足时间需求  
> 算了下， 32位的hash， 存在redis里面的话至少需要 `32*100000000/1024/1024=3052M` 
> 至少需要3G的内存才能存的下  
> 在查询了许多资料以后，决定用 `布隆过滤器` ，具体关于布隆过滤器
> 的解释网上可以搜到，已经实现python库 `pybloom` , 但是不满足持久化的需求  
> 后来看到大神大神崔庆才针对scrapy写的 `Scrapy-Redis-BloomFilter` 以后，
> 本着拿来主义的原则，小改了一下集成到了代码里，好用！  
> 代码在这里[代码](./utils/bloomfilter.py)

### 使用方式
```text
import redis
from bloomfilter import BloomFilter

conn = redis.StrictRedis(host=redis_conf['host'], port=redis_conf['port'], db=redis_conf['db'])
f = BloomFilter(server=conn, key='bloomfilter', bit=32, hash_number=6)

```
然后调用f.exists()和f.insert()即可

