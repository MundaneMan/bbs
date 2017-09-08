cms管理系统

本系统在windows环境中，使用pycharm进行开发，服务器采用ubuntu-server 16.04

服务器配置
1.环境搭建
  未安装pip的首先安装pip,sudo apt-get install pyothon-pip
  sudo pip install -r requirements.txt

2.安装nginx,mongodb
  sudo apt-get isntall nginx
  sudo apt-get isntall mongodb

3.配置本地访问域名

  windows hosts 配置 192.168.195.139(服务器地址)       www-local.instructions.com
  ubuntu hosts  配置  127.0.0.1    mongodb

4.nginx配置
   拷贝 工程目录config 下的 vhost_instructions.conf 到 /etc/nginx/sites-enabled/下
   重启nginx   sudo service nginx restart



