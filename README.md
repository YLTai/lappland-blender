# 原版五星拉普兰德双剑 · Blender Cosplay 复原

从空白脚本起步，以用户提供的十二张原版 / E2 / 幼狼的牙齿参考图完成 bpy 建模。**不包含典雅噩兆或荒芜拉普兰德结构。**

## 获取与运行

现有 **Blender Build** Actions 在 main 的 `model.py` / `render.py` 更新后运行，上传 **lappland-build**，内含 `output/` 与 `renders/`。使用 Blender 4.2.1 可重复生成：

```sh
blender -b --python model.py
blender -b --python render.py
```

## 交付内容

`lappland_original_pair.blend` 为可编辑分件双剑；同名 `.glb` 带材质且无外部依赖；`lappland_sword_A_mm.stl`、`lappland_sword_B_mm.stl` 为同一母型的两个单剑文件；`lappland_pair_mm.stl` 包含并置双剑。STL 数值单位是毫米，GLB/Blender 坐标单位是米。STL 只保存几何，颜色参照 GLB 与 PNG。

十四张 PNG 覆盖双剑正面、单剑正反面、侧面、顶面、实际 45° 双剑/护手/刀尖、护手正反面和侧面、刀尖正面、握柄及无材质轮廓检查图。BLEND 内保留灯光、相机和可编辑部件，合并导出实体放在隐藏集合。`SHA256SUMS.txt` 记录最终模型与 PNG 校验值。

## 尺寸与实现

选择总长约 1.067 m、柄根至柄尾 210 mm 的等身复原尺度；不是官方公布的工程尺寸。主剑身名义厚 8.5 mm，宽剑根约 50 mm、名义厚 11.5 mm；护手芯体厚 12 mm，周边/肩套另有真实层级。握柄按设定图采用浅色主体、深色交叉接缝与深色柄尾，而不是通用武士刀的深色菱孔。

`model.py` 保存尺寸与参考描线，并在建模后执行明确的握柄材质分配；`lappland_geometry.py` 为从零编写的网格构建与导出代码；`render.py` 生成检查视图。`output/model_manifest.json` 记录实际包围盒、拓扑、单位、源提交与运行编号；`REFERENCE_NOTES.md` 记录全部参考及推断边界；`ITERATIONS.md` 记录真实的失败、下载、对照与返修。

最终单剑 STL 必须通过一个连通分量、零非流形边的检查；BLEND 保留可编辑的相交分件。整剑 STL 不是特定打印机的分段连接套件。

## 安全与推断边界

保留名义 3.2 mm 钝边和 4 mm 圆鼻，不设计锋利真刀。用于轻质、柔性 Cosplay 制作参考；刚性打印仍可能伤人，不构成抗冲击或展会准入认证。护手厚度、背面槽层、肩套叠层、柄尾及固定点的精确尺寸仍属于基于参考图的合理补全。
