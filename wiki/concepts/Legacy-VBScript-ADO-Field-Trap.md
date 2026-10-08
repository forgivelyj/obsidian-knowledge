# Legacy VBScript ADO Field Object Reference Trap

## 概述
在传统 Classic ASP 与 VBScript 环境中，通过 ADODB Recordset 提取数据库数据并存入 Scripting.Dictionary 或其他对象容器时，容易踩中对象引用陷阱导致游标移动后数据失效并抛出 `(null): 严重错误 (0x8000FFFF)`。

## 根因剖析 (Root Cause)
在 VBScript 中，语法 `rs("FieldName")` 实际返回的是 `ADODB.Field` COM 对象实例，而非字段的底层标量值。
当执行：
```vbscript
dict.Add "myField", rs("FieldName")
```
VBScript 存入的是当前活跃游标对应的 Field COM 对象引用。
一旦后续调用 `rs.MoveNext`，游标向前移动，原有的 Field COM 对象内部指针随之变化或失效。当后续在另一个循环中读取 `dict("myField")` 时，会试图重新解析已移动游标的字段，导致数据错乱，或者当 Recordset 遍历完毕 (EOF) 后直接触发 COM 运行时严重异常：
`(null): 严重错误 (0x8000FFFF)`

## 规范修复方案 (Validated Solution)
在向容器添加、赋值或拼接前，必须通过显式类型转换强制脱钩 COM 引用，将其转化为 VBScript 标量基本类型（Primitive Value）：
1. **数值类型**：`CLng(rs("ID"))`, `CDbl(rs("Amount"))`
2. **字符串类型 / Null 安全拼接**：`rs("Name") & ""` 或 `CStr(rs("Code") & "")`
3. **JSON 序列化安全封装**：通过 `EscapeJson` 转义双引号与控制字符。

## 反模式与负面证据 (Negative Anti-Patterns)
- **直接添加字段对象**：`objDict.Add "Score", rs("Score")`（❌ 游标前进后失效）
- **未处理 Null 值的类型转换**：`CLng(rs("NullableField"))`（❌ 当字段为 NULL 时抛出 Type Mismatch 错误）
