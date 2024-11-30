## ruikang.tech 聊天机器人
#### 初始设置
Create venv
```
python3 -m venv myenv
```
Activate venv
```
source myenv/bin/activate
```
#### 部署到阿里云函数计算FC
1. Install packages ```pip install -r requirements.txt --target ./my-layer-code/python```
2. Zip the python folder under my-layer-code: ```zip -r my-layer-code.zip ./python```
3. Create layer using this zip file on Aliyun
4. Zip .py files and create a FC function on Aliyun