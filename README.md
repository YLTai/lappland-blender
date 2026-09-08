# 原版五星拉普兰德双剑 · 参数化 Cosplay 成品

范围只含原版 / E2 / 幼狼的牙齿，不含典雅噩兆或荒芜拉普兰德。当前几何从部件规则生成，不再把透视图的像素边缘固化为三维曲线。

## 护手的结构约束

共同外半径 **175 mm**、内半径 **150 mm**，每片外弧严格为 **180°**；直径梁宽 **24 mm**，与剑轴成 **30°**。两片真实护手网格经刚体变换可配成外径 **350 mm** 的圆。每片的梁只占自己的半平面，配对时梁不会互相占用相同体积。

环和梁不是两件带共面重叠面的模型：`continuous_guard.py` 由外 D 边界与内孔一次生成连续封闭框体，内外凸缘同样是嵌套的连续 D 形实体，避免弧/梁接头处的黑块和深度冲突。肩套、凹槽与芯体保持真实的厚度层次；上肩板不越过公共外圆。

## 生成与交付内容

现有 Blender Build Actions 生成 **lappland-build**。Blender 4.2.1 本地命令：

```sh
blender -b --python model.py
blender -b --python render.py
```

`output/lappland_original_pair.blend` 保留可编辑部件和两个场景：**Original Lappland | twin props**、**Guard closure | actual mesh pair | diameter 350 mm**。在 Blender 的场景选择器中切换即可查看护手配圆。配圆场景只验证护手框，未设计两把完整剑的机械锁合。

另含带材质双剑 `.glb`、A/B 两个单剑 `.stl`、双剑 `.stl`、`lappland_guard_circle_proof.glb`、参数、几何检查与 SHA-256 清单。STL 数值单位为毫米；Blender/GLB 坐标为米。STL 不保存颜色。

**17 张 PNG** 覆盖双剑正面、单剑正反面/侧面/顶面、45°、护手各面、刀尖、握柄、无材质轮廓，以及配圆正面/45°/端部接缝。所有检查视图均由实际模型渲染；配圆不是替换成示意圆环。

## 尺寸与安全

总长约 **1082 mm**（含柄尾挂环），柄根至端帽名义 **210 mm**。主剑身宽 **31.5 mm**、最大名义厚 **8.5 mm**；宽剑根约 **50 mm**、名义厚 **11.5 mm**。护手芯体厚 **12 mm**，周边层总厚 **17.2 mm**，上肩层总厚 **24.4 mm**。实际 STL 包围盒与拓扑记录在 `model_manifest.json`。

保持 **3.2 mm 名义钝边、4 mm 名义圆鼻**。仅用于轻质、柔性 Cosplay 道具外形参考，不开锋，不构成抗冲击或展会准入认证。整剑 STL 不是特定打印机的分段连接套件。

## 来源和复现

`model.py` 保存参数；`continuous_guard.py` 实现闭合 D 形框体；`semantic_geometry.py` 实现参数化剑身与真实网格配圆验证；`lappland_geometry.py` 提供本次从零编写的网格/导出基础工具；`render.py` 生成视图。源码随 Artifact 提供。

官方图没有工程尺寸，厚度、背面槽层、连接件精确位置等仍是合理推断。用户提供的 MakerWorld 页面访问返回 403，因此未导入、修改或重新发布该作者网格；访问记录随 Artifact 提供。参考列表见 REFERENCE_NOTES.md，实际迭代见 ITERATIONS.md。
