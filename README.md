# AwsS3WindowsUploader
> aws s3 uploader for windows.  
> aws windows GUI界面文件上传小工具

![通过测试](https://img.shields.io/badge/build-passing-green.svg)
![python3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![windows10](https://img.shields.io/badge/supportos-windows10-blue.svg)
# GUI
<img src="gui.png"/>

# config.ini
| ArgClass | Args | Detail | e.g |
| ---- | ---- | ---- | ---- |
| aws_account | aws_kid | aws IAM access key ID | A**** |
| aws_account | aws_sak | aws IAM secret access key | o**** |
| bucket_info | region_name | aws s3 region name 区域 | us-west-1 |
| bucket_info | bucket | your bucket name<br>你的桶名称 | mybucket |
| bucket_info | key | filename prefix<br>文件前缀 | myfolder |
