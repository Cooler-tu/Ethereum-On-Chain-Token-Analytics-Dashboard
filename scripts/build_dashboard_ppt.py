#!/usr/bin/env python3
"""Generate a 4-slide high-density Dashboard汇报 PowerPoint."""

from __future__ import annotations

from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

BG = RGBColor(0x0F, 0x17, 0x2A)
CARD = RGBColor(0x1E, 0x29, 0x3B)
HEAD = RGBColor(0x11, 0x1A, 0x2E)
BORDER = RGBColor(0x33, 0x41, 0x55)
TEXT = RGBColor(0xF1, 0xF5, 0xF9)
MUTED = RGBColor(0x94, 0xA3, 0xB8)
DIM = RGBColor(0x64, 0x74, 0x8B)
ACCENT = RGBColor(0x3B, 0x82, 0xF6)
ACCENT_L = RGBColor(0x60, 0xA5, 0xFA)
GREEN = RGBColor(0x4A, 0xDE, 0x80)
YELLOW = RGBColor(0xFA, 0xCC, 0x15)
RED = RGBColor(0xF8, 0x71, 0x71)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ROW_ALT = RGBColor(0x16, 0x21, 0x33)
TH = RGBColor(0x17, 0x2A, 0x46)

W = Inches(13.333)
H = Inches(7.5)
FONT = "PingFang SC"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Dashboard汇报.pptx"
TOTAL = 4


def _set_run(run, text, size, color, bold=False, font=FONT):
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", FONT)


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _fill_line(shape, fill, line=BORDER, width_pt=0.6):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(width_pt)


def rect(slide, l, t, w, h, fill, line=None, width_pt=0.6):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    if line is None:
        _fill(sh, fill)
    else:
        _fill_line(sh, fill, line, width_pt)
    sh.shadow.inherit = False
    return sh


def round_rect(slide, l, t, w, h, fill, line=None, width_pt=0.6):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    if line is None:
        _fill(sh, fill)
    else:
        _fill_line(sh, fill, line, width_pt)
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = 0.06
    except Exception:
        pass
    return sh


