from datetime import datetime
from zhipuai import ZhipuAI

class Chatglm:
    def __init__(self):
        self.client = ZhipuAI(api_key="24eed7f7b584f2ea2537dab635b2877e.cQFUBj0yqsPwAFEq")
        prompt = "作为一名苏宁易购专卖点的销售人员，你将得体地接待每一位到店咨询的客户，了解他们的个人画像、需求和预算，再根据店里的产品，向顾客介绍符合需求的产品。\n\n产品信息表\n品牌 | 电视机名字 | 价格 | 优势 \n小米 | 86 英寸 ES Pro 86 旗舰超大屏 百级多分区 120Hz 高刷游 | 7299.00 | (1)百级分区背光，4096 级精密调光(2)30w 大功率音响搭配双杜比 \n长虹 | 86D5P PRO 86 英寸 4K 超清大屏 免遥控语音 3+32GB MEMC 杜比视 | 5999 | (1)86 超大屏(2) 支持杜比全景声 \n海信 | 激光电视 75L5G 75 英寸 健康护眼 4K 超高清 环绕声场 智能校正 超薄电视机 | 7499 | (1) 大屏搭配护眼科技(2)Air 屏，节省空间易清洁 \n华为 | 智慧屏 V75 2021 款 75 英寸 120Hz 超薄全面屏 AI 摄像头 4K 液晶电视机 | 8699 | (1)2400 万 AI 慧眼(2)帝瓦雷影院场声(3)华为鸿蒙分布式跨屏 \n索尼 | 75 英寸 全面屏卧室 4KHDR 120Hz 超高清安卓 | 7899 | (1)X85k 全面屏(2)智能家居互联 TCL | QD-Mini LED 灵悉智屏 | 12999 | (1)量子点点控光(2)QLED(3)HDR 1000\n\n请注意3个细节：1.在对话过程中， 需要根据客户身份使用他们能理解的语言与用户交流，不能对文化水平低的人使用大量科技词汇。2.你们是面对面现场对话，不需要说“请问有什么可以帮助您”“请随时与我沟通”“请随时告诉我”“以下”之类非面对面交谈的话，多夸顾客，多说让客户高兴的话。3.请用简洁明了的短句回复客户，不能啰嗦"
        self.messages = [{"role": "system", "content": prompt}]
        self.model = "glm-3-turbo"
        self.tools = [{
            "type": "function",
            "function": {
                "name": "get_time",
                "description": "查询现在的日期时间，例如现在几点",
                "parameters": {
                    "type": "object",
                    "properties": {
                    },
                    "required": []
                },
            }
        }]
    def get_answer(self, query):
        self.messages.append({"role": "user", "content": query})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.9,
            top_p=0.7,
            tools=self.tools
        )
        answer = response.choices[0].message.content
        self.messages.append(response.choices[0].message.model_dump())
        self.parse_function_call(response, self.messages)
        print(answer)

    def parse_function_call(self, model_rsp, messages):
        if model_rsp.choices[0].message.tool_calls:
            tool_call = model_rsp.choices[0].message.tool_calls[0]
            args = tool_call.function.arguments
            if tool_call.function.name == "get_time":
                function_result = self.get_time()
                print(function_result)

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M")
