# AI Cut 多屏媒体控制系统

该项目为线下酒吧等场景提供一个可以集中管控所有屏幕播放内容的软件雏形，包含：

- 基于 FastAPI 的后台服务，负责屏幕、素材、播放列表管理与实时指令下发
- 简洁大气的 Web 控制台，用于配置门店屏幕、上传素材并编排播放列表
- 基于 Video.js 的前端播放器，可部署在每块显示屏终端，实现视频/图片播放、自适应裁切与多种循环模式

## 目录结构

```
backend/    FastAPI 后端服务
frontend/   控制台与屏幕播放器静态页面
```

## 快速体验

1. 安装依赖并启动后端
   ```bash
   cd backend
   poetry install
   poetry run uvicorn app.main:app --reload
   ```
2. 浏览控制台：<http://127.0.0.1:8000/control/>
3. 在屏幕终端访问播放器：<http://127.0.0.1:8000/player/?screen=1>

> 提示：首次打开播放器会提示输入屏幕 ID，需先在控制台创建屏幕并分配播放列表。

更多后台接口说明参见 [`backend/README.md`](backend/README.md)。
