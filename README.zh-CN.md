<!-- anchor: chefs-pick-oss-starter-workspace -->
# Chef's Pick OSS Starter — 开发工作区

[English](README.md) · **简体中文**

> 英文版是规范版本。本页与 [README.md](README.md) 不一致时，以英文版为准。

<!-- translation-of: README.md sha256:b46563346c02a932 -->

这是 [chefs-pick-oss-starter](https://github.com/anyingiit/chefs-pick-oss-starter)
模板仓库的开发与维护工作区：规格、选型调研、校验工具都在这里，模板仓库只承载 `template/` 的内容。

<!-- anchor: layout -->
## 目录结构

| 路径 | 说明 | 是否发布 |
|---|---|---|
| `template/` | 模板仓库默认分支的全部内容 | 是 |
| `specs/001-chefs-pick-starter/` | 最初的规格、计划、任务、调研与契约 | 否 |
| `specs/002-english-first-docs/` | 文档改为英文规范版的改造 | 否 |
| `specs/003-workspace-self-compliance/` | 让工作区遵守它自己交付的规矩 | 否 |
| `tools/` | 校验与数据刷新脚本及其测试 | 否 |
| `.specify/`、`.claude/` | Spec Kit 与 AI 助手的配置 | 否 |

`template/` 共 28 个文件。**只有 `template/` 会被发布。** 校验项 C02 会拦截任何混入其中的开发文件。

<!-- anchor: common-commands -->
## 常用命令

```bash
python3 tools/check_template.py              # 27 项结构校验
python3 tools/check_template.py --release    # 发布门禁，核实日期收紧到 30 天
python3 tools/check_template.py --update-digests  # 刷新译本的来源标记
python3 -m unittest discover -s tools/tests  # 单元测试
python3 tools/verify_sources.py              # 只读复核认可度数据
python3 tools/verify_sources.py --write      # 写入刷新后的认可度数据
```

刷新认可度数据需要已登录的 `gh` 命令行工具。复核周期、重新评估的触发条件与发布门禁，见
`template/.github/chefs-pick/MAINTAINING.md`。

<!-- anchor: publishing -->
## 发布

发布指的是把 `template/` 的内容复制到模板仓库的默认分支上。工作区里的其他内容一概不发布。
完整背景见 [quickstart.md](specs/001-chefs-pick-starter/quickstart.md) 的 B、C、D 三部分。

用哪一套步骤，取决于模板仓库里是否已经有内容。

**首次发布，目标是刚建好的空仓库。** 把 `template/` 的内容复制进空仓库的克隆后提交即可，或者运行：

```bash
git subtree split --prefix=template -b publish
git push <模板仓库远程名> publish:main
```

**此后的每一次发布。** 在模板仓库的克隆里操作，在已有内容之上追加一个提交：

```bash
# 后续发布：在模板仓库的克隆里替换内容，追加一个提交
git -C <克隆路径> fetch origin main
git -C <克隆路径> checkout main
cp -a template/. <克隆路径>/
git -C <克隆路径> add -A
git -C <克隆路径> commit -m "docs: sync template content"
git -C <克隆路径> push origin main
```

复制完、提交前，克隆的工作树应当与 `template/` 逐字节相同，可用
`diff -r --exclude=.git <克隆路径> template` 当场核对。

有三件事必须知道，弄错会损坏已发布的仓库：

- 绝不要对模板仓库强制推送。
- 推送被拒，意味着模板仓库上有工作区没有的提交；此时应当停下来排查，而不是强推。
- `git subtree split` 切出的历史与模板仓库没有共同祖先，只能靠 `--force` 推上去。它适用于向空仓库的首次发布，此后一概不用。

最后这一条不是假想。模板仓库上有 `v1.0.0` 标签，强推一套 split 历史会让该标签指向的提交
从任何分支都不再可达。

也不要在模板仓库上直接合并 Dependabot 的合并请求，原因见 MAINTAINING 的「动作版本更新」一节。

<!-- anchor: license -->
## 许可证

MIT，与模板仓库一致。模板自身的许可证与署名说明见
`template/.github/chefs-pick/LICENSE`。
