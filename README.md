# 聚合图片反搜项目

---

### 核心代码来自: https://github.com/kitUIN/PicImageSearch

---

## 支持的引擎:
| Engine             | Website                              |
|--------------------|--------------------------------------|
| AnimeTrace         | <https://www.animetrace.com/>        |
| Baidu              | <https://graph.baidu.com/>           |
| Bing               | <https://www.bing.com/images/search> |
| Copyseeker         | <https://copyseeker.net/>            |
| E-Hentai           | <https://e-hentai.org/>              |
| Google Lens        | <https://lens.google.com/>           |
| SauceNAO           | <https://saucenao.com/>              |
| Tineye             | <https://tineye.com/search/>         |

---

## 使用方法
1. 配置根目录下 "config.py" 的 "PROXIES" 参数（否则墙内用户只能使用百度引擎）
2. 查看 "test_templates" 目录下代码模板，根据需要自行选择引擎

---

## 注意事项
### google_lens引擎强制要求 cookie

谷歌相关网站 cookie 捕获方法：
  1. 打开浏览器无痕模式
  2. 使用 "F12" 打开开发者面板
  3. 点击 "网络" 或 "Network" -> 点击 "Fetch/XHR"
  4. 访问 https://www.google.com/
  5. 选中任意一条访问 google 主域名的网络请求，查看 "请求标头" 的 "Cookie" 参数
  6. 全选复制并替换根目录下 "config.py" -> "DEFAULT_COOKIES" -> "google_lens" 对应的 cookie

无痕账户的 cookie 格式应当是 "AEC= ; NID= "  
每个无痕账户的 cookie 有效期限为 6 个月  
必须使用无痕账户 cookie，登录账户 cookie 有效期极短

---
