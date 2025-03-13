# -*- coding: utf-8 -*-
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS  # 导入 CORS
import time

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# 模拟 SSE 数据流
@app.route('/stream')
def stream():
    def generate():
        # 模拟一段长的回复内容
        long_message = (
            "这是一个较长的回复内容，将逐字显示。\n"
            "这是第二行内容，继续逐字显示。\n"
            "这是最后一行内容，打字机效果结束。"
        )
        for char in long_message:  # 逐字推送
            time.sleep(0.1)  # 控制打字速度
            yield "data: {}\n\n".format(char)  # 使用 str.format()
    return Response(stream_with_context(generate()), content_type='text/event-stream')

# 新的输入接口
@app.route('/send', methods=['POST'])
def send_message():
    user_input = request.json.get('message')  # 获取用户输入
    if user_input:
        print("收到用户输入: {}".format(user_input))  # 使用 str.format()
        # 这里可以触发新的 SSE 数据流或其他逻辑
        return {"status": "success", "message": "输入已接收"}
    else:
        return {"status": "error", "message": "输入不能为空"}, 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True)