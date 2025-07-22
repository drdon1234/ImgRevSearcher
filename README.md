# 聚合图片反搜项目

> **核心代码基于**：[kitUIN/PicImageSearch](https://github.com/kitUIN/PicImageSearch)

## 支持的搜索引擎

| 引擎       | 网址                                  |
|-----------|-------------------------------------|
| AnimeTrace | [https://www.animetrace.com/](https://www.animetrace.com/)      |
| Baidu      | [https://graph.baidu.com/](https://graph.baidu.com/)            |
| Bing       | [https://www.bing.com/images/search](https://www.bing.com/images/search) |
| Copyseeker | [https://copyseeker.net/](https://copyseeker.net/)              |
| E-Hentai   | [https://e-hentai.org/](https://e-hentai.org/)                  |
| Google Lens| [https://lens.google.com/](https://lens.google.com/)            |
| SauceNAO   | [https://saucenao.com/](https://saucenao.com/)                  |
| Tineye     | [https://tineye.com/search/](https://tineye.com/search/)        |

## 快速开始使用

1. **配置代理**  
   编辑根目录的 `config.py` 中的 `PROXIES` 参数（墙内用户无代理时默认只能用百度引擎）

2. **查看示例模板**  
   参考 `test_templates` 目录下的代码模板，可根据需求选择合适的引擎调用方式

## 重要说明

### Google Lens 引擎的 Cookie 强制要求

请按以下步骤获取无痕模式下有效的 Google Cookie：

1. 打开浏览器无痕窗口  
2. 按 `F12` 打开开发者工具，切换到“网络(Network)”标签，过滤“Fetch/XHR”  
3. 访问 [https://www.google.com/](https://www.google.com/)  
4. 找到访问google主域名的请求，查看请求头中的 `Cookie` 字段  
5. 复制完整的 Cookie 内容，替换到 `config.py` 中 `DEFAULT_COOKIES` 的 `google_lens` 项

**注意：**  
- 无痕模式cookie格式一般为 `AEC= ;NID= `，有效期限约6个月
- 登录状态cookie有效期极短，不建议使用

# 图片搜索API参数说明文档

## AnimeTrace

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索  
3. 📄 通过提供base64编码图片搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件，可以是路径字符串、字节数据或Path对象 |
| `base64` | `Optional[str]` | ❌ | Base64编码的图片数据 |
| `model` | `Optional[str]` | ❌ | 识别模型，默认为None |
| `**kwargs` | `Any` | ❌ | 传递给请求的其他参数 |

#### 可用模型
- `anime_model_lovelive`
- `pre_stable` 
- `anime`
- `full_game_model_kira`

### 返回值

```python
AnimeTraceResponse
```
包含：
- ✨ 检测到的角色及其来源作品
- 📍 边界框坐标
- 🏷️ 其他元数据（trace_id、AI检测标识）

### 异常

- `ValueError`: 如果未提供`url`、`file`或`base64`中的任何一个

> **⚠️ 注意事项**
> - 只能提供`url`、`file`或`base64`中的一个
> - URL和base64搜索使用JSON POST请求
> - 文件上传使用multipart/form-data POST请求

## Baidu

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件 |
| `**kwargs` | `Any` | ❌ | 传递给父类的其他参数 |

### 返回值

```python
BaiDuResponse
```
包含搜索结果和元数据。如果未找到匹配项或存在'noresult'卡片，则返回空结果。

### 异常

- `ValueError`: 如果既未提供`url`也未提供`file`

> **⚠️ 注意事项**
> - 只能提供`url`或`file`中的一个
> - 搜索过程涉及对百度API的多次HTTP请求
> - 响应格式因是否找到匹配项而异

## Bing

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件 |
| `**kwargs` | `Any` | ❌ | 传递给父类的其他参数 |

### 返回值

```python
BingResponse
```
包含搜索结果和元数据的对象。

### 异常

- `ValueError`: 如果既未提供`url`也未提供`file`
- `ValueError`: 如果上传图片时无法找到BCID

## Copyseeker

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件 |
| `**kwargs` | `Any` | ❌ | 传递给父类的其他参数 |

### 返回值

```python
CopyseekerResponse
```
如果无法获得发现ID，则返回空响应。

## EHentai/ExHentai

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件 |
| `**kwargs` | `Any` | ❌ | 传递给父类的其他参数 |

### 返回值

```python
EHentaiResponse
```
包含：
- 📚 相似图库条目
- 🔗 图库URL和标题
- 📊 相似度评分
- 🏷️ 搜索结果中的其他元数据

### 异常

- `ValueError`: 如果既未提供`url`也未提供`file`
- `RuntimeError`: 如果在ExHentai上搜索时没有适当的身份验证

> **🔐 重要提示**
> - 对于ExHentai搜索，必须在request_kwargs中提供有效的cookies
> - 搜索行为受初始化时设置的covers、similar和exp标志影响

## GoogleLens

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|---------|------|
| `base_url` | `str` | `"https://lens.google.com"` | Google Lens搜索的基础URL |
| `search_url` | `str` | `"https://www.google.com"` | Google搜索结果的基础URL |
| `search_type` | `Literal` | `"all"` | 搜索类型 |
| `q` | `Optional[str]` | `None` | 搜索查询参数（不适用于'exact_matches'） |
| `hl` | `str` | `"en"` | 语言参数 |
| `country` | `str` | `"US"` | 区域设置参数 |
| `**request_kwargs` | `Any` | - | 网络请求的其他参数 |

#### 搜索类型选项
- `all` - 全部搜索
- `products` - 产品搜索
- `visual_matches` - 视觉匹配
- `exact_matches` - 精确匹配

### 异常

- `ValueError`: 如果search_type为'exact_matches'且提供了q参数
- `ValueError`: 如果search_type不是有效选项之一

## SauceNAO

**支持的搜索方式：**
1. 🔗 通过图片URL搜索
2. 📁 通过上传本地图片文件搜索

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | `Optional[str]` | ❌ | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | ❌ | 本地图片文件 |
| `**kwargs` | `Any` | ❌ | 传递给父类的其他参数 |

### 返回值

```python
SauceNAOResponse
```
包含：
- 🎯 带有相似度评分的搜索结果
- 🖼️ 来源信息和缩略图
- 📈 其他元数据（状态码、搜索配额）

### API限制

#### 免费账户限制
| 限制类型 | 数量 |
|----------|------|
| 每日搜索次数 | 150次 |
| 每30秒搜索次数 | 4次 |

> **📊 结果排序**
> 结果按相似度评分降序排列

## Tineye

使用图片URL或本地图片文件搜索网络上的匹配图片。初始搜索后，检索匹配图片的域名信息。

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|---------|------|
| `url` | `Optional[str]` | - | 要搜索的图片URL |
| `file` | `Union[str, bytes, Path, None]` | - | 本地图片文件路径 |
| `show_unavailable_domains` | `bool` | `False` | 是否包含来自不可用域名的结果 |
| `domain` | `str` | `""` | 过滤特定域名的结果 |
| `sort` | `str` | `"score"` | 排序标准 |
| `order` | `str` | `"desc"` | 排序顺序 |
| `tags` | `str` | `""` | 逗号分隔的过滤标签 |
| `**kwargs` | `Any` | - | 其他关键字参数 |

### 排序选项

#### sort参数
| 值 | 说明 |
|----|------|
| `score` | 按匹配评分排序 |
| `crawl_date` | 按爬取日期排序 |
| `size` | 按图片大小排序 |

#### order参数 + 效果组合
| sort + order | 效果 |
|--------------|------|
| `score` + `desc` | 最佳匹配优先 ⭐ |
| `score` + `asc` | 最多变化优先 |
| `crawl_date` + `desc` | 最新图片优先 🆕 |
| `crawl_date` + `asc` | 最旧图片优先 📅 |
| `size` + `desc` | 最大图片优先 📏 |

### 返回值

```python
TineyeResponse
```
包含搜索结果、域名信息和元数据。

## 📝 通用注意事项

> **🚨 重要提醒**
> - 所有服务都只能提供`url`或`file`参数中的一个
> - 建议在使用前检查各服务的API限制和使用条款
> - 某些服务可能需要身份验证或API密钥