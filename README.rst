####
后台
####

代码风格
#########

使用 flak8 作为lint工具检测, 开发人员配置 pre-commit 钩子在每次提交前进行检测

1. 安装:  `pip install pre-commit`
2. 激活: `pre-commit install`
3. 试运行:  `pre-commit run`


配置
####

程序通过以下顺序读取配置信息，后加载的配置会覆盖当前配置. 
此处代码位于 `server/settings.py:CONFIG`


1. 从配置文件中加载配置到环境变量，默认配置文件位置为 `server/.env`


接口文档
########

接口文档以 openapi 格式生成, 存放位置在 `docs/api.yaml`

* 生成接口文档

  .. code:: shell
  
     $ cd src/
     $ python manage.py generate_swagger -o -f yaml ../docs/api.yaml

* 预览接口文档(`/` 在 `swagge-ui` 中预览接口文档, `/editor` 在 `swagger-editor` 中预览接口文档)

  .. code:: shell

    $ cd src/
    $ DEBUG=True python manage.py preview_api_doc 


数据库初始化
####

```bash
$ python manage.py migrate
```
