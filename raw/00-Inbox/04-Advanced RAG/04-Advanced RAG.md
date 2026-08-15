# 04\-Advanced RAG

## Advanced RAG

**学习目标:**

1. 熟悉 Advanced RAG的基本作用

1. 熟悉 前索引优化方式

1. 熟悉 查询优化方式

1. 熟悉 后索引优化方式

### 一\. Advanced RAG概述

Advanced RAG重点聚焦在检索增强，即优化Retrieval阶段。增加了Pre\-Retrieval预检索和Post\-Retrieval后检索阶段。

![d58be599\-b885\-4467\-bf60\-f1099b39e2dd\.png](图片和附件/d58be599-b885-4467-bf60-f1099b39e2dd.png)

基于朴素RAG，高级RAG主要通过预检索策略和后检索策略来提升检索质量。

**预检索过程**

高级RAG着重优化了索引结构和查询的方式。优化索引旨在提高被索引内容的质量，包括增强数据颗粒度、优化索引结构、添加元数据、对齐优化和混合检索等策略。查询优化的目标则是明确用户的原始问题，使其更适合检索任务，使用了**查询重写、查询转换、查询扩展**等技术。

**后检索过程**

对于由问题检索得到的一系列上下文，后检索策略关注如何优化它们与查询问题的集成。这一过程主要包括**重新排序和压缩上下文**。重新排列检索到的信息，将最相关的内容予以定位标记，这种策略已经在LlamaIndex2、LangChain等框架中得以实施。直接将所有相关文档输入到大型语言模型（LLMs）可能导致信息过载，为了缓解这一点，后检索工作集中选择必要的信息，强调关键部分，并限制了了相应的上下文长度。

### 二\. 摄取管道

**IngestionPipeline** 是 LlamaIndex 中用于**文档摄取（Ingestion）的核心组件，它把从“原始数据”到“可检索索引”的整个过程流程化、模块化、可复用**。

简单来说：**它是一条自动化的数据加工生产线**，专门负责把原始文档一步步转变成高质量的 Node（节点），并可选地直接插入向量数据库。

**1\. 主要作用:**

- **统一管理摄取流程**：把加载、解析、分块、元数据提取、嵌入生成、索引存储等步骤串成一条可配置的管道。

- **提升生产效率**：支持**缓存（Cache）**，相同文档\+相同转换只需处理一次，后续运行极快。

- **支持复杂高级 RAG**：轻松实现语义分块、元数据增强、Embedding 优化、自动提取标题/摘要等高级操作。

- **异步与并行处理**：支持 arun\(\) 异步执行，适合大规模文档摄取。

- **可重复性与版本控制**：管道配置固定后，摄取结果可高度复现。

文档地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/ingestion/?h=ingestionpipeline\#llama\_index\.core\.ingestion\.pipeline\.IngestionPipeline

**整体架构:**

```Plaintext
Reader
    ↓
 Document
    ↓
 IngestionPipeline
    ├── NodeParser
    ├── Extractors
    ├── Metadata
    ├── Embedding
    └── Transformations
    ↓
 Node
    ↓
 VectorStore
 读取成Document之后,就直接用管道,不需要再重复写逻辑
```

#### 1\.基础使用

```Plaintext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.extractors import (
    TitleExtractor,
)

from base_llm import embed_model, llm

# 定义数据连接器去读取数据
documents = SimpleDirectoryReader(input_files=["../data_file/小说.txt"]).load_data()
# 定义文本分割器
text_splitter = SentenceSplitter(chunk_size=256, chunk_overlap=30)

# 提取器
title_extractor = TitleExtractor(nodes=5, node_template="请为以下文档生成一个简洁的标题: {context_str}", num_workers=5, llm=llm)

# 创建数据摄入管道
pipeline = IngestionPipeline(
    transformations=[text_splitter, embed_model, title_extractor]
)

# 执行管道
nodes = pipeline.run(documents=documents)

# 打印处理后的节点
for node in nodes:
    print(repr(node))
    print("-------")


index = VectorStoreIndex(nodes, embed_model=embed_model)
print(index.as_retriever().retrieve('萧炎父亲是谁'))
```

#### 2\. 元数据提取

在 LlamaIndex 中，**Metadata Extractor**（元数据提取器）是一类特殊的 **Transformation** 组件，它的作用是：

> **使用 LLM（大模型）自动为每个 Node（文本块）生成额外的元数据信息**，从而丰富 Node 的 metadata，帮助后续检索和生成阶段更加精准。

**为什么需要元数据提取器？**

单纯把文档切块后，每个小块（Node）往往**缺少上下文**。 通过元数据提取器，可以让每个小块“带上”标题、摘要、关键词、能回答的问题等信息，提升：

- 检索精度（结合 Metadata Filtering）

- 生成质量（LLM 能看到更多结构化信息）

- 可解释性和可过滤性

文档地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/extractors/

##### 1\. 常用元数据提取器

|提取器|作用|常用参数|成本|
|---|---|---|---|
|**TitleExtractor**|为每个 Node 生成一个简洁标题|nodes=5（前N个）|中|
|**SummaryExtractor**|生成当前块的摘要（可包含前后块摘要）|summaries=\["self", "prev", "next"\]|中高|
|**QuestionsAnsweredExtractor**|生成这个 Node 能回答的几个问题|questions=3|中|
|**KeywordExtractor**|提取关键词|keywords=10|低|

- 使用方式

```Plaintext
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline

from llama_index.core.extractors import (
    TitleExtractor,
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    KeywordExtractor,
)

from base_llm import llm, embed_model


# 读取文档
documents = SimpleDirectoryReader(input_files=["../data_file/小说.txt"]).load_data()
# 为每一个节点生成问题-默认的提示词是英文，手动添加提示词
question_prompt_template = """
以下是参考内容：
{context_str}

请根据上述上下文信息，生成 {num_questions} 个该内容能够具体回答的问题，这些问题的答案最好是该内容独有的，不容易在其他地方找到。

你也可以参考上下文中可能提供的更高层次的总结信息，结合这些总结，尽可能生成更优质、更具有针对性的问题。请用中文输出！
"""


# 构建数据处理流水线
pipeline = IngestionPipeline(
    transformations=[
        # 文本切分
        SentenceSplitter(
            chunk_size=300,
            chunk_overlap=50
        ),

        # 提取标题利用前几个chunk
        # 通过LLM推断文档主题
        # 再把标题注入所有chunk metadata
        # 超长文档不适用效果下降
        TitleExtractor(
            llm=llm,
            nodes=5
        ),

        # 提取摘要  summaries对那些节点进行摘要
        SummaryExtractor(
            llm=llm,
            summaries=["prev", "self",  "next"]
        ),

        # 提取当前chunk可回答的问题  默认生成是英文  需要自定义提示词
        QuestionsAnsweredExtractor(
            llm=llm,
            questions=3,
            prompt_template=question_prompt_template
        ),

        # 提取关键词
        KeywordExtractor(
            llm=llm,
            keywords=5
        ),
    ]
)


# 执行pipeline
nodes = pipeline.run(
    documents=documents
)


# 查看metadata
for node in nodes:
    print(repr(node))
    print()


# 构建向量索引
index = VectorStoreIndex(
    nodes=nodes, embed_model=embed_model
)

# 查询测试
query_engine = index.as_query_engine(llm=llm)

response = query_engine.query(
    "萧炎斗气多少?"
)

print("\n最终回答:")
print(response)
```

#### 3\. 缓存

在 LlamaIndex 的 IngestionPipeline 中，缓存（Cache） 是非常重要的生产级特性，主要用于避免重复计算，极大提升文档摄取效率，尤其适合增量更新场景。

**缓存到底是什么？**

IngestionCache 的作用是：

- 对 每个文档（Document） \+ 每个 Transformation（转换步骤） 的结果进行哈希缓存。

- 当你再次运行相同的 Pipeline 时，系统会检查缓存：

    - 如果内容和转换逻辑都没变 → 直接从缓存中读取结果，跳过该步骤。

    - 如果内容发生了变化 → 重新执行对应 Transformation。 这可以节省大量时间和费用（尤其是 Embedding 和 LLM 提取元数据这类耗时操作）。

**缓存主要缓存哪些内容?**

- 分块后的 Node（TextNode）

- Embedding 向量

- 元数据提取结果（Title、Summary、Keyword 等）

