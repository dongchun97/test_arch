清式建筑建模命名规范模板

### 清式建筑建模命名规范模板（原型阶段）

| 构件类型 | 命名前缀 | 命名结构模板 | 示例 | 说明 |
|----------|-----------|---------------|------|------|
| 柱类 Column | COL | COL_<序号>_H<高度>_D<直径>_STYLE_<体系> | COL_001_H3.20_D0.30_STYLE_qing_small | 清式或宫殿式柱（含金柱、檐柱等） |
| 梁类 Beam | BEAM | BEAM_<序号>_L<长度>_TYPE_<类型>_STYLE_<体系> | BEAM_002_L4.50_TYPE_3jia_STYLE_qing | 如七架梁、五架梁、三架梁等 |
| 枋类 Fang | FANG | FANG_<序号>_POS_<位置>_L<长度> | FANG_004_POS_yanfang_L2.80 | 用于下架檐枋、金枋等 |
| 檩类 Purlin | PURL | PURL_<序号>_TYPE_<种类>_L<长度> | PURL_002_TYPE_jin_L5.20 | 檐檩、金檩、脊檩等 |
| 屋顶 Roof（卷棚/歇山/攒尖） | ROOF | ROOF_<序号>_TYPE_<形式>_W<面宽>_D<进深>_STYLE_<体系> | ROOF_001_TYPE_xieshan_W9.00_D6.00_STYLE_qing | 主要屋顶系统 |
| 翼角 Wing Corner | WING | WING_<序号>_ANG<角度>_STYLE_<体系> | WING_001_ANG35_STYLE_qing | 角梁、翘飞椽等系统 |
| 斗拱 Dougong | DOUG | DOUG_<序号>_TYPE_<科制>_C<踩数>_STYLE_<体系> | DOUG_003_TYPE_ping_C5_STYLE_qing | 平身科、柱头科、角科 |
| 斗口/模数系 Modulus | MODU | MODU_<序号>_DOUKOU_<斗口尺寸> | MODU_001_DOUKOU_0.35 | 建筑整体比例参数 |
| 基础 Platform / Base | BASE | BASE_<序号>_TYPE_<类型>_H<高度> | BASE_001_TYPE_taiji_H0.60 | 台基、须弥座等 |
| 门窗 Decoration | DECO | DECO_<序号>_TYPE_<种类>_STYLE_<样式> | DECO_005_TYPE_door_STYLE_chinese | 板门、槛窗、槛框等 |
| 雕刻/饰件 Carving | CARV | CARV_<序号>_THEME_<主题> | CARV_002_THEME_dragon | 花罩、碧纱厨、楣子等 |
| 整体建筑 Architecture | ARCH | ARCH_<名称>_TYPE_<建筑类型>_STYLE_<体系> | ARCH_mingpalace_TYPE_palace_STYLE_qing | 整体建筑实例 |

### 一、命名编码规则说明

| 元素 | 格式 | 说明 |
|------|------|------|
| <序号> | 三位数字 (001, 002…) | 用于同类构件编号 |
| <参数> | 小数点两位（H3.20） | 几何参数（高、宽、径等） |
| <类型> | 英文关键字（ping, xieshan, wudian） | 构件类型或形式 |
| <体系> | 建筑风格（qing, song, ming） | 用于区分体系规则 |
| <位置> | 语义标签（yanfang, jinfang） | 用于定位构件位置 |
| <主题> | 可读文本（dragon, cloud, lotus） | 雕饰或题材标识 |

### 二、命名解析策略

import re

pattern = r"COL_(\d+)_H([0-9.]+)_D([0-9.]+)_STYLE_(\w+)"
name = "COL_001_H3.20_D0.30_STYLE_qing_small"

match = re.match(pattern, name)
if match:
    index, height, diameter, style = match.groups()
    data = {
        "type": "column",
        "index": int(index),
        "params": {
            "height": float(height),
            "diameter": float(diameter),
            "style": style
        }
    }
    print(data)

输出：

{
  "type": "column",
  "index": 1,
  "params": {"height": 3.2, "diameter": 0.3, "style": "qing_small"}
}

### 三、命名规范的扩展思路

阶段	目标	扩展方式
原型期	区分类型和主要参数	纯字符串命名
模块期	支持程序筛选与统计	统一前缀与关键参数
语义期	加入元数据同步	命名 + obj[“meta”]
BIM期	命名与 IFC 对应	命名规则映射 IFC 属性集

### 四、命名与元数据一体化（过渡策略）

当前阶段	存储方式	未来升级
现在	obj.name = "COL_001_H3.20_D0.30_STYLE_qing_small"	快速识别
下阶段	obj["meta"] = {...}	元数据结构化
未来	ifc_attribute_map(obj)	IFC / BIM 输出

### 五、下一步推荐

可以设计一个 统一的命名解析器类（NameParser），自动识别柱、梁、屋顶等构件命名并返回对应参数字典，作为命名规范 → 元数据的过渡桥梁。