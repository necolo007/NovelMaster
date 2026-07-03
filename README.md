# NovelMaster

> AI 网文小说生成系统。通过多角色协作（架构师 → 写手 → 编辑），将灵感转化为完整小说，支持一致性追踪与多格式导出。

## 快速开始

```bash
# 初始化新小说项目
python3 skills/novel-master/scripts/project_manager.py init "星辰杂货铺" --genre kehuan

# 校验项目结构
python3 skills/novel-master/scripts/project_manager.py validate projects/星辰杂货铺

# 完成框架 + 写作阶段后，导出成品
python3 skills/novel-master/scripts/export_txt.py projects/星辰杂货铺
```

## 核心流水线

```
灵感/素材 → 创建项目 → [流派模板] → 架构师六大确认
→ [素材搜集] → 写手逐章生成 → 编辑审核
→ 后期处理 → 导出（TXT / EPUB / Markdown）
```

## 核心目录

| 目录 | 用途 |
|------|------|
| `skills/novel-master/SKILL.md` | 权威流水线工作流 |
| `skills/novel-master/references/` | 角色定义（架构师、写手、编辑）+ 共享规范 |
| `skills/novel-master/templates/` | 框架规格参考、执行锁参考、流派模板 |
| `skills/novel-master/workflows/` | 独立子工作流（头脑风暴、续写、修订、大纲展开、人物深挖） |
| `skills/novel-master/scripts/` | Python 工具脚本（项目管理、审核器、导出器） |
| `skills/novel-master/examples/` | 示例项目 |
| `projects/` | 用户项目工作区 |
| `ingredient/` | 参考网文与灵感素材 |

## 入口指引

AI Agent 入口：先读 [`AGENTS.md`](AGENTS.md)，再读 [`skills/novel-master/SKILL.md`](skills/novel-master/SKILL.md)。

人类阅读入口：设计文档见 [`novel-master-design.md`](novel-master-design.md)。