- 自定义 Transformation 的输出

**常见缓存容器:**

|缓存容器|类型|核心功能|优点|缺点|最常见场景|
|---|---|---|---|---|---|
|`SimpleKVStore`|内存缓存|运行时临时缓存|极快、零配置|进程结束即丢失|Notebook、测试|
|`RedisKVStore`|Redis分布式缓存|分布式共享缓存|高性能、支持多Worker|需要部署Redis|企业级RAG|
|`MongoDBKVStore`|Mongo缓存|存复杂Node结构|文档结构灵活|查询性能一般|复杂metadata|
|`Embedding Cache`|向量缓存|缓存Embedding结果|节省Embedding成本|需要版本管理|高频Embedding|

![056\.png](图片和附件/056.png)

##### 1\. 本地缓存

- 实现代码

```Plaintext
from llama_index.core import SimpleDirectoryReader
from llama_index.core.extractors import TitleExtractor
from llama_index.core.node_parser import SentenceSplitter

from llama_index.core.ingestion import (
    IngestionPipeline,
    IngestionCache
)

from llama_index.core.storage.kvstore import SimpleKVStore

from day05.base_llm import llm



# 创建KVStore
# kvstore = SimpleKVStore()
#
#
# # 创建Cache
# cache = IngestionCache(
#     cache=kvstore
# )
#
#
# # 创建Pipeline
# pipeline = IngestionPipeline(
#     transformations=[
#         SentenceSplitter(
#             chunk_size=300,
#             chunk_overlap=50
#         ),
#
#         TitleExtractor(
#             llm=llm,
#             nodes=5
#         ),
#     ],
#
#     cache=cache
# )
#
# # 读取文档
# documents = SimpleDirectoryReader(
#     input_files=["../data_file/小说.txt"]
# ).load_data()
#
#
# # 第一次运行
# nodes = pipeline.run(
#     documents=documents
# )
#
# print("第一次运行完成")
#
#
# # 保存缓存
# kvstore.persist(
#     "./cache/cache.json"
# )
#
# print("缓存已保存")



# 加载本地缓存
kvstore = SimpleKVStore.from_persist_path(
    "./cache/cache.json"
)

cache = IngestionCache(
    cache=kvstore
)


# 创建Pipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(
            chunk_size=300,
            chunk_overlap=50
        ),

        TitleExtractor(
            llm=llm,
            nodes=5
        ),
    ],

    cache=cache
)
documents = SimpleDirectoryReader(
    input_files=["../data_file/小说.txt"]
).load_data()
nodes = pipeline.run(
    documents=documents
)

print("第二次运行完成")
```

- 源码实现步骤

```Plaintext
pipeline.run()
│
├── 1. 检查输入
│
├── 2. documents 转 nodes
│       │
│       └── SentenceSplitter 之前
│           先包装成 DocumentNode
│
├── 3. 遍历 transformations
│       │
│       ├── SentenceSplitter
│       │       │
│       │       ├── 计算 cache key
│       │       ├── 查询缓存
│       │       ├── 命中 → 返回缓存
│       │       └── 未命中 → 真正执行
│       │
│       ├── TitleExtractor
│       │       │
│       │       ├── 查询缓存
│       │       ├── 命中 → 返回
│       │       └── 调用LLM
│       │
│       └── 其他 Transformation
│
└── 4. 返回最终 nodes
```

##### 2\. redis缓存

- 实现代码

```Plaintext
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.storage.kvstore.redis import RedisKVStore
from base_llm import llm, embed_model



# # 创建 Redis KVStore
# kvstore = RedisKVStore.from_host_and_port(
#     host="localhost",
#     port=6379
# )
#
# # 创建 IngestionCache
# cache = IngestionCache(
#     cache=kvstore
# )
#
#
# # 创建 Pipeline
# pipeline = IngestionPipeline(
#     transformations=[
#         # 文本切分
#         SentenceSplitter(
#             chunk_size=300,
#             chunk_overlap=50
#         ),
#         # 摘要提取
#         SummaryExtractor(
#             llm=llm,
#             summaries=["self"]
#         )
#     ],
#
#     cache=cache
# )
#
# # 读取文档
# documents = SimpleDirectoryReader(
#     input_files=["../data_file/小说.txt"]
# ).load_data()
#
#
# # 第一次运行
# print("===== 第一次运行 =====")
#
# nodes = pipeline.run(
#     documents=documents
# )
#
# print(f"节点数量: {len(nodes)}")
#
#
# # 查看metadata
# for node in nodes[:2]:
#     print(repr(node))
#     print()
#
#
# # 第二次运行
# print("\n===== 第二次运行（命中缓存） =====")
#
# nodes = pipeline.run(
#     documents=documents
# )
#
# print(f"节点数量: {len(nodes)}")



print("----------------------直接查询 Redis 数据库----------------------")
import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, charset="utf-8")

# 查看所有 keys
all_keys = redis_client.keys("llama_cache")
print(f"Redis 中的所有相关 keys: {len(all_keys)} 个")

# 查看前几个 key 的内容
for key in all_keys[:3]:
    value = redis_client.hgetall(key)
    print(f"Key: {key}")
    for k, v in value.items():
        # 将存储的内容进行转义
        print(f"Value: {v.encode('utf-8').decode('unicode_escape')}")
    print("-" * 30)
```

### 三\. 查询优化

查询重写是指在检索之前，使用 LLM（大语言模型）对用户原始查询进行改写、扩展或优化，生成一个或多个更好的查询版本，再去进行向量检索或混合检索。

**为什么要使用查询重写？**

1. 用户查询通常质量较差

1. 用户输入的查询往往**简短、模糊、口语化**，缺少关键信息或上下文，导致检索效果很差。

2. 显著提升召回率（Recall）

2. 重写后的查询更清晰、语义更丰富、更接近文档中的表达方式，能检索到更多相关文档。

3. 解决语义不匹配问题

    - 处理同义词、不同表述方式（如“怎么做” vs “最佳实践”）

    - 补充隐含信息

    - 把模糊问题变成具体问题

#### 1\. 实现逻辑

```Plaintext
from llama_index.core import PromptTemplate
from base_llm import llm

class QueryOptimizer:

    def __init__(self):
        # 初始化 LLM
        self.llm = llm

        # 1. Query Rewrite Prompt
        self.rewrite_prompt = PromptTemplate(
            """
            你是一个专业的查询优化助手。
            
            请优化用户问题。
            
            要求：
            1. 保持原始语义
            2. 增强技术关键词
            3. 更适合向量检索
            4. 不要回答问题
            5. 只输出优化后的问题
            
            用户问题：
            {query}
            
            优化后的问题：
            """
        )


        # 3. Multi Query Prompt
        self.multi_query_prompt = PromptTemplate(
            """
            你是一个查询增强助手。
            
            请基于用户问题：
            
            生成5个不同表达方式的问题。
            
            要求：
            1. 保持语义一致
            2. 使用不同关键词
            3. 更适合搜索和向量检索
            4. 每行一个问题
            5. 不要解释
            
            用户问题：
            {query}
            
            生成的问题：
            """
        )


    # Query Rewrite
    def rewrite(self, query: str):
        result = self.llm.predict(
            self.rewrite_prompt,
            query=query
        )

        return result.strip()


    # Multi Query
    def multi_query(self, query: str):
        result = self.llm.predict(
            self.multi_query_prompt,
            query=query
        )

        queries = [
            line.strip("1234567890.- ").strip()
            for line in result.split("\n")
            if line.strip()
        ]

        return queries

    # Full Optimization Pipeline
    def optimize(self, query: str):

        print("=" * 60)
        print("原始问题:")
        print(query)

        # 1. Rewrite
        rewritten_query = self.rewrite(query)

        print("\n" + "=" * 60)
        print("Rewrite 后:")
        print(rewritten_query)

        # 3. Multi Query
        multi_queries = self.multi_query(rewritten_query)

        print("\n" + "=" * 60)
        print("Multi Query 结果:")

        for idx, q in enumerate(multi_queries, 1):
            print(f"{idx}. {q}")

        print("\n" + "=" * 60)

        return {
            "original_query": query,
            "rewritten_query": rewritten_query,
            "multi_queries": multi_queries,
        }


if __name__ == "__main__":
    optimizer = QueryOptimizer()

    query = "llamaindex 查询优化怎么做"

    result = optimizer.optimize(query)

    print("\n最终结果:")
    print(result)
```

