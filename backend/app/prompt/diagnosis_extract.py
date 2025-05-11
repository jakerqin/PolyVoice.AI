DIAGNOSIS_EXTRACT_SYSTEM_PROMPT = """
请分析以下{diagnosis_type}诊断内容，提取关键问题和搜索关键词：

```
{diagnosis_content}
```

请提取正整理用户语言中的问题，以便在网上搜索相关教学资源。
"""