#!/usr/bin/env python3
"""Generate a PDF description of BMW E36 318tds (1.8 TDS)."""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Fonts with Cyrillic support
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerifBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))

# BMW-inspired palette (not purple/cream clichés)
BMW_BLUE = HexColor("#1C69D4")
BMW_DARK = HexColor("#0B1D2E")
BMW_STEEL = HexColor("#2C3E50")
BMW_SILVER = HexColor("#E8EEF2")
BMW_ACCENT = HexColor("#C4A35A")
LIGHT_BG = HexColor("#F5F7FA")
ROW_ALT = HexColor("#EEF3F8")
TEXT = HexColor("#1A2332")
MUTED = HexColor("#5A6A7A")


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="HeroBrand",
            fontName="DejaVuSerifBold",
            fontSize=28,
            leading=34,
            textColor=white,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="HeroSub",
            fontName="DejaVu",
            fontSize=12,
            leading=16,
            textColor=HexColor("#B8C9D9"),
            alignment=TA_CENTER,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="HeroTag",
            fontName="DejaVuBold",
            fontSize=11,
            leading=14,
            textColor=BMW_ACCENT,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            fontName="DejaVuSerifBold",
            fontSize=14,
            leading=18,
            textColor=BMW_DARK,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyRu",
            fontName="DejaVu",
            fontSize=10,
            leading=15,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLeft",
            fontName="DejaVu",
            fontSize=10,
            leading=14,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SpecLabel",
            fontName="DejaVu",
            fontSize=9,
            leading=12,
            textColor=MUTED,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SpecValue",
            fontName="DejaVuBold",
            fontSize=9,
            leading=12,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Footer",
            fontName="DejaVu",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletRu",
            fontName="DejaVu",
            fontSize=10,
            leading=14,
            textColor=TEXT,
            leftIndent=12,
            spaceAfter=3,
        )
    )
    return styles


def draw_header(canvas, doc):
    canvas.saveState()
    width, height = A4

    # Top hero band
    canvas.setFillColor(BMW_DARK)
    canvas.rect(0, height - 72 * mm, width, 72 * mm, fill=1, stroke=0)

    # Diagonal accent stripe
    canvas.setFillColor(BMW_BLUE)
    canvas.setFillAlpha(0.18)
    path = canvas.beginPath()
    path.moveTo(0, height - 20 * mm)
    path.lineTo(width, height - 55 * mm)
    path.lineTo(width, height - 72 * mm)
    path.lineTo(0, height - 72 * mm)
    path.close()
    canvas.drawPath(path, fill=1, stroke=0)
    canvas.setFillAlpha(1)

    # Gold line under hero
    canvas.setStrokeColor(BMW_ACCENT)
    canvas.setLineWidth(2.5)
    canvas.line(0, height - 72 * mm, width, height - 72 * mm)

    # Side trim
    canvas.setFillColor(BMW_BLUE)
    canvas.rect(0, 0, 4 * mm, height, fill=1, stroke=0)

    # Page footer
    canvas.setFillColor(LIGHT_BG)
    canvas.rect(0, 0, width, 14 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(BMW_SILVER)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("DejaVu", 8)
    canvas.drawCentredString(
        width / 2,
        6 * mm,
        f"BMW E36 318tds  ·  стр. {doc.page}",
    )
    canvas.restoreState()


def draw_first_page(canvas, doc):
    draw_header(canvas, doc)
    canvas.saveState()
    width, height = A4

    # Brand block inside hero
    canvas.setFillColor(white)
    canvas.setFont("DejaVuSerifBold", 36)
    canvas.drawCentredString(width / 2, height - 28 * mm, "BMW")

    canvas.setFillColor(BMW_ACCENT)
    canvas.setFont("DejaVuBold", 11)
    canvas.drawCentredString(width / 2, height - 36 * mm, "3 SERIES  ·  E36")

    canvas.setFillColor(white)
    canvas.setFont("DejaVuSerifBold", 22)
    canvas.drawCentredString(width / 2, height - 48 * mm, "318tds  /  1.8 TDS")

    canvas.setFillColor(HexColor("#A8BCCE"))
    canvas.setFont("DejaVu", 10)
    canvas.drawCentredString(
        width / 2,
        height - 58 * mm,
        "Турбодизель  ·  1994–2000  ·  Задний привод",
    )
    canvas.restoreState()


def spec_table(styles, rows):
    data = []
    for label, value in rows:
        data.append(
            [
                Paragraph(label, styles["SpecLabel"]),
                Paragraph(value, styles["SpecValue"]),
            ]
        )

    table = Table(data, colWidths=[72 * mm, 98 * mm])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BOX", (0, 0), (-1, -1), 0.5, BMW_SILVER),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, BMW_SILVER),
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#E4EBF2")),
    ]
    for i in range(1, len(rows), 2):
        style_cmds.append(("BACKGROUND", (1, i), (1, i), ROW_ALT))

    table.setStyle(TableStyle(style_cmds))
    return table


