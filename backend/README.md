# 多屏媒体控制后台服务

该 FastAPI 应用负责门店多块屏幕的资产管理、播放列表编排以及实时控制。它使用 SQLite 持久化数据，并通过 WebSocket 与屏幕终端保持连接。

## 快速启动

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

服务默认监听 `http://127.0.0.1:8000`，静态控制台与播放器页面分别挂载在：

- 控制台：`http://127.0.0.1:8000/control/`
- 播放端：`http://127.0.0.1:8000/player/?screen=<屏幕ID>`

## 核心能力

- **资产管理**：登记视频、图片或流媒体地址并记录元数据
- **播放列表编排**：支持顺序、循环列表、单素材循环，并可设置单项裁切/展示时长
- **屏幕控制**：为每块屏幕分配播放列表、设置裁切区域、适配模式与音量
- **实时通信**：通过 WebSocket 推送播放指令、音量调整、强制刷新等消息给终端

## 主要接口

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| `POST /assets` | 创建素材资产 |
| `GET /assets` | 查询素材列表 |
| `POST /playlists` | 创建播放列表及条目 |
| `PUT /playlists/{id}/items` | 替换播放条目 |
| `POST /screens` | 登记屏幕 |
| `POST /screens/{id}/playlist` | 为屏幕分配播放列表 |
| `POST /commands/screens/{id}` | 向屏幕推送即时命令 |

WebSocket 端点：`/screens/ws/{screen_id}`。

## 播放器集成

播放终端页面使用 Video.js 作为成熟播放器内核，根据后台下发的播放列表自动切换素材，支持图片展示与视频/流媒体播放，并根据裁切信息调整展示比例。
