web article parser service
=========
Based on https://github.com/buriy/python-readability
##### Install
pip install readability-lxml
##### Run
python main.py
##### Use
####### Get article parsed json result 
```GET /parse?url=http://example.com/```

***or***

```POST {"url": "http://example.com/"} /parse?url=http://example.com/```
####### Get article parsed html content 
```GET /parse/?url=http://example.com/```

***or***

```POST {"url": "http://example.com/"} /parse/?url=http://example.com/```