### 三\. 预检索\-优化索引

索引优化是高级 RAG（Advanced RAG）中最重要的一环。它指的是在数据摄取（Ingestion）阶段和索引构建阶段，通过各种技术手段提升索引数据的质量、结构和检索效率，从而让最终检索结果更准确、更相关。

**核心目标:**

- 提高检索的**精度（Precision）** 和 **召回率（Recall）**

- 减少无关噪声，降低 LLM 幻觉

- 更好地处理长文档、复杂结构文档

- 支持更精细的过滤和控制

- 提升整体 RAG 系统性能和用户体验

文档地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/indices/

#### 1\. 父子索引

**父子索引** 是 LlamaIndex 中一种**层级化（Hierarchical）的索引策略，主要用来解决大文档检索时上下文丢失**的问题。

其核心思想是：

- **子节点（Child）**：小块文本（通常 256\~512 tokens），用于**精确检索**（embedding 相似度高）

- **父节点（Parent）**：更大的文本块（通常 1024\~2048 tokens 或整个文档），用于**提供完整上下文**

当检索时，先找到最相关的**子节点**，然后自动返回其对应的**父节点**，从而实现“**小块检索 \+ 大块返回**”的效果。

##### 1\. 实现代码

```Plaintext
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,StorageContext,load_index_from_storage
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import HierarchicalNodeParser,get_leaf_nodes
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import os

from base_llm import embed_model, llm

# 1. Chroma 向量数据库
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)
chroma_collection = chroma_client.get_or_create_collection(
    "parent_child_demo"
)

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)

# 2. 判断索引是否存在
if os.path.exists("./storage"):

    print("开始加载索引...")

    # 注意：
    # 不要自己重新 new docstore
    # 要从 persist_dir 自动恢复
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage",
        vector_store=vector_store,
    )
    # 加载索引
    index = load_index_from_storage(
        storage_context=storage_context,
        embed_model=embed_model,
    )
    print("索引加载成功")
else:
    print("开始构建索引...")
    # 3. 加载文档
    documents = SimpleDirectoryReader(
        input_files=["../data_file/小说.txt"]
    ).load_data()
    # 4. 层级切分
    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 512, 128]
    )
    # 5. Ingestion Pipeline
    # 这里只做切分
    # 不提前做 embedding
    pipeline = IngestionPipeline(
        transformations=[
            node_parser,
        ]
    )

    # 6. 生成所有 nodes
    nodes = pipeline.run(
        documents=documents
    )

    # 7. 获取叶子节点
    # 只有 leaf nodes 参与向量化
    leaf_nodes = get_leaf_nodes(nodes)
    # 8. 创建 docstore
    # 保存所有层级节点
    docstore = SimpleDocumentStore()

    docstore.add_documents(nodes)

    # 9. StorageContext
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        docstore=docstore,
    )

    # 10. 创建索引
    # 这里只会给 leaf_nodes 生成 embedding
    index = VectorStoreIndex(
        leaf_nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    # 11. 持久化
    # 会保存：
    # - docstore
    # - index_store
    # - vector_store
    index.storage_context.persist(
        persist_dir="./storage"
    )

    print("索引构建完成")

# 12. 基础 Retriever
# 先召回 leaf nodes
base_retriever = index.as_retriever(
    similarity_top_k=5
)

# 13. AutoMergingRetriever
# 自动向上合并 parent nodes
retriever = AutoMergingRetriever(
    vector_retriever=base_retriever,
    storage_context=index.storage_context,
    verbose=True,
    simple_ratio_thresh=0.5
)

# 14. QueryEngine
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=llm,
)

# 15. 查询
query = "萧炎父亲是谁"

response = query_engine.query(query)

print("\n================== 回答 ==================\n")
print(response)

# 16. 查看检索结果
nodes = retriever.retrieve(query)

print("\n================== 检索结果 ==================\n")
for node in nodes:
    print(repr(node))
    print()
```

- 功能图

![058\.png](图片和附件/058.png)

#### 2\. 元数据索引

LlamaIndex 的元数据索引优化是指在构建索引时为每个文本节点（Node）附加丰富的元数据（metadata），然后在检索阶段通过 MetadataFilters 对向量搜索结果进行精确过滤，从而实现结构化条件筛选（如按文件名、日期、类别、章节等），大幅提升检索精准度。

##### 1\. 实现代码

```Plaintext
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterCondition
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    KeywordExtractor,
)

import chromadb
import os

from base_llm import embed_model, llm

# ====================== Chroma 配置 ======================
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("parent_child_demo")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# ====================== 索引加载或构建 ======================
if os.path.exists("./storage"):
    print("开始加载索引...")
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage",
        vector_store=vector_store,
    )
    index = load_index_from_storage(
        storage_context=storage_context,
        embed_model=embed_model,
    )
    print("索引加载成功")
else:
    print("开始构建索引...")

    # 加载文档
    documents = SimpleDirectoryReader(
        input_files=["../data_file/小说.txt"]
    ).load_data()

    # 为文档添加基础元数据
    for doc in documents:
        doc.metadata.update({
            "file_name": "斗破苍穹",
            "doc_type": "novel",
            "language": "zh",
            "category": "玄幻"  # 可根据实际情况修改
        })

    # 层级节点解析器
    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 512, 128]
    )
    question_prompt_template = """
    以下是参考内容：
    {context_str}

    请根据上述上下文信息，生成 {num_questions} 个该内容能够具体回答的问题，这些问题的答案最好是该内容独有的，不容易在其他地方找到。

    你也可以参考上下文中可能提供的更高层次的总结信息，结合这些总结，尽可能生成更优质、更具有针对性的问题。请用中文输出！
    """
    # 元数据提取器
    extractors = [
        TitleExtractor(nodes=5, llm=llm),  # 提取标题
        QuestionsAnsweredExtractor(questions=3, prompt_template=question_prompt_template, llm=llm),  # 提取可回答的问题
        KeywordExtractor(keywords=10, llm=llm),  # 提取关键词
    ]

    # Ingestion Pipeline
    pipeline = IngestionPipeline(
        transformations=[
            node_parser,
            *extractors,  # 自动添加 metadata
        ]
    )

    nodes = pipeline.run(documents=documents)

    # 获取叶子节点（用于向量索引）
    leaf_nodes = get_leaf_nodes(nodes)

    # Docstore 保存所有层级节点（含 metadata）
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)

    # StorageContext
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        docstore=docstore,
    )

    # 创建索引（仅叶子节点向量化）
    index = VectorStoreIndex(
        leaf_nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    # 持久化
    index.storage_context.persist(persist_dir="./storage")
    print("索引构建完成")





# ====================== 支持元数据过滤的 QueryEngine ======================
def create_query_engine(book_name):
    # 加上元数据过滤
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="file_name", value=book_name),
            MetadataFilter(key="doc_type", value="novel"),
        ],
        # 过滤条件  与或非
        condition=FilterCondition.AND
    )
    # ====================== 创建 Retriever ======================
    base_retriever = index.as_retriever(
        similarity_top_k=8,
        filters=filters  # 支持传入 metadata filters
    )

    retriever = AutoMergingRetriever(
        vector_retriever=base_retriever,
        storage_context=index.storage_context,
        verbose=True,
        simple_ratio_thresh=0.5
    )
    return RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
    )


query = "萧炎父亲是谁"
if "萧炎" in query:
    book_name = "斗破苍穹"



response_filtered = create_query_engine(book_name).query(query)
print("\n=== 带元数据过滤的回答 ===")
print(response_filtered)

print("\n=== 检索数据 ===")
ret_nodes = create_query_engine(book_name).retrieve("萧炎父亲是谁")
for no in ret_nodes:
    print(repr(no))
    print()
```

### 四\. 检索器

在 RAG 中，它负责先从知识库、向量库数据源中召回相关文本，再交给 LLM 生成答案。

- 接口地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/retrievers/

**常见检索器:**

