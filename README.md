## pdf-toc-creator
为PDF文档创建目录


## 用法
### 参数说明
- offset, 实际pdf文件中的页码应该比toc文件中指定的页码偏移多少，正整数表示pdf文件中页码更大
- toc, 指定PDF标签的文件

### toc文件格式说明：
- 一行产生一个目录标签，以左边tab缩进表示目录层级(必须是tab)
- 页码在每行最后，用半角分号分隔

## 用例
```
python pdf-toc-creator.py -f InfoQ-2020中国技术发展白皮书.pdf -o 3 -t toc-infoq.txt
```
