import asyncio
from fastmcp.client import SSETransport
from fastmcp import Client

# ==========================================
# 配置部分
# ==========================================
# 这里指定服务端的 URL，而不是脚本路径
SERVER_URL = "http://localhost:8000/sse"


async def main():
    print(f"🔌 正在连接到服务器: {SERVER_URL} ...")

    # ==========================================
    # 关键变化点
    # ==========================================
    # 旧代码: async with stdio_client(server_params) as (read, write):
    # 新代码: 直接传入 URL
    transport = SSETransport(url=SERVER_URL)
    client = Client(transport)
    async with  client:
        await client.ping()
        print(await client.list_tools())
        # 3. 初始化会话 (Session)

        # ==========================================
        # 场景 A: 使用工具 (Tools)
        # ==========================================
        print("--- 测试工具调用 (Tools) ---")

        # A1. 列出可用工具
        tools = await client.list_tools()
        print(f"发现 {len(tools)} 个工具: {[t.name for t in tools]}")

        # A2. 调用 add 工具
        print("\n>> 调用 add(a=10, b=5.5)...")
        result_add = await client.call_tool("add", arguments={"a": 10, "b": 5.5})
        print(f"计算结果: {result_add.content[0].text}")

        # A3. 调用 calculate_bmi 工具
        print("\n>> 调用 calculate_bmi(weight=70, height=1.75)...")
        result_bmi = await client.call_tool("calculate_bmi", arguments={"weight_kg": 70, "height_m": 1.75})
        print(f"BMI 结果: {result_bmi.content[0].text}")

        # ==========================================
        # 场景 B: 读取资源 (Resources)
        # ==========================================
        print("\n--- 测试资源读取 (Resources) ---")

        # B1. 列出可用资源
        resources = await client.list_resources()
        print(f"发现资源: {[r.uri for r in resources]}")

        # B2. 读取具体资源内容
        target_uri = "resource://health-guidelines"
        print(f"\n>> 读取资源内容: {target_uri}")
        try:
            res_content = await client.read_resource(target_uri)
            text = res_content[0].text
            print(f"资源内容预览:\n{text.strip()}")
        except Exception as e:
            print(f"读取失败: {e}")

        # ==========================================
        # 场景 C: 获取提示词 (Prompts)
        # ==========================================
        print("\n--- 测试提示词模板 (Prompts) ---")

        # C1. 列出可用提示词
        prompts = await client.list_prompts()
        print(f"发现提示词: {[p.name for p in prompts]}")

        # C2. 获取填充后的提示词
        prompt_name = "analyze_my_health"
        print(f"\n>> 获取提示词: {prompt_name} (参数: Alice, 60kg, 1.65m)")

        # 注意：FastAPI/FastMCP 可能会对参数类型校验更严格，确保传入的是字符串
        prompt_result = await client.get_prompt(
            prompt_name,
            arguments={"name": "Alice", "weight": "60", "height": "1.65"}
        )

        message = prompt_result.messages[0]
        print(f"生成的 Prompt 角色: {message.role}")
        print(f"生成的 Prompt 内容:\n{message.content.text}")

        print("\n所有测试完成，断开连接。")


if __name__ == "__main__":
    # 确保先运行了服务端 (python server.py)
    try:
        asyncio.run(main())
    except ConnectionRefusedError:
        print("\n连接失败！请检查服务端是否已启动 (http://localhost:8000/sse)")
    except Exception as e:
        print(f"\n发生错误: {e}")