|检索器|核心作用|适合场景|核心特点|
|---|---|---|---|
|`VectorIndexRetriever`|向量相似度检索|通用 RAG|语义检索能力强|
|`BM25Retriever`|关键词检索|专业术语、代码、API|精确匹配强|
|`QueryFusionRetriever`|多检索器融合|企业级 Hybrid RAG|Dense \+ BM25 融合|
|`AutoMergingRetriever`|层级检索|长文档、PDF|小块检索，大块返回|
|`RouterRetriever`|智能路由检索|多数据源系统|自动选择 Retriever|
|`SQLRetriever`|SQL 数据检索|结构化数据|面向数据库|
|`SummaryRetriever`|摘要级检索|超长文档|先摘要再检索|
|`KeywordTableRetriever`|关键词表检索|传统搜索|类似倒排索引|
|`SimpleFusionRetriever`|简单融合检索|多路召回|多 Retriever 合并|

#### 1\. 混合检索

混合检索 = **向量检索 \+ 关键词检索** 的结合。

- **向量检索**：使用 Embedding 模型（如 text\-embedding\-ada\-002、bge、voyage 等），基于**语义相似度**检索，能理解同义词、上下文。

- **关键词检索**：使用 BM25、TF\-IDF 等传统算法，基于**精确词频匹配**，对专有名词、缩写、数字、产品型号等非常敏感。

混合检索会把两种结果**融合**（Fusion）后返回 Top K 文档。

```Plaintext
pip install llama-index-retrievers-bm25
```

##### 1\. BM25

**BM25**（Best Matching 25）是一种经典的**关键词检索算法**（也称为 Sparse Retrieval 稀疏检索），是现代搜索引擎（如 Elasticsearch）中广泛使用的概率排名模型。

它是 TF\-IDF（词频\-逆文档频）算法的改进版本，在信息检索领域被公认为**传统关键词检索的最强算法之一**。

##### 2\. 实现代码

```Plaintext
import os

import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.vector_stores.chroma import ChromaVectorStore

from base_llm import embed_model, llm

# 索引和 DocStore 的持久化路径
PERSIST_DIR = "./storage"
DOCSTORE_PATH = "./storage/docstore.json"

# 使用本地 Chroma 作为向量库
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("hybrid_demo")
vector_store = ChromaVectorStore(chroma_collection=collection)

# 本地没有索引时，读取文档并重新构建索引
if not os.path.exists(PERSIST_DIR):
    print("首次构建索引...")

    documents = SimpleDirectoryReader(
        input_files=["../data_file/deepseek介绍.txt"]
    ).load_data()

    # 将文档切分成节点，方便向量检索和关键词检索使用
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    nodes = splitter.get_nodes_from_documents(documents)

    # DocStore 保存节点原文，BM25 检索依赖这里的数据
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)
    docstore.persist(persist_path=DOCSTORE_PATH)

    # StorageContext 统一管理向量库和文档存储
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store,
        docstore=docstore,
    )

    # 构建向量索引并写入本地存储
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("索引构建完成")
else:
    # 本地已有索引时，直接加载持久化数据
    print("检测到本地索引，直接加载...")

    docstore = SimpleDocumentStore.from_persist_path(DOCSTORE_PATH)
    storage_context = StorageContext.from_defaults(
        persist_dir=PERSIST_DIR,
        vector_store=vector_store,
        docstore=docstore,
    )

    index = load_index_from_storage(
        storage_context=storage_context,
        embed_model=embed_model,
    )

# 向量检索负责语义相似度召回
vector_retriever = index.as_retriever(similarity_top_k=7)

# BM25 检索负责关键词匹配召回
bm25_retriever = BM25Retriever.from_defaults(
    docstore=docstore,
    similarity_top_k=7,
)

# 融合检索会合并向量检索和 BM25 检索结果，并重新排序
retriever = QueryFusionRetriever(
    retrievers=[
        vector_retriever,
        bm25_retriever,
    ],
    llm=llm,
    similarity_top_k=5,
    mode="reciprocal_rerank",
    use_async=True,
    # 生成问题
    num_queries=1,
    retriever_weights=[0.4, 0.6]
)

# 测试查询文本
query = "Alexander Wang 对deepseek的评价"

print("\nbm25检索" + "=" * 50)
vector_res = bm25_retriever.retrieve(query)
for vector_node in vector_res:
    print(f"score: {vector_node.score}")
    print(vector_node.text[:500])

print("\n向量检索" + "=" * 50)
vector_res = vector_retriever.retrieve(query)
for vector_node in vector_res:
    print(f"score: {vector_node.score}")
    print(vector_node.text[:500])

print("\n混合检索" + "=" * 50)
fusion_results = retriever.retrieve(query)
for node in fusion_results:
    print(f"score: {node.score}")
    print(node.text[:500])

# 使用融合检索结果作为上下文，让大模型生成最终回答
print("\n模型回复" + "=" * 50)
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=llm,
)

res = query_engine.query(query)
print(res)
```

##### 3\. QueryFusionRetriever

QueryFusionRetriever 是 LlamaIndex 中一个专门用于混合检索（Hybrid Retrieval） 的高级检索器（Retriever）。

![060\.png](图片和附件/060.png)

##### 4\. 融合排序

|模式|全称 / 说明|特点|推荐场景|
|---|---|---|---|
|**reciprocal\_rerank** \(默认推荐\)|**Reciprocal Rank Fusion \(RRF\)**|根据**排名位置**（而非原始分数）进行融合。出现越靠前的结果权重越高。|**最常用**，效果稳定，适合 Vector \+ BM25 混合检索|
|**simple**|Simple Fusion|简单合并所有结果，去重后按原始分数排序|快速测试、结果不多时使用|
|**relative\_score**|Relative Score Fusion|基于相对分数进行归一化融合（Weaviate 提出）|分数分布差异较大的检索器|
|**dist\_based\_score**|Distribution\-Based Score Fusion|基于分数分布进行融合，试图改进 RRF|实验性，追求更精细融合时使用|

###### 1\. reciprocal\_rerank

- 把我们检索到的内容进行融合和排序

- 多个查询可能检索到不同的相关文档，有的排名高，有的排名低。`RRF` 通过公式 `1 / (rank + k)` 对所有查询结果重新评分，保证更全面的相关性。

- 假设还是 Vector \+ BM25 两个检索器，权重设置为 0\.4, 0\.6 结果如下：

|文档|Vector 排名|BM25 排名|Vector 贡献 \(w=0\.4\)|BM25 贡献 \(w=0\.6\)|**加权 RRF 总分**|
|---|---|---|---|---|---|
|Doc A|1|3|0\.4 × 1/ \(1\+60\) ≈ 0\.00656|0\.6 × 1/ \(3\+60\) ≈ 0\.00952|**0\.01608**|
|Doc B|2|1|0\.4 × 1/ \(2\+60\) ≈ 0\.00645|0\.6 × 1/\( 1\+60\) ≈ 0\.00984|**0\.01629**|
|Doc C|3|5|0\.4 × 1/ \(3\+60\) ≈ 0\.00635|0\.6 × 1/ \(5\+60\) ≈ 0\.00923|**0\.01558**|
|Doc D|\-|2|0|0\.6 × 1/ \(2\+60\) ≈ 0\.00968|**0\.00968**|
|Doc E|4|\-|0\.4 × 1/ \(4\+60\) ≈ 0\.00625|0|**0\.00625**|

###### 2\.relative\_score

- relative\_score 是 QueryFusionRetriever 中的一种融合模式，由 Weaviate 提出，主要用于不同检索器分数尺度差异很大的情况（比如向量检索分数通常在 0\~1 之间，而 BM25 分数可能是 0\~几十）。

- 把每个检索器的原始分数归一化（Min\-Max Scaling）到 \[0, 1\] 区间，再进行加权求和，最后按总分排序。

**归一化公式:**

$\text{normalized_score} = \frac{\text{original_score} - \text{min_score}}{\text{max_score} - \text{min_score}}$

**权重设置**：\[0\.6, 0\.4\]（Vector 权重 0\.6，BM25 权重 0\.4）

|文档|Vector 原始分|Vector 归一化计算过程|Vector 归一化结果|BM25 原始分|BM25 归一化计算过程|BM25 归一化结果|**最终得分计算过程**|**最终得分**|**排序**|
|---|---|---|---|---|---|---|---|---|---|
|Doc A|0\.85|\(0\.85 \- 0\.72\) / \(0\.91 \- 0\.72\)|**0\.684**|12\.5|\(12\.5 \- 5\.0\) / \(18\.0 \- 5\.0\)|**0\.577**|0\.6×0\.684 \+ 0\.4×0\.577|**0\.641**|**1**|
|Doc B|0\.72|\(0\.72 \- 0\.72\) / \(0\.91 \- 0\.72\)|**0\.000**|18\.0|\(18\.0 \- 5\.0\) / \(18\.0 \- 5\.0\)|**1\.000**|0\.6×0\.000 \+ 0\.4×1\.000|**0\.400**|**3**|
|Doc C|0\.91|\(0\.91 \- 0\.72\) / \(0\.91 \- 0\.72\)|**1\.000**|5\.0|\(5\.0 \- 5\.0\) / \(18\.0 \- 5\.0\)|**0\.000**|0\.6×1\.000 \+ 0\.4×0\.000|**0\.600**|**2**|

###### 3\. dist\_based\_score

- dist\_based\_score 是 LlamaIndex QueryFusionRetriever 支持的融合模式之一，全称 Distribution\-Based Score Fusion（基于分布的分数融合），也简称 DBSF。

- 它是 **Relative Score Fusion** 的改进版本，不再简单使用 Min\-Max 归一化，而是**根据每个检索器结果的分数分布**（均值 \+ 标准差）来进行**标准化（Z\-Score 风格）**，然后加权融合。

- 这种方式能更好地处理**分数分布差异大、不均匀**的情况，比单纯的 Min\-Max 更鲁棒。

**核心公式:**

$\text{normalized_score} = \frac{\text{original_score} - \text{mean}}{\text{std}}$

mean：该检索器本次返回的所有结果的分数**均值**

std：该检索器本次返回的所有结果的分数**标准差**

- 计算过程: 权重：\[0\.6, 0\.4\]（Vector 0\.6，BM25 0\.4）

|文档|Vector 原始分|Vector 均值|Vector 标准差|Vector 标准化过程|Vector 标准化结果|BM25 原始分|BM25 均值|BM25 标准差|BM25 标准化过程|BM25 标准化结果|最终得分计算过程|最终得分|排序|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Doc A|0\.85|0\.8267|0\.0807|\(0\.85 \- 0\.8267\) / 0\.0807|\+0\.289|12\.5|11\.8333|5\.333|\(12\.5 \- 11\.8333\) / 5\.333|\+0\.125|0\.6×0\.289 \+ 0\.4×0\.125|0\.223|1|
|Doc B|0\.72|0\.8267|0\.0807|\(0\.72 \- 0\.8267\) / 0\.0807|\-1\.322|18\.0|11\.8333|5\.333|\(18\.0 \- 11\.8333\) / 5\.333|\+1\.156|0\.6×\(\-1\.322\) \+ 0\.4×1\.156|\-0\.331|3|
|Doc C|0\.91|0\.8267|0\.0807|\(0\.91 \- 0\.8267\) / 0\.0807|\+1\.033|5\.0|11\.8333|5\.333|\(5\.0 \- 11\.8333\) / 5\.333|\-1\.281|0\.6×1\.033 \+ 0\.4×\(\-1\.281\)|0\.107|2|

Vector 均值计算：

$\frac{0.85+0.72+0.91}{3}=0.8267$

Vector 标准差计算：

$\sqrt{\frac{(0.85-0.8267)^2+(0.72-0.8267)^2+(0.91-0.8267)^2}{3}}=0.08073$

#### 2\. 路由检索

- **RouterRetriever**（路由检索器）是 LlamaIndex 中一个**智能分发器**，它的核心作用是：**根据用户查询的内容，自动选择最合适的检索器（Retriever）来执行检索**。

- 简单来说，它就像一个“交通警察”，把不同的查询路由到最擅长的检索通道上。

接口地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/retrievers/router/\#llama\_index\.core\.retrievers\.RouterRetriever

##### 1\. 实现代码

```Plaintext
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.core.tools import RetrieverTool
from llama_index.core.retrievers import RouterRetriever

from base_llm import llm, embed_model

# 加载 deepseek 文档
deep_docs = SimpleDirectoryReader(
    input_files=["../data_file/deepseek介绍.txt"]
).load_data()

deep_index = VectorStoreIndex.from_documents(
    deep_docs, embed_model=embed_model
)

# 加载 小说文档
doupo_docs = SimpleDirectoryReader(
    input_files=["../data_file/小说.txt"]
).load_data()

doupo_index = VectorStoreIndex.from_documents(
    doupo_docs, embed_model=embed_model
)

# 创建 Retriever
deep_retriever = deep_index.as_retriever(
    similarity_top_k=3
)

doupo_retriever = doupo_index.as_retriever(
    similarity_top_k=3
)

# 包装成 Tool
deep_tool = RetrieverTool.from_defaults(
    retriever=deep_retriever,
    description="""
    用于检索 DeepSeek 相关介绍资料。
    适合回答 DeepSeek 的背景、模型特点、技术能力、应用场景、人物评价等问题。
    """
)

doupo_tool = RetrieverTool.from_defaults(
    retriever=doupo_retriever,
    description="""
    用于检索小说相关内容。
    适合回答小说人物、剧情发展、章节情节、角色关系、功法设定等问题。
    """
)

# 创建 RouterRetriever
router_retriever = RouterRetriever.from_defaults(
    retriever_tools=[
        deep_tool,
        doupo_tool
    ],
    llm=llm,
    # 能不能一次选择多个 Retriever
    select_multi=False
)

# 开始检索
questions = [
    "DeepSeek 为什么受到关注？",
    "Alexander Wang 对 DeepSeek 的评价是什么？",
    "萧炎和萧薰儿是什么关系？",
]

for query in questions:
    nodes = router_retriever.retrieve(query)

    print(f"\n用户问题: {query}")
    print("=" * 50)

    for node in nodes:
        print(node.text)
        print()
```

- 实现过程

![061\.png](图片和附件/061.png)

#### 3\. sql 检索

- SQL 检索 是 LlamaIndex 提供的结构化数据检索能力，其核心是 Text\-to\-SQL（自然语言转 SQL）技术。

- 它允许用户用自然语言提问，LlamaIndex 自动将问题转换成 SQL 语句，然后在关系型数据库（MySQL、PostgreSQL、SQLite 等）上执行查询，最后返回结果并生成自然语言回答。

- 适用场景:

    - 公司销售报表查询（如“2025年Q1 华东区销售额Top10客户”）

    - 用户订单、库存、财务数据查询

    - CRM、ERP、数据仓库的自然语言查询

##### 1\. 实现代码

```Plaintext
from sqlalchemy import create_engine

from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from base_llm import llm, embed_model


# MySQL
engine = create_engine(
    "mysql+pymysql://root:root@localhost/spiders"
)

sql_database = SQLDatabase(engine)

# Query Engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["ali"],
    llm=llm,
    context_query_kwargs={
            "ali": "存储阿里的公司招聘岗位信息，包括城市、岗位名称、公司等"
        },
    # 当表多了之后, 需要问题匹配表
    embed_model=embed_model
)


question = '西安有那些岗位?'
response = query_engine.query(question)

print("\n回答：")
print(response)

print("\nSQL：")
print(response.metadata)
```

- 功能图

![062\.png](图片和附件/062.png)

### 五\. 后检索\-后处理器

在 LlamaIndex 里，**后处理器的作用就是对检索到的文档或初步结果进行再加工，以生成最终的回答或输出**。可以理解为“检索结果的最后一步加工器”。

**作用概述:**

1. 答案融合（Answer Fusion）

    - 当一个问题匹配到多条文档或数据源时，后处理器会把它们整合成一个自然语言答案。

    - 例如多条向量检索结果，后处理器将相关内容摘要、合并、去重复后返回。

2. 格式化输出（Formatting / Post\-Processing）

    - 对检索结果进行格式化：表格、Markdown、JSON、摘要。

    - 可以统一回答风格或输出结构。

3. 质量优化（Rerank / Filtering / Refinement）

    - 可以对结果排序、过滤噪声，或者使用 LLM 进一步提炼内容。

    - 例如 `QueryFusionRetriever` 结合 LLM 做候选结果融合就是典型的后处理。

4. 上下文补充（Context Enrichment）

    - 根据检索结果补充上下文信息，例如给回答加上出处、引用或相关文档链接。

接口地址:https://developers\.llamaindex\.ai/python/framework\-api\-reference/postprocessor/

**常用后节点:**

|后处理器|类型|作用|实现原理|企业使用率|
|---|---|---|---|---|
|`SimilarityPostprocessor`|过滤|过滤低相关节点|根据 `NodeWithScore.score` 与阈值比较|⭐⭐⭐⭐⭐|
|`PIINodePostprocessor`|过滤|删除敏感信息|正则匹配身份证、手机号、邮箱等|⭐|
|`LLMRerank`|重排序|使用 LLM 对检索结果重新排序|Prompt \+ LLM排序|⭐⭐⭐|
|`RankGPTRerank`|重排序|使用 RankGPT 方法排序|Pairwise Ranking|⭐⭐|
|`CohereRerank`|重排序|调用 Cohere Rerank API|Cross Encoder|⭐⭐⭐⭐|
|`SentenceTransformerRerank`|重排序|使用 CrossEncoder模型排序|Query\+Node相关度计算|⭐⭐⭐⭐|
|`FlagEmbeddingReranker`|重排序|使用 BGE\-Reranker排序|BGE Cross Encoder|⭐⭐⭐⭐⭐|
|`LongContextReorder`|上下文优化|解决 Lost in the Middle|重要节点重新排列到首尾|⭐⭐⭐⭐⭐|
|`SentenceEmbeddingOptimizer`|上下文优化|句子级裁剪|保留最相关句子|⭐⭐⭐⭐|
|`PrevNextNodePostprocessor`|上下文扩展|自动补充前后节点|加载相邻Chunk|⭐⭐⭐⭐|
|`AutoPrevNextNodePostprocessor`|上下文扩展|自动判断是否扩展上下文|LLM决定是否补充前后节点|⭐⭐|
|`FixedRecencyPostprocessor`|时间排序|优先最新文档|根据时间戳排序|⭐|
|`EmbeddingRecencyPostprocessor`|时间排序|时间\+相关度排序|Similarity \+ Recency Score|⭐⭐|
|`TimeWeightedPostprocessor`|时间排序|时间衰减排序|Similarity × TimeDecay|⭐⭐|

#### 1\. 过滤

后节点过滤 是 RAG 流程中检索完成之后（Post\-Retrieval），对初步召回的 Nodes（文档块）进行筛选和过滤的步骤。

**主要作用:**

- 提高回答的**精度**

- 减少无关内容干扰

- 节省 Token 消耗（上下文更干净）

- 降低幻觉概率

##### 1\. 实现代码

```Plaintext
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from base_llm import embed_model, llm


documents = SimpleDirectoryReader(
    input_files=["../data_file/公司规章制度.txt"]
).load_data()

parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

index = VectorStoreIndex(
    parser.get_nodes_from_documents(documents),
    embed_model=embed_model
)

retriever = index.as_retriever(similarity_top_k=15)  # 先多召回15条


similarity_processor = SimilarityPostprocessor(similarity_cutoff=0.7)

query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=llm,
    node_postprocessors=[
        similarity_processor,
    ],
)


query = "公司上下班时间"
response = query_engine.query(query)
print("==== LLM回答 ====")
print(response)



nodes = retriever.retrieve(query)
print("\n==== 检索节点分数 ====")
for node in nodes:
    print(f"Score: {node.score:.3f} | Text: {node.text[:100]}...")


res = similarity_processor.postprocess_nodes(nodes)
print(res)
```

#### 2\. 重排序

- **重排序** 是 RAG 流程中**检索之后**的一个重要步骤：

    - 在向量检索（或混合检索）召回一批候选文档（通常 Top 10\~50）后，使用**更强大的模型**对这些文档重新打分和排序，把最相关的文档排到最前面。

```Plaintext
# 模块下载
pip install llama-index-postprocessor-flag-embedding-reranker 
pip install FlagEmbedding
# 可能transformers 会冲突 降低版本
pip install transformers==4.46.3
```

##### 1\. 实现代码

```Plaintext
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from base_llm import embed_model, llm
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker


documents = SimpleDirectoryReader(
    input_files=["../data_file/公司规章制度.txt"]
).load_data()

parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

index = VectorStoreIndex(
    parser.get_nodes_from_documents(documents),
    embed_model=embed_model
)

retriever = index.as_retriever(similarity_top_k=15)  # 先多召回15条


# 重排序
reranker = FlagEmbeddingReranker(
    # 专门的重排模型
    model=r"D:\LLM\Local_model\BAAI\bge-reranker-large",
    top_n=5
)


query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=llm,
    node_postprocessors=[
        reranker
    ],
)



query = "公司上下班时间"
response = query_engine.query(query)
print("==== LLM回答 ====")
print(response)


nodes = retriever.retrieve(query)
print("\n==== 检索节点分数 ====")
for node in nodes:
    print(f"Score: {node.score:.3f} | Text: {node.text[:100]}...")


print('==== 重排节点 ====')
rerank_nodes = reranker.postprocess_nodes(
    nodes,
    query_str=query
)
for i, node in enumerate(rerank_nodes):
    print(f"{i+1}. score={node.score}")
    print(node.text[:100])
    print()
```

#### 3\. 上下文优化

上下文优化是 LlamaIndex 节点后处理器中的一个分类，定位在**检索完成后、LLM 生成前**这一环节。它的核心任务是对检索到的原始节点进行**顺序调整或内容精简**，使送入 LLM 的上下文更加优质。

##### 1\.实现代码

```Plaintext
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex
)

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.postprocessor import LongContextReorder

from base_llm import embed_model

# 读取文档
documents = SimpleDirectoryReader(
    input_files=["../data_file/公司规章制度.txt"]
).load_data()

# 切分
parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)

# 构建索引
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)

# 检索器
retriever = index.as_retriever(
    similarity_top_k=8
)

query = "公司上下班时间"

# 原始检索结果
retrieved_nodes = retriever.retrieve(query)

print("===== 重排前 =====")

for i, node in enumerate(retrieved_nodes):
    print(f"{i+1}. score={node.score:.4f}")
    print(node.text[:50])
    print()

# LongContextReorder
reorder = LongContextReorder()

reordered_nodes = reorder.postprocess_nodes(
    retrieved_nodes
)

print("===== 重排后 =====")

for i, node in enumerate(reordered_nodes):
    print(f"{i+1}. score={node.score:.4f}")
    print(node.text[:50])
    print()
```

#### 4\. 上下文拓展

**上下文拓展（Context Expansion）**，又叫 **上下文增强**，指的是在给 LLM 提问或生成答案时，不仅使用直接检索到的相关节点（Chunk），还主动扩充额外相关信息，使 LLM 拥有 **更丰富、更完整的背景知识** 来生成回答。

核心目标：减少 LLM **信息不足或断章取义**的风险。

1. **召回更多节点**（Top\-K Retriever \+ 后处理）

2. **增加相关上下文**（Query Expansion / Reranker / Similarity \+ Knowledge Graph）

3. **跨文档上下文融合**（QueryFusionRetriever / Multi\-Index Retrieval）

##### 1\. 实现代码

```Plaintext
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import AutoPrevNextNodePostprocessor
from base_llm import llm, embed_model  

# 读取文档
documents = SimpleDirectoryReader(
    input_files=["../data_file/公司规章制度.txt"]
).load_data()

# 切分文档为节点
parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)

# 构建索引
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)

# 创建检索器
retriever = index.as_retriever(
    similarity_top_k=10   # 先召回10条
)

# 创建 AutoPrevNextNodePostprocessor
auto_prevnext_processor = AutoPrevNextNodePostprocessor(
    # 需要通过docstore 获取前后节点
    docstore=index.docstore,
    llm=llm,
    max_prev_nodes=1,   # 最多取前1个节点
    max_next_nodes=1,   # 最多取后1个节点
    max_tokens=1000      # 扩展上下文的总token限制
)

# 创建 QueryEngine 并加入后处理器
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever,
    llm=llm,
    node_postprocessors=[
        auto_prevnext_processor
    ]
)

# 查询示例
query = "公司上下班时间"

response = query_engine.query(query)

print("===== LLM 回答 =====")
print(response)

# 查看最终被选中的节点
retrieved_nodes = retriever.retrieve(query)
print("===== 拓展前 =====")

for i, node in enumerate(retrieved_nodes):
    print(f"{i+1}. score={node.score:.4f}")
    print(node.text[:50])
    print()

processed_nodes = auto_prevnext_processor.postprocess_nodes(retrieved_nodes, query_str=query)

print("\n===== 扩展后的节点 =====")
for i, node in enumerate(processed_nodes):
    print(node)
```

- 功能图

![063\.png](图片和附件/063.png)

#### 5\. 时间排序

时间排序是 LlamaIndex 节点后处理器中的一个分类，专门用于**根据节点的时间元数据对检索结果进行重新排序**。它适用于文档内容具有时间属性的场景，确保**更新、更近的信息优先呈现**给 LLM。

时间排序的根本目标是**让 LLM 优先获得最新、最有时效性的信息**，具体体现在：

1\.**确保时效性**：最新生成的文档节点排在前面，避免过时信息干扰回答

2\.**平衡相关性与新鲜度**：通过混合排序，在语义相关和时间新旧之间取得平衡

3\.**适应动态知识**：对于频繁更新的领域（如新闻、产品信息、政策法规等），保证答案基于最新数据

##### 1\. 实现代码

```Plaintext

from datetime import datetime, timedelta
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import TimeWeightedPostprocessor
from base_llm import llm, embed_model

# 1. 构造带时间戳的文档数据
now = datetime.now()
documents = [
    Document(
        text="我们的退货政策是：在30天内可退货。",
        metadata={"created_at": (now - timedelta(days=40)).timestamp()}  # 较早
    ),
    Document(
        text="我们最近更新了退货政策，现在是15天内可退货。",
        metadata={"created_at": (now - timedelta(days=10)).timestamp()}  # 比较新
    ),
    Document(
        text="退货政策是，目前可以20天内可退货",
        metadata={"created_at": (now - timedelta(days=1)).timestamp()}  # 最新
    )
]

# 2. 构建索引和向量检索器
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
retriever = index.as_retriever(similarity_top_k=5)


time_postprocessor = TimeWeightedPostprocessor(
    time_decay=0.1,
    top_k=3,  # 最多返回3条
    # 在确定使用时间排序前 一定要先确保每个节点都有元数据存在
    last_accessed_key="created_at"
)

# 4. 构建 QueryEngine
query_engine = RetrieverQueryEngine.from_args(
    llm=llm,
    retriever=retriever,
    node_postprocessors=[time_postprocessor]
)

# 5. 用户提问
query = "你们现在的退货政策是怎样的？"
response = query_engine.query(query)
print("回答：", response)

print('=======原始检索=======')
retrieved_nodes = retriever.retrieve(query)
for i, node in enumerate(retrieved_nodes):
    print(f"{i+1}. score={node.score:.4f}")
    print(node.text[:50])
    print()


processed_nodes = time_postprocessor.postprocess_nodes(retrieved_nodes)

print("\n===== 时间排序节点 =====")
for i, node in enumerate(processed_nodes):
    print(f"{i + 1}. score={node.score:.4f}")
    print(node.text[:50])
    print()
```

- 功能架构

![064\.png](图片和附件/064.png)



### 六\.PDF处理

**问题描述:**

之前我们讲过我们半结构化数据对于传统 RAG 来说可能具有挑战性，文本拆分可能会分解表，从而损坏检索中的数据；嵌入表可能会给语义相似性搜索带来挑战。对于这个问题可以通过构建摘要索引解决这个问题：分别为每个文本和表格数据创建摘要或者转换成其他处理方便的格式\(html, md, json\)

#### 1\. MinerU 是什么？

MinerU 是**上海人工智能实验室 OpenDataLab** 开源的一站式文档智能解析工具

主要目标：

- 把**复杂排版 PDF**（公式 \+ 表格 \+ 多栏 \+ 图表 \+ 脚注 \+ 页眉页脚） → 转为**结构清晰、可直接喂大模型**的 Markdown / JSON

核心亮点（目前开源 PDF 解析工具中最强之一）：

- 公式 → LaTeX（极高准确率）

- 表格 → Markdown 表格 / HTML

- 图片 → 提取 \+ 可配图描述 \- 支持**扫描件 / 生图 PDF**（自动 OCR，109 种语言）

- 自动去除页眉、页脚、页码、重复脚注 \- 保留阅读顺序（单栏/双栏/复杂混排都比较聪明）

- 支持中英文混排、科技文献效果显著优于大部分商业工具

适用场景：

- 学术文献批量清洗 → RAG / 知识库

- 财报 / 招股书 / 法律文件结构化提取

- LLM 预训练 / SFT 高质量语料准备

- 个人文献管理、阅读增强

项目地址：https://github\.com/opendatalab/MinerU

在线体验（限速/限量）：https://mineru\.net/

#### 2\. 三种使用方式对比

|使用方式|难度|速度|表格识别|公式 LaTeX|批量处理|适合人群|
|---|---|---|---|---|---|---|
|在线网页版|★☆☆|较慢|部分|部分|不方便|临时体验、少量文件|
|一键桌面客户端|★★☆|快|优秀|优秀|支持|大多数普通用户|
|本地命令行/Python|★★★|最快|完全可控|完全可控|极强|开发者 / 批量需求|

##### 1\. 方式一

1. 打开 https://mineru\.net/

2. 拖入或上传 pdf 文件（≤200MB 左右）

3. 等待解析完成 → 下载 \.md 文件

**注意事项**：

- 图片是网络链接（在线版不下载图片实体）

- 复杂表格可能仍以图片形式存在

- 免费额度有限，高峰期要排队

##### 2\. 方式二

官方已推出跨平台客户端（Win / Mac / Linux）

下载地址：https://mineru\.net/ → 客户端下载区

操作步骤：

1. 安装后打开 MinerU 客户端

2. 选择「PDF 解析」模块

3. 拖入文件或文件夹（支持批量）

4. 重要参数设置（建议）：

    - 公式识别：开启    \- 表格识别：开启（推荐 table\-transform: markdown）

    - 输出格式：Markdown（推荐） / JSON（结构化需求）

5. 点击「开始解析」→ 得到输出文件夹

![065\.png](图片和附件/065.png)

##### 3\. 方式三

- 模块下载

```Plaintext
pip install -U "mineru[all]"
pip install hf_xet
```

- 首次模型下载

```Plaintext
from modelscope import snapshot_download

snapshot_download('OpenDataLab/PDF-Extract-Kit-1.0', local_dir=r'D:\LLM\Local_model\PDF-Extract-Kit-1.0')
```

- 添加模型文件配置

```Plaintext
{
  "models-dir": {
    "pipeline": "D:/LLM/Local_model/PDF-Extract-Kit-1.0"
  }
}
mineru.json文件
```

- 替换代码

```Plaintext
import os
import re
from pathlib import Path

LOCAL_MODEL_DIR = r"D:\LLM\Local_model\PDF-Extract-Kit-1.0"
LOCAL_MINERU_CONFIG = os.path.join(os.path.dirname(__file__), "mineru.json")


os.environ["MINERU_MODEL_SOURCE"] = "local"
os.environ["MINERU_TOOLS_CONFIG_JSON"] = LOCAL_MINERU_CONFIG

from mineru.cli.common import do_parse
from mineru.data.data_reader_writer import FileBasedDataWriter

# ===== 输入 PDF =====
pdf_path = "../data_file/2020-03-17__厦门灿坤实业股份有限公司__200512__闽灿坤__2019年__年度报告.pdf"

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# ===== 输出目录 =====
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# ===== MinerU 要求：必须是「列表」 =====
pdf_file_names = [os.path.basename(pdf_path)]
pdf_bytes_list = [pdf_bytes]
p_lang_list = [""]   # 自动语言识别

# ===== 图片 writer =====
img_writer = FileBasedDataWriter(
    os.path.join(output_dir, "images")
)


def fix_markdown_headings(md_path):
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    new_lines = []

    for line in lines:
        stripped = line.strip()

        if not stripped.startswith("#"):
            new_lines.append(line)
            continue

        title = stripped.lstrip("#").strip()

        if re.match(r"^第[一二三四五六七八九十]+节", title):
            new_lines.append(f"# {title}")
        elif re.match(r"^[一二三四五六七八九十]+、", title):
            new_lines.append(f"## {title}")
        elif re.match(r"^(\d+|[a-zA-Z])、", title):
            new_lines.append(f"### {title}")
        elif re.match(r"^（\d+）", title):
            new_lines.append(f"#### {title}")
        elif title.startswith(("√", "□", "单位：")):
            new_lines.append(title)
        else:
            new_lines.append(line)

    Path(md_path).write_text("\n".join(new_lines), encoding="utf-8")


def fix_output_markdown_headings(output_dir):
    for md_path in Path(output_dir).rglob("*.md"):
        fix_markdown_headings(md_path)


if __name__ == '__main__':

    # ===== 核心解析 =====
    do_parse(
        pdf_file_names=pdf_file_names,
        pdf_bytes_list=pdf_bytes_list,
        p_lang_list=p_lang_list,
        output_dir=output_dir,
        img_writer=img_writer,
        parse_method="auto"
    )

    fix_output_markdown_headings(output_dir)
```

