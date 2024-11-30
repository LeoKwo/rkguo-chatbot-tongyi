from langchain_community.chat_models.tongyi import ChatTongyi
import os
from dotenv import load_dotenv
from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from resumeTool import resumeTool
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

load_dotenv()

tools = [resumeTool]

tool_node = ToolNode(tools)

model = ChatTongyi(
      model='qwen-turbo',
      api_key=os.getenv('DASHSCOPE_API_KEY'),
)

# Initialize memory to persist state between graph runs
memory = MemorySaver()

system_message = """
    你是由郭睿康（Leo Guo）创造的 GuoGenius。
    你是郭睿康的数字化人格，负责回答关于郭睿康的专业经验、教育背景以及其他与职业相关的话题的问题。
    你可以查询郭睿康知识库以获取信息，但除此之外对郭睿康一无所知。
    在回答问题时，你应该始终首先查询知识库中与问题概念相关的信息。

    例如，给定以下输入问题：
    —–示例输入问题开始—–
    郭睿康在 Day & Nite 的现任工作中表现如何？
    —–示例输入问题结束—–
    你的研究流程应为：
        1.	查询你的知识库工具（resumeTool），获取关于“工作”的相关上下文信息。
        2.	根据你收集的上下文回答问题。
    如果找不到答案，绝不要编造答案。直接说明你不知道即可。
    
    尽可能完整地回答以下问题：
"""

agent_executor = create_react_agent(
    model=model, tools=tools, state_modifier=system_message, checkpointer=memory
)

# # TESTER
# print(agent_executor.invoke({
#         "messages": [
#             ("user", "ruikang guo的职业信息")
#         ]
#     },
#     {"configurable": {"thread_id": "test"}},
# )["messages"][-1].content)

# Define a wrapper function
def bot(msg: str, thread_id: int):
    return agent_executor.invoke({
            "messages": [
                ("user", msg)
            ]
        },
        {"configurable": {"thread_id": thread_id}}
    )["messages"][-1].content

def lambda_handler(event, context):
    # Extract 'msg' and 'thread_id' from the event
    msg = event.get("msg", "")
    thread_id = event.get("thread_id", 0)
    
    # Call the bot function
    try:
        response = bot(msg, thread_id)
        return {
            "statusCode": 200,
            "body": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }