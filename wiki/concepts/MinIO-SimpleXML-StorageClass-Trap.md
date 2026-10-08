# MinIO Java SDK SimpleXML StorageClass 解析陷阱与热修复方案

## 1. 现象与报错堆栈
在调用 MinIO Java SDK 8.5.x 列举分片上传任务（如 `listMultipartUploads`）或查询 S3 结果时，后台抛出如下反射与反序列化异常：
```log
Caused by: io.minio.errors.XmlParserException: org.simpleframework.xml.core.ValueRequiredException: Empty value for @org.simpleframework.xml.Element(name="StorageClass", type=void.class, data=false, required=true) on field 'storageClass' private java.lang.String io.minio.messages.Upload.storageClass in class io.minio.messages.Upload at line 2
	at io.minio.Xml.unmarshal(Xml.java:55) ~[minio-8.5.17.jar:8.5.17]
	at io.minio.S3Base.lambda$listMultipartUploadsAsync$31(S3Base.java:3241) ~[minio-8.5.17.jar:8.5.17]
```

## 2. 根因剖析 (Root Cause)
1. **SimpleXML 严格校验模式**：
   MinIO Java SDK 内部使用 `org.simpleframework.xml` 解析 S3 服务端返回的 XML。
   在 `io.minio.messages.Upload` 类中，`storageClass` 字段标注为 `@Element(name="StorageClass")`，SimpleXML 默认其 `required = true`。
2. **服务端返回空标签**：
   部分 MinIO 版本或私有云 S3 兼容网关对于默认存储类型的分片上传任务，返回的 XML 为 `<StorageClass></StorageClass>` 或 `<StorageClass/>`。
3. **反序列化崩溃**：
   SimpleXML 在遇到空值且 `required=true` 的元素时，会直接抛出 `ValueRequiredException: Empty value for @org.simpleframework.xml.Element`，导致整个 XML 解析失败。

## 3. 负面证据 (Negative Anti-Patterns)
* **不可行方案 1**：修改 `io.minio.messages.Upload` 源码（位于第三方闭源或已打包 jar 中，难以直接侵入）。
* **不可行方案 2**：在应用层 try-catch 吞掉异常（会导致孤立分片清理任务完全无法获取到待清理的分片列表）。

## 4. 经过验证的最佳解决方案 (Validated Solution)
通过为 `MinioClient` 注入自定义的 `OkHttpClient`，并配置网络拦截器（Interceptor）：
* 仅拦截 XML 类型响应（`contentType.subtype().contains("xml")`），保证文件二进制数据传输零开销；
* 检查如果 XML 包含空 `StorageClass` 标签（`<StorageClass>\s*</StorageClass>|<StorageClass\s*/>`），将其动态重写规范化为 `<StorageClass>STANDARD</StorageClass>`；
* SimpleXML 即可正常将 `storageClass` 属性映射为字符串 `"STANDARD"`，彻底消除崩溃。

```java
OkHttpClient httpClient = new OkHttpClient.Builder()
        .addInterceptor(chain -> {
            Response response = chain.proceed(chain.request());
            ResponseBody body = response.body();
            if (body != null) {
                MediaType contentType = body.contentType();
                if (contentType != null && (contentType.subtype().contains("xml") || contentType.type().contains("xml"))) {
                    String bodyString = body.string();
                    if (bodyString.contains("StorageClass")) {
                        bodyString = bodyString.replaceAll("<StorageClass>\\s*</StorageClass>|<StorageClass\\s*/>", "<StorageClass>STANDARD</StorageClass>");
                    }
                    ResponseBody newBody = ResponseBody.create(bodyString, contentType);
                    return response.newBuilder().body(newBody).build();
                }
            }
            return response;
        })
        .build();

MinioClient minioClient = MinioClient.builder()
        .endpoint(url)
        .credentials(accessKey, secretKey)
        .httpClient(httpClient)
        .build();
```