### 七\. RAG实战\-金融助手

- 在金融领域，开发一个能够仿效专家解读上市公司年报的智能对话系统，一直是人工智能技术进步的关键目标。尽管目前的人工智能系统在文本对话领域已展现出显著的进展，但在更为精细、更具挑战性的金融领域交互方面，其性能尚需进一步提升。因此，我们致力于在现有大型模型的基础上，通过精细化调整、大型与小型模型的协同工作以及利用向量数据库等尖端技术，旨在进一步增强人工智能模型的性能

\*\*DM文档表格解析 \*\*

- MarkdownElementNodeParser 是 LlamaIndex 中专门用于处理 Markdown 文档 的高级节点解析器（Node Parser），继承自 BaseElementNodeParser。

- 它最核心的特点是：将 Markdown 文档拆分成普通文本节点 \+ 结构化对象节点（尤其是表格），特别适合包含大量表格、代码块、标题的复杂 Markdown 内容。

- 实现代码

```Plaintext
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from base_llm import llm, embed_model

# LlamaIndex默认使用的大模型被替换为百炼
Settings.llm = llm
# 加载本地的嵌入模型
Settings.embed_model = embed_model

# 自定义你的提示词
# 建议：明确告诉 AI 保持简洁，并提取关键的关键词（如命令、字段名）
MY_CUSTOM_SUMMARY_QUERY = (
    "你是一个技术文档解析助手。请提取以下 Markdown 表格或内容的极简摘要。"
    "要求：1. 严禁啰嗦；2. 必须包含表格中的关键实体词（如 API 路径、参数名、状态码）；"
    "3. 如果是代码相关内容，请保留具体的命令名称。请用中文摘要"
)


# 读取文件+解析文档
md_docs = documents = SimpleDirectoryReader(
        input_files=["../data_file/test.md"]
    ).load_data()
# 是否建立前后节点
parser1 = MarkdownElementNodeParser(include_prev_next_rel=True, summary_query_str=MY_CUSTOM_SUMMARY_QUERY)
nodes = parser1.get_nodes_from_documents(md_docs)
# print(nodes)

for node in nodes:
    print()
    print(node.model_dump_json(indent=2))
```

#### 1\. 实现代码

```Plaintext
from pathlib import Path
import re
import chromadb
from base_llm import embed_model, llm
from llama_index.core import (
    Settings,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    MarkdownElementNodeParser,
    get_leaf_nodes,
)
from llama_index.core.schema import Document
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.vector_stores.chroma import ChromaVectorStore


MD_PATH = Path(
    r"D:\python_project\python_ai_code\llama_project\day07\output\2020-03-17__厦门灿坤实业股份有限公司__200512__闽灿坤__2019年__年度报告.pdf\auto\2020-03-17__厦门灿坤实业股份有限公司__200512__闽灿坤__2019年__年度报告.pdf.md"
)
INDEX_ID = "tsannkuen_2019_auto_merging"
PERSIST_DIR = Path("./storage_auto_merging")
RERANK_MODEL_PATH = r"D:\LLM\Local_model\BAAI\bge-reranker-large"
SIMILARITY_TOP_K = 8
RERANK_TOP_N = 4
AUTO_MERGE_RATIO = 0.5





def build_storage_context():
    return StorageContext.from_defaults(
        docstore=MongoDocumentStore.from_uri(
            uri="mongodb://127.0.0.1:27017",
            db_name="llama_md_report",
            namespace='merging_docstore',
        ),
        vector_store=build_vector_store(),
        persist_dir=str(PERSIST_DIR) if index_persisted() else None,
    )


def build_vector_store():
    chroma_client = chromadb.PersistentClient(path="./merging_chroma")
    chroma_collection = chroma_client.get_or_create_collection(
        name="tsannkuen_2019_leaf_nodes"
    )
    return ChromaVectorStore(chroma_collection=chroma_collection)


def split_by_h1():
    text = MD_PATH.read_text(encoding="utf-8")
    sections = re.split(r"(?=^# )", text, flags=re.MULTILINE)
    results = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        # 提取 H1 标题
        match = re.match(r"^#\s+(.+)", section)
        h1_title = match.group(1).strip() if match else "未知标题"
        results.append(Document(
            text=section,
            metadata={"h1_title": h1_title},
        ))
    return results

def build_pipeline():
    hierarchical_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 512],
        chunk_overlap=20,
    )
    markdown_parser = MarkdownElementNodeParser(
        llm=llm,
        nested_node_parser=hierarchical_parser,
        num_workers=2,
        show_progress=True,
    )
    title_extractor = TitleExtractor(
        llm=llm,
        nodes=5,
        num_workers=2,
        show_progress=True,
    )
    return IngestionPipeline(
        transformations=[
            markdown_parser,
            title_extractor,
        ],
        cache=IngestionCache(
            cache=RedisKVStore(redis_uri="redis://127.0.0.1:6379"),
            collection='ingestion_cache',
        ),
        disable_cache=False,
    )


def parse_nodes():
    documents = split_by_h1()
    pipeline = build_pipeline()
    return list(pipeline.run(documents=documents, show_progress=True))


def index_persisted():
    return (PERSIST_DIR / "index_store.json").exists()


def build_or_load_index():
    Settings.llm = llm
    Settings.embed_model = embed_model

    storage_context = build_storage_context()
    if index_persisted():
        print(f"加载本地 index: {PERSIST_DIR}")
        index = load_index_from_storage(
            storage_context,
            index_id=INDEX_ID,
            embed_model=embed_model,
        )
        return index

    print("未发现本地 index，开始读取 Markdown 并摄取解析。")
    nodes = parse_nodes()
    leaf_nodes = get_leaf_nodes(nodes)
    storage_context.docstore.add_documents(nodes, allow_update=True)
    print(f"父子全量 nodes 已写入 MongoDB: {len(nodes)}")
    print(f"用于向量索引的 leaf nodes: {len(leaf_nodes)}")
    index = VectorStoreIndex(
        leaf_nodes,
        storage_context=storage_context,
        embed_model=embed_model,
        store_nodes_override=True,
        show_progress=True,
    )
    index.set_index_id(INDEX_ID)
    index.storage_context.persist(persist_dir=str(PERSIST_DIR))
    print(f"index 已持久化到: {PERSIST_DIR}")
    return index


def build_auto_merging_retriever(index):
    vector_retriever = index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)
    return AutoMergingRetriever(
        vector_retriever,
        index.storage_context,
        simple_ratio_thresh=AUTO_MERGE_RATIO,
        verbose=True,
    )


def build_reranker():
    return SentenceTransformerRerank(
        model=RERANK_MODEL_PATH,
        top_n=RERANK_TOP_N,
    )


def build_response_synthesizer():
    return get_response_synthesizer(
        llm=llm,
        response_mode="compact",
        verbose=True,
    )

def build_query_engine(retriever):
    reranker = build_reranker()
    response_synthesizer = build_response_synthesizer()
    return RetrieverQueryEngine.from_args(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[reranker],
    )


if __name__ == "__main__":
    index = build_or_load_index()
    retriever = build_auto_merging_retriever(index)
    query_engine = build_query_engine(retriever)
    questions = [
        "结合营业收入、净利润和现金流，评价公司2019年的经营质量。",
        "公司2019年的盈利能力变动主要受哪些因素影响？",
        "年报中哪些内容说明公司面临市场竞争风险？",
        "请对比公司2019年和2018年的主要财务指标。",
        "公司2019年的收入结构和业务重点是什么？",
        "从年报看，公司未来发展的主要挑战是什么？",
    ]
    for qa in questions:
        response = query_engine.query(qa)
        print('问题:', qa)
        print('回答:', response)
```