def build_pdf(output_path: Path):
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=78 * mm,
        bottomMargin=20 * mm,
        title="BMW E36 318tds (1.8 TDS) — описание",
        author="BMW E36 Reference",
        subject="Техническое описание BMW 318tds E36",
    )

    story = []

    story.append(Paragraph("Обзор модели", styles["Section"]))
    story.append(
        Paragraph(
            "BMW 318tds (часто обозначается как <b>E36 1.8 TDS</b>) — "
            "четырёхцилиндровая турбодизельная версия третьего поколения "
            "BMW 3 Series. Модель выпускалась с <b>1994 по 2000</b> год "
            "и стала первым «четвёртым» дизелем в линейке BMW. "
            "Официальный объём двигателя — <b>1,665 см³ (~1,7 л)</b>; "
            "в обиходе и коммерческих объявлениях модель нередко называют "
            "«1.8 TDS» из‑за индекса 318.",
            styles["BodyRu"],
        )
    )
    story.append(
        Paragraph(
            "Автомобиль построен на классической компоновке BMW: "
            "переднее расположение двигателя и <b>задний привод</b>. "
            "Дизель предлагался в кузовах седан, Touring (универсал) "
            "и Compact (трёхдверный хэтчбек).",
            styles["BodyRu"],
        )
    )

    story.append(Paragraph("Двигатель M41D17", styles["Section"]))
    story.append(
        Paragraph(
            "Силовой агрегат <b>M41D17</b> — рядный четырёхцилиндровый "
            "турбодизель с предкамерным впрыском (indirect injection). "
            "Конструкция во многом унаследована от шестицилиндрового "
            "M51: около <b>86%</b> деталей совместимы. Двигатель оснащён "
            "турбонаддувом с интеркулером, алюминиевой ГБЦ (8 клапанов, SOHC), "
            "чугунным блоком и цепным приводом ГРМ.",
            styles["BodyRu"],
        )
    )

    engine_specs = [
        ("Код двигателя", "M41D17"),
        ("Конфигурация", "R4, SOHC, 8 клапанов"),
        ("Рабочий объём", "1 665 см³ (1,7 л)"),
        ("Диаметр × ход поршня", "80,0 × 82,8 мм"),
        ("Степень сжатия", "22,0 : 1"),
        ("Топливная система", "Предкамерный впрыск"),
        ("Наддув", "Турбина + интеркулер"),
        ("Мощность", "66 кВт / 90 л.с. при 4 400 об/мин"),
        ("Крутящий момент", "190 Н·м при ~2 000 об/мин"),
        ("Ограничитель оборотов", "≈ 4 800 об/мин"),
        ("Нормы выбросов", "EURO 1 / EURO 2"),
        ("Ресурс (оценка)", "до ~300 000 км при уходе"),
    ]
    story.append(spec_table(styles, engine_specs))

    story.append(Paragraph("Динамика и расход", styles["Section"]))
    story.append(
        Paragraph(
            "Для седана 318tds заявлены типичные показатели экономичного "
            "туристического дизеля 90‑х: спокойный разгон при уверенной "
            "тяге «внизу» и невысокий расход на трассе.",
            styles["BodyRu"],
        )
    )
    perf_specs = [
        ("Максимальная скорость", "≈ 180–183 км/ч"),
        ("Разгон 0–100 км/ч", "≈ 14–15 с (седан)"),
        ("Расход (город)", "≈ 8,8 л/100 км"),
        ("Расход (трасса)", "≈ 5,2 л/100 км"),
        ("Расход (смешанный)", "≈ 6,5 л/100 км"),
        ("Коробка передач", "5‑ступ. МКПП (авт. на части рынков)"),
        ("Привод", "Задний (RWD)"),
    ]
    story.append(spec_table(styles, perf_specs))

    story.append(Paragraph("Кузова и габариты (седан E36)", styles["Section"]))
    body_specs = [
        ("Годы выпуска 318tds", "1994–2000"),
        ("Доступные кузова", "Седан, Touring, Compact"),
        ("Колёсная база", "2 700 мм"),
        ("Длина × ширина", "≈ 4 433 × 1 710 мм"),
        ("Высота", "≈ 1 366–1 390 мм"),
        ("Снаряжённая масса (седан)", "≈ 1 290–1 320 кг"),
        ("Предшественник / преемник", "E30 → E36 → E46"),
    ]
    story.append(spec_table(styles, body_specs))

    story.append(Paragraph("Особенности эксплуатации", styles["Section"]))
    bullets = [
        "• Цепной привод ГРМ — меньше рисков, чем у ремня, но важны натяжители и состояние цепи на больших пробегах.",
        "• Предкамерный дизель чувствителен к качеству топлива; свечи накаливания и ТНВД требуют регулярного внимания.",
        "• Рекомендуемое масло: вязкость класса вроде 5W‑40, объём заправки около 5,0 л.",
        "• Турбина с интеркулером даёт хороший запас тяги уже с ~2 000 об/мин — удобно для города и трассы.",
        "• Типичные слабые места кузова E36: пороги, арки, днище, швы багажника — особенно на рынках с солёными зимами.",
        "• Электрика и ОЖ‑прокладки (в т.ч. связанные с возрастом) стоит проверять при покупке «живого» экземпляра.",
    ]
    for b in bullets:
        story.append(Paragraph(b, styles["BulletRu"]))

    story.append(Paragraph("Место в линейке дизелей E36", styles["Section"]))
    story.append(
        Paragraph(
            "В семействе E36 дизели были представлены тремя основными "
            "вариантами: <b>318tds</b> (M41, 90 л.с.), <b>325td</b> "
            "(M51 без интеркулера, 115 л.с.) и <b>325tds</b> "
            "(M51 с интеркулером, 143 л.с.). 318tds позиционировался "
            "как экономичный вход в дизельную «тройку»: проще и легче "
            "шестицилиндровых TD, при этом сохраняет фирменный "
            "характер шасси и компоновку заднего привода.",
            styles["BodyRu"],
        )
    )

    story.append(Spacer(1, 8 * mm))
    story.append(
        HRFlowable(width="100%", thickness=0.8, color=BMW_ACCENT, spaceBefore=4, spaceAfter=8)
    )
    story.append(
        Paragraph(
            "Справка подготовлена по открытым данным о модели BMW 318tds (E36) "
            "и двигателе M41D17. Индекс «1.8 TDS» в названии документа "
            "соответствует распространённому бытовому обозначению; "
            "заводской объём — 1,7 л.",
            styles["Footer"],
        )
    )

    doc.build(story, onFirstPage=draw_first_page, onLaterPages=draw_header)
    return output_path


if __name__ == "__main__":
    out_dir = Path("/workspace/artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "BMW_E36_318tds_1.8_TDS.pdf"
    # Also copy to Cursor artifacts for walkthrough
    artifact = Path("/opt/cursor/artifacts")
    artifact.mkdir(parents=True, exist_ok=True)

    path = build_pdf(out)
    copy = artifact / path.name
    copy.write_bytes(path.read_bytes())
    print(f"Created: {path}")
    print(f"Copied:  {copy}")
    print(f"Size:    {path.stat().st_size} bytes")
