from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

# ====================================
# FastMCP 是官方提供的一个高层（High-level）封装框架
# 能够快速的创建MCP Server，他是利用问的字符串和类型提示自动生成配置
# ====================================
# 1. 初始化
mcp = FastMCP("fast-health-calculator")


# 2. 定义工具
# 注意：FastMCP 会自动读取函数参数类型 (a: float, b: float) 生成 Schema
# 也会自动读取文档字符串 ("计算两个数字的和") 作为工具描述

@mcp.tool()
def add(a: float, b: float) -> float:
    """计算两个数字的和"""
    return a + b


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """
    计算 BMI 指数并返回健康建议。
    Args:
        weight_kg: 体重 (公斤)
        height_m: 身高 (米)
    """
    if height_m <= 0:
        return "错误：身高必须大于 0"

    bmi = weight_kg / (height_m ** 2)
    result = f"BMI 指数: {bmi:.2f}"

    if bmi < 18.5:
        return f"{result} (偏瘦)"
    elif bmi < 24.9:
        return f"{result} (正常)"
    else:
        return f"{result} (偏胖)"


# 模拟一份静态数据
HEALTH_GUIDELINES = """
1. 每天保持 8 小时睡眠。
2. 多吃蔬菜水果，少吃糖。
3. 每周至少运动 150 分钟。
"""


# 定义资源：使用自定义的 URI 协议头 (health://)
@mcp.resource("health://guidelines", mime_type="text/plain")
def get_health_guidelines() -> str:
    """获取通用的健康生活指南"""
    return HEALTH_GUIDELINES


# 定义提示词模板
@mcp.prompt()
def analyze_my_health(
        name: Annotated[str, Field(description="用户的姓名或昵称")],
        weight: Annotated[float, Field(description="体重，单位：公斤 (kg)")],
        height: Annotated[float, Field(description="身高，单位：米 (m)")]
) -> str:
    """创建一个让 AI 分析个人健康状况的提示词"""
    return f"""
    请扮演一位专业的健康顾问。
    用户 {name} 的体重是 {weight}kg，身高是 {height}m。

    请执行以下步骤：
    1. 使用 'calculate_bmi' 工具计算他的 BMI。
    2. 读取 'health://guidelines' 资源，结合指南给出建议。
    """


# 3. 运行
if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8060, path="/mcp/http")