def tb(slide, l, t, w, h, text, size=12, color=TEXT, bold=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf._txBody.bodyPr.set(
            "anchor",
            {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor],
        )
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    p.space_before = Pt(0)
    run = p.add_run()
    _set_run(run, text, size, color, bold)
    return box


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def footer(slide, page):
    rect(slide, Inches(0), Inches(7.28), W, Inches(0.22), RGBColor(0x0B, 0x12, 0x22))
    tb(slide, Inches(0.32), Inches(7.28), Inches(9.2), Inches(0.22),
       "On-Chain Token Crash  ·  Dashboard 汇报  ·  Ethereum / Uni V1–V4 / Curve / Balancer V2",
       8, DIM, anchor=MSO_ANCHOR.MIDDLE)
    tb(slide, Inches(10.4), Inches(7.28), Inches(2.6), Inches(0.22),
       f"{page}  /  {TOTAL}", 8, DIM, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header(slide, kicker, title, subtitle):
    rect(slide, Inches(0), Inches(0), Inches(0.10), H, ACCENT)
    rect(slide, Inches(0), Inches(0), W, Inches(0.92), HEAD)
    tb(slide, Inches(0.32), Inches(0.08), Inches(12.7), Inches(0.22),
       kicker, 10, ACCENT_L, bold=True)
    tb(slide, Inches(0.32), Inches(0.28), Inches(12.7), Inches(0.32),
       title, 20, TEXT, bold=True)
    tb(slide, Inches(0.32), Inches(0.60), Inches(12.7), Inches(0.26),
       subtitle, 11, MUTED)


def bg(slide):
    rect(slide, Inches(0), Inches(0), W, H, BG)


def add_table(slide, left, top, width, height, headers, rows, col_w=None, font_size=9):
    table_shape = slide.shapes.add_table(1 + len(rows), len(headers), left, top, width, height)
    table = table_shape.table
    if col_w:
        total = sum(col_w)
        for i, w in enumerate(col_w):
            table.columns[i].width = int(width * (w / total))

    def paint(cell, text, fill, color, bold=False, size=font_size):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        # clear default run
        if p.runs:
            run = p.runs[0]
            _set_run(run, text, size, color, bold)
        else:
            run = p.add_run()
            _set_run(run, text, size, color, bold)
        for border in ("lnL", "lnR", "lnT", "lnB"):
            ln = cell._tc.get_or_add_tcPr().find(qn(f"a:{border}"))
            if ln is None:
                continue
            ln.set("w", "6350")
            sf = ln.find(qn("a:solidFill"))
            if sf is not None:
                srgb = sf.find(qn("a:srgbClr"))
                if srgb is not None:
                    srgb.set("val", "334155")

    for i, h in enumerate(headers):
        paint(table.cell(0, i), h, TH, ACCENT_L, bold=True, size=font_size)
    for r, row in enumerate(rows, start=1):
        fill = ROW_ALT if r % 2 == 0 else CARD
        for c, val in enumerate(row):
            paint(table.cell(r, c), str(val), fill, TEXT, bold=(c == 0), size=font_size)
    return table_shape


ASSETS = ROOT / "docs" / "ppt-assets"


def fit_pic(slide, name, left, top, max_w, max_h):
    path = ASSETS / name
    from PIL import Image
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    pw, ph = iw * scale, ih * scale
    return slide.shapes.add_picture(str(path), int(left), int(top), int(pw), int(ph))


def bullets_col(slide, l, t, w, items):
    y = t
    for title, body in items:
        round_rect(slide, Inches(l), Inches(y), Inches(w), Inches(1.18), CARD, BORDER)
        tb(slide, Inches(l + 0.14), Inches(y + 0.08), Inches(w - 0.24), Inches(0.28),
           title, 12, ACCENT_L, bold=True)
        tb(slide, Inches(l + 0.14), Inches(y + 0.38), Inches(w - 0.24), Inches(0.72),
           body, 12, MUTED)
        y += 1.28


def shot_wide(prs, kicker, title, subtitle, img, items, page, note=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, kicker, title, subtitle)
    n = len(items)
    gap = 0.12
    usable = 12.78
    bw = (usable - gap * (n - 1)) / n
    x = 0.28
    for head, body in items:
        round_rect(s, Inches(x), Inches(1.02), Inches(bw), Inches(1.22), CARD, BORDER)
        tb(s, Inches(x + 0.12), Inches(1.10), Inches(bw - 0.22), Inches(0.28),
           head, 12, ACCENT_L, bold=True)
        tb(s, Inches(x + 0.12), Inches(1.40), Inches(bw - 0.22), Inches(0.74),
           body, 11, MUTED)
        x += bw + gap
    round_rect(s, Inches(0.28), Inches(2.36), Inches(12.78), Inches(4.78), CARD, BORDER)
    fit_pic(s, img, Inches(0.42), Inches(2.50), Inches(12.50), Inches(4.50))
    footer(s, page)
    if note:
        notes(s, note)
    return s


def shot_side(prs, kicker, title, subtitle, img, items, page, note=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(s, kicker, title, subtitle)
    bullets_col(s, 0.28, 1.04, 4.15, items)
    round_rect(s, Inches(4.58), Inches(1.04), Inches(8.48), Inches(6.10), CARD, BORDER)
    fit_pic(s, img, Inches(4.72), Inches(1.18), Inches(8.20), Inches(5.82))
    footer(s, page)
    if note:
        notes(s, note)
    return s


def s01_overview(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(
        s, "功能介绍  ·  总览",
        "把一次区块窗口分析变成可解释的静态看板",
        "后面每一页只讲一块功能，并配对应 dashboard 截图。数字是实例画面，汇报讲的是模块本身。",
    )
    mods = [
        ("01  顶部 KPI", "窗口、覆盖率、四张规模卡、启发式风险"),
        ("02  结构三图", "角色分布、已测池集中度、样本内 Top10"),
        ("03  价格 / 量", "Swap 价格与分池成交量，同一时间桶"),
        ("04  持有人表", "EOA/合约、DEX 标签、展开 LP、复制"),
        ("05  已验证池", "池身份、目标代币储备、Not measured"),
        ("06  钱包两表", "余额变动最大 vs 窗口内显著交易"),
        ("07  储备 / LP", "储备时间线、Gross vs Net 流量"),
        ("08  撤资表", "确认动作 vs 能量化金额，缺失不写 0"),
    ]
    positions = [
        (0.28, 1.08), (3.52, 1.08), (6.76, 1.08), (10.00, 1.08),
        (0.28, 2.85), (3.52, 2.85), (6.76, 2.85), (10.00, 2.85),
    ]
    for (x, y), (title, body) in zip(positions, mods):
        round_rect(s, Inches(x), Inches(y), Inches(3.10), Inches(1.58), CARD, BORDER)
        tb(s, Inches(x + 0.14), Inches(y + 0.16), Inches(2.82), Inches(0.50), title, 14, TEXT, bold=True)
        tb(s, Inches(x + 0.14), Inches(y + 0.70), Inches(2.82), Inches(0.72), body, 12, MUTED)
    round_rect(s, Inches(0.28), Inches(4.62), Inches(12.78), Inches(2.48), CARD, BORDER)
    tb(s, Inches(0.48), Inches(4.76), Inches(12.4), Inches(0.28), "另外三块", 13, ACCENT_L, bold=True)
    add_table(
        s, Inches(0.48), Inches(5.12), Inches(12.40), Inches(1.80),
        ["页", "讲什么"],
        [
            ["Pipeline", "Dune / RPC → 12 步加工 → artifacts → Dashboard 只读"],
            ["额外功能", "Print / Save PDF、地址复制、LP/TVL 下钻、本地 Studio、Pages"],
            ["分析能力", "能算哪些层、明确不声称预测 / 普查 / 把缺失写成 0"],
        ],
        col_w=[2.2, 10.2],
        font_size=12,
    )
    footer(s, 1)


def s_pipeline(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(
        s, "Pipeline",
        "数据流向：外部源 → 12 步加工 → artifacts → Dashboard 只读",
        "python3 -m src.cli analyze <TOKEN> --from-block N --to-block M    ·    Dune-first，失败回退 RPC",
    )
    flow = [
        ("左：源", "Dune SQL\nEthereum RPC"),
        ("中：加工", "analyze 1–12\n过滤 / 合并 / 打分"),
        ("右：产物", "JSON / Parquet\nreport.md"),
        ("交付面", "dashboard.html\nStudio / Pages"),
    ]
    x = 0.28
    for i, (title, body) in enumerate(flow):
        round_rect(s, Inches(x), Inches(1.00), Inches(2.70), Inches(0.88), CARD, BORDER)
        tb(s, Inches(x + 0.12), Inches(1.06), Inches(2.46), Inches(0.22), title, 12, ACCENT_L, bold=True)
        tb(s, Inches(x + 0.12), Inches(1.30), Inches(2.46), Inches(0.50), body, 12, TEXT)
        if i < 3:
            tb(s, Inches(x + 2.62), Inches(1.24), Inches(0.28), Inches(0.36), "→", 16, ACCENT, align=PP_ALIGN.CENTER)
        x += 3.22
    steps = [
        ("1 Profile", "RPC meta", "token_profile"),
        ("2 Discover", "Dune pools ∥ V4", "池候选"),
        ("3 Verify", "RPC 校验配对", "verified_pools"),
        ("4 Holdings", "balances + balanceOf", "holdings"),
        ("5 Positions", "V3/V4 tick 份额", "portfolios"),
        ("6 Index", "Swap / LP / Transfer", "事件表"),
        ("7 Labels", "EOA / 角色 / DEX", "address_dex"),
        ("8 Metrics", "集中度 · 流量 · P99", "metrics"),
        ("9 Timeline", "按窗口自动分桶", "timeline"),
        ("10 Risk", "启发式 + confidence", "risk"),
        ("11 Report", "Markdown", "report.md"),
        ("12 Dashboard", "读产物，不回源", "dashboard.html"),
    ]
    x0, y0 = 0.28, 2.02
    bw, bh = 2.05, 1.05
    for i, (name, body, art) in enumerate(steps):
        r, c = divmod(i, 6)
        x = Inches(x0 + c * (bw + 0.10))
        y = Inches(y0 + r * (bh + 0.08))
        round_rect(s, x, y, Inches(bw), Inches(bh), CARD, BORDER)
        rect(s, x, y, Inches(0.08), Inches(bh), ACCENT)
        tb(s, x + Inches(0.16), y + Inches(0.06), Inches(1.80), Inches(0.26), name, 11, ACCENT_L, bold=True)
        tb(s, x + Inches(0.16), y + Inches(0.34), Inches(1.80), Inches(0.32), body, 11, TEXT)
        tb(s, x + Inches(0.16), y + Inches(0.70), Inches(1.80), Inches(0.26), art, 10, DIM)
    add_table(
        s, Inches(0.28), Inches(4.30), Inches(12.78), Inches(2.80),
        ["流", "从哪拿", "变成什么", "看板读哪一块"],
        [
            ["池", "dex.trades + V4 Swap/Init；RPC 校验", "已验证 Uni V1–V4 / Curve / Balancer 池", "池表、储备饼图、集中度"],
            ["成交", "Swap 事件只拉一次", "本地分桶 → 价格、分池成交量（不再重查 dex.trades）", "价格图、成交量图"],
            ["持仓", "Dune balances；失败则 RPC balanceOf", "start / end / peak / 净变动 + 覆盖率", "KPI、Holders、Movers"],
            ["LP", "Mint/Burn、V4 ModifyLiquidity", "仓位；Gross/Net；金额三态", "LP 下钻、Flow、撤资表"],
            ["储备", "历史 RPC balanceOf 或事件重建", "snapshot 或 reconstructed 时间线", "储备图及点击下钻"],
        ],
        col_w=[1.1, 3.6, 4.3, 3.8],
        font_size=10,
    )
    footer(s, 12)
    notes(s, "只讲流向。截图里的覆盖率数字是实例，不要当成产品承诺。")


def s_extras(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(
        s, "额外功能",
        "打印/PDF、本地 Studio，以及同一套看板上的操作层",
        "不改计算公式，只改变查看、导出、复跑和发布方式",
    )
    round_rect(s, Inches(0.28), Inches(1.02), Inches(7.70), Inches(2.55), CARD, BORDER)
    tb(s, Inches(0.46), Inches(1.12), Inches(7.4), Inches(0.28), "Print / Save PDF", 14, GREEN, bold=True)
    tb(s, Inches(0.46), Inches(1.42), Inches(7.4), Inches(0.70),
       "导航栏按钮 → 切换 A4 浅色打印样式 → Chart.js 按纸宽 resize → 系统打印框（可存 PDF）→ 打印后恢复深色交互尺寸。表格取消裁切，表头每页重复。",
       12, MUTED)
    fit_pic(s, "00-nav.png", Inches(0.46), Inches(2.18), Inches(7.34), Inches(1.20))

    round_rect(s, Inches(8.14), Inches(1.02), Inches(4.92), Inches(2.55), CARD, BORDER)
    tb(s, Inches(8.32), Inches(1.12), Inches(4.56), Inches(0.28), "屏幕 vs 纸面", 13, ACCENT_L, bold=True)
    tb(s, Inches(8.32), Inches(1.46), Inches(4.56), Inches(1.95),
       "屏幕：深色、多列、表可滚动。\n打印：白底 A4、时间序列改单列全宽、饼/环图居中正方形。\n隐藏：toast、tooltip、Etherscan 图标、下钻关闭按钮。",
       12, MUTED)

    round_rect(s, Inches(0.28), Inches(3.70), Inches(7.70), Inches(3.40), CARD, BORDER)
    tb(s, Inches(0.46), Inches(3.80), Inches(7.4), Inches(0.28),
       "Studio  ·  python3 -m src.cli studio", 14, ACCENT_L, bold=True)
    fit_pic(s, "12-studio.png", Inches(0.46), Inches(4.12), Inches(7.34), Inches(2.82))

    extras = [
        ("地址", "悬停全文、点击复制、主网地址链到 Etherscan；V4 poolId 只复制"),
        ("下钻", "持有人行展开 LP 仓位；点击储备时点看分池明细"),
        ("复跑", "dashboard --refresh-wallet-activity 用本地 swaps 重算分位数，不打 Dune"),
        ("Pages", "静态案例站；CI 通过后才部署；访客不能提交任意 token"),
    ]
    y = 3.70
    for title, body in extras:
        round_rect(s, Inches(8.14), Inches(y), Inches(4.92), Inches(0.80), CARD, BORDER)
        tb(s, Inches(8.32), Inches(y + 0.08), Inches(4.56), Inches(0.24), title, 12, ACCENT_L, bold=True)
        tb(s, Inches(8.32), Inches(y + 0.32), Inches(4.56), Inches(0.42), body, 11, MUTED)
        y += 0.85
    footer(s, 13)
    notes(s, "演示：先点 Print / Save PDF，再打开 studio 表单。")


def s_analysis(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    header(
        s, "数据分析能力",
        "能算什么、按什么口径展示——不是某次 token 的结果页",
        "输入任意 ERC-20 + 区块窗口；输出结构、流量、筛查信号，并标明覆盖与不可得",
    )
    add_table(
        s, Inches(0.28), Inches(1.02), Inches(12.78), Inches(3.70),
        ["层", "做什么", "明确不做"],
        [
            ["持仓", "期初/期末/峰值/净变动；区分 EOA、合约、池托管", "不当作全市场持有人普查"],
            ["池与集中度", "验证 DEX 池；份额只在已测目标代币储备内比较", "未测不写成 0%；V4 共享托管不装成逐池余额"],
            ["价格 / 量", "已索引 Swap 推导价格与分池成交量，同窗口分桶", "不同报价单位不硬折成一张不可比美元图"],
            ["LP 流量", "按桶汇总添加/移除；净流 = 添加 − 移除", "累计撤资 ≠ 永久外部退出"],
            ["撤资", "能量化才算 USD/占比；否则保留负 ΔL 并标缺失", "缺失金额不改写成 0"],
            ["钱包", "窗口内分位数标记 Trade / Mover / Volume / Activity", "不用跨 token 的全局固定阈值"],
            ["风险", "可解释加权 + 迁移下调 + 置信度 → LOW/MEDIUM/HIGH", "不是崩盘概率，也不是已校准预测模型"],
        ],
        col_w=[1.7, 5.9, 5.2],
        font_size=11,
    )
    add_table(
        s, Inches(0.28), Inches(4.86), Inches(12.78), Inches(2.24),
        ["边界", "说明"],
        [
            ["本地 vs 线上", "Studio / CLI 可跑任意 token；GitHub Pages 只展示预生成静态案例"],
            ["窗口责任", "图、表、DEX 标签只对本次 from–to 区块负责，不是长期身份"],
            ["三种数分开写", "真实测到的值（含真实 0） / 部分覆盖下的排序与占比 / 数据不可得"],
            ["范围", "Ethereum · Uniswap V1–V4 · Curve · Balancer V2。多链、实时、钱包 unwrap 不在本产品面"],
        ],
        col_w=[2.2, 10.58],
        font_size=11,
    )
    footer(s, 14)


def build():
    global TOTAL
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    builders = []

    def add(fn):
        builders.append(fn)

    add(s01_overview)
    add(lambda p: shot_wide(
        p, "功能模块",
        "顶部：窗口元数据 + 四张 KPI",
        "先交代这次分析覆盖了什么，再给规模和风险档。",
        "01-kpis.png",
        [
            ("窗口", "区块闭区间、余额来源、覆盖率。所有图只对这个窗口负责。"),
            ("四个大数", "Transfer 地址、正余额样本、已验证池、启发式风险。"),
            ("不要误读", "Transfer 地址不是持有人数；风险徽章是筛查，不是崩盘概率。"),
        ],
        2,
    ))
    add(lambda p: shot_wide(
        p, "功能模块",
        "结构三图：角色、池集中度、样本内 Top 持有人",
        "回答「钱在谁手里、流动性在哪几个池」，但都受查询覆盖约束。",
        "02-structure.png",
        [
            ("角色", "已覆盖且余额为正的行：池/托管 vs 非池。EOA 是字节码表面标签。"),
            ("集中度", "份额分母 = 已测池，不是全部 verified pools。"),
            ("Top10", "查询样本内期末余额排序，不是全量 holder 榜。条可复制地址。"),
        ],
        3,
    ))
    add(lambda p: shot_wide(
        p, "功能模块",
        "价格与分池成交量，共用同一时间桶",
        "图表主路径复用已索引 Swap，不再回源重查 dex.trades。",
        "03-market.png",
        [
            ("价格", "Swap 隐含价，保留真实报价单位（USD / WETH per token）。"),
            ("成交量", "目标代币单位、按池堆叠。月窗按日、周/日窗按小时。"),
            ("不要误读", "不同报价不硬折成一张不可比的总美元图。"),
        ],
        4,
    ))
    add(lambda p: shot_side(
        p, "功能模块",
        "持有人表：身份、DEX 证据、LP 下钻",
        "表是交互核心。截图为实例窗口，讲的是列和操作。",
        "04-holders.png",
        [
            ("看什么", "期末余额排序；Start / Δ / Peak；Tx 次数。"),
            ("怎么点", "悬停看全文，点击复制；合法地址开 Etherscan；行展开只显示 LP 仓位。"),
            ("不要误读", "DEX 列是本窗口证据，不是所有权。余额变动不是买卖。"),
            ("覆盖", "Top 20 只在已查询、非池、正余额样本内。"),
        ],
        5,
    ))
    add(lambda p: shot_side(
        p, "功能模块",
        "已验证池 + 目标代币储备分布",
        "先看池是谁，再看测到了多少；测不到就写 Not measured。",
        "05-pools.png",
        [
            ("看什么", "协议/版本、交易对、观测储备、成交量份额。"),
            ("饼图", "已识别托管地址上的目标代币余额分布。"),
            ("V4 注意", "可能是共享 PoolManager，一个扇区对应多个 poolId。"),
            ("不要误读", "未测 ≠ 0%。储备是目标代币数量，不是双边 USD TVL。"),
        ],
        6,
    ))
    add(lambda p: shot_side(
        p, "功能模块",
        "Largest Covered Balance Changes：余额变动，不一定是交易",
        "按期末 − 期初排序。正变动不是自动买入，负变动不是自动卖出。",
        "06-movers.png",
        [
            ("排序键", "窗口内余额净变动，且排除池地址。"),
            ("Swap 列", "Bought / Sold / Swap Net 只是索引到的成交上下文。"),
            ("来源", "转账、托管迁移、合约操作都会改余额。"),
            ("覆盖", "只在余额查询已覆盖的地址中排序。"),
        ],
        7,
    ))
    add(lambda p: shot_side(
        p, "功能模块",
        "Notable Wallets：窗口内分位数筛出的显著交易地址",
        "四个标签互相独立。默认不用跨 token 的固定金额阈值。",
        "07-notable.png",
        [
            ("Movers", "按期末−期初余额排序。正变动不是自动买入。"),
            ("Notable", "Trade / Mover / Volume / Activity 四个独立标签。"),
            ("阈值", "默认用当前窗口内分位数，不用全局固定金额。"),
            ("Swap 列", "Bought/Sold 只是索引到的成交上下文。"),
        ],
        8,
    ))
    add(lambda p: shot_wide(
        p, "功能模块",
        "储备时间线：snapshot 还是事件重建，页面会打徽章",
        "点击时点可展开分池明细，时间戳与成交量桶对齐。",
        "08-tvl.png",
        [
            ("snapshot", "历史 RPC balanceOf，目标代币单位。"),
            ("reconstructed", "由事件累加的代理，不能叫精确链上余额。"),
            ("不要误读", "目标代币储备 ≠ 双边 USD TVL。"),
        ],
        9,
    ))
    add(lambda p: shot_wide(
        p, "功能模块",
        "LP Event Flow：把活动量和净进出拆开",
        "绿柱添加、红柱移除、蓝线净流。同一笔资金撤出再注入会进 Gross。",
        "09-lpflow.png",
        [
            ("Gross", "衡量 LP 活动，可能重复计算同一资本。"),
            ("Net", "添加 − 移除，更接近窗口内净进出。"),
            ("还不是储备", "Swap 和直接转账也会改池余额。"),
        ],
        10,
    ))
    add(lambda p: shot_side(
        p, "功能模块",
        "撤资表：确认发生了 removal，不等于能量化金额",
        "负 liquidity delta 证明动作；USD / 占比还需要 token amount。",
        "10-withdraw.png",
        [
            ("已测", "token 数量已知，可算 USD 和参考占比。"),
            ("仅 ΔL", "确认撤池，页面写 Token amount not returned。"),
            ("未映射", "无法可靠对到目标代币一侧。"),
            ("禁止", "缺失绝不显示成 0；测到的 0 仍是 0。"),
        ],
        11,
    ))
    add(s_pipeline)
    add(s_extras)
    add(s_analysis)

    TOTAL = len(builders)
    # footer uses TOTAL at call time — set before running
    globals()["TOTAL"] = TOTAL
    for fn in builders:
        fn(prs)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT))
    print(f"Wrote {OUT}  ({TOTAL} slides)")


if __name__ == "__main__":
    build()
