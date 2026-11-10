# 奶蛙 3D 源文件

- naiwa.blend：Blender 工程（模型 + 骨骼 + 4 个动作：idle / walk / laugh / battle），用 Blender 4.2+ 打开
- 模型由 TRELLIS.2 根据正面图生成（MIT），在 Blender 里减面、调色、绑骨骼
- *.py：重建流程脚本，按 clean → rig → posetest → reweight → headfix → anims 顺序运行
- 网页用的导出文件：../assets/naiwa.glb
