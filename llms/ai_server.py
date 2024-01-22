from llms import *

if __name__ == '__main__':
    llm = Chatglm()
    while True:
        query = input("请输入：")
        llm.get_answer(query)
