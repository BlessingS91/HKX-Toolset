import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
from HKX_Tools import (
    duplicate_attacks,
    rename_attack_to_power,
    rename_power_to_attack,
)
from Animation_Tools import (
    merge_animations,
    reverse_animation,
    scale_animation,
)
import os

# =========================================================
# LANGUAGE / LOCALIZATION
# =========================================================

DEFAULT_LANGUAGE = "English"
LANGUAGE = DEFAULT_LANGUAGE

DEFAULT_APPEARANCE = "Dark"
APPEARANCE = DEFAULT_APPEARANCE

appearance_cache = "appearance.txt"

language_cache = "language.txt"

translations = {
    "English": {
        "title": "HKX Animation Toolkit",
        "home_title": "HKX Animation Toolkit",
        "home_subtitle": "Select a category from the sidebar",
        "ready": "Ready",
        "settings": "Settings",
        "language": "Language",
        "language_help": "Choose the UI language",
        "nav_home": "Home",
        "nav_merge": "Animation Merge",
        "nav_reverse": "Reverse Animation",
        "nav_scale": "Stretch / Compress",
        "nav_file": "HKX File Tools",
        "nav_settings": "Settings",
        "file_tools_title": "HKX File Tools",
        "browse_hkx": "Browse HKX",
        "duplicate_desc": "Duplicate the selected attack animation into all 10 available attack slots",
        "duplicate_btn": "Duplicate Attacks",
        "attack_desc": "Rename all Attack animation files into PowerAttack files",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "Rename all PowerAttack animation files back into Attack files",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "Animation Merge Tools",
        "merge_select_a": "Select Animation json A",
        "merge_select_b": "Select Animation json B",
        "merge_a_start": "Animation A Start Frame Removal",
        "merge_a_end": "Animation A Ending Frame Removal",
        "merge_b_start": "Animation B Start Frame Removal",
        "merge_b_end": "Animation B Ending Frame Removal",
        "select_output": "Select Output",
        "merge_btn": "MERGE ANIMATIONS",
        "reverse_tools_title": "Reverse Animation Tools",
        "reverse_help": "Select a single JSON animation and save a reversed copy.",
        "reverse_select": "Select Animation",
        "reverse_output_label": "Reversed Output Filename",
        "reverse_output_btn": "Select Output",
        "reverse_btn": "REVERSE ANIMATION",
        "scale_tools_title": "Stretch / Compress Animation",
        "scale_help": "Adjust animation speed by scaling frame timing.",
        "scale_select": "Select Animation",
        "scale_ratio_label": "Scale Ratio (0.5 = faster, 2.0 = slower)",
        "scale_output_btn": "Select Output",
        "scale_btn": "SCALE ANIMATION",
        "scale_output_label": "Scaled Output Filename",
        "select_sidebar": "Select a category from the sidebar",
        "select_animation_a": "Select Animation A",
        "select_animation_b": "Select Animation B",
        "select_animation": "Select Animation",
        "appearance": "Appearance",
        "appearance_help": "Choose the application theme",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "theme_system": "System",
        "help_title": "Help / Usage Guide",
        "help_text": """This tool is designed to be used with Smooth's HKX Editor.

HKX File Tools:
• Require a normal .hkx animation file.
• Used for duplication and Attack/PowerAttack conversions.

Animation Tools:
• Require the JSON animation format exported from Smooth's HKX Editor.
• Used for merging, reversing, and stretching/compressing animations.

Workflow:
1. Export your animation as JSON from Smooth's HKX Editor.
2. Modify the animation using this toolkit.
3. Import the finished JSON back into Smooth's HKX Editor.
4. Export the final HKX animation.""",
    },
    "한국어": {
        "title": "HKX 애니메이션 도구",
        "home_title": "HKX 애니메이션 도구",
        "home_subtitle": "사이드바에서 카테고리를 선택하세요",
        "ready": "준비 완료",
        "settings": "설정",
        "language": "언어",
        "language_help": "UI 언어를 선택하세요",
        "nav_home": "홈",
        "nav_merge": "애니메이션 병합",
        "nav_reverse": "애니메이션 반전",
        "nav_scale": "늘리기 / 압축",
        "nav_file": "HKX 파일 도구",
        "nav_settings": "설정",
        "file_tools_title": "HKX 파일 도구",
        "browse_hkx": "HKX 선택",
        "duplicate_desc": "선택한 공격 애니메이션을 10개 공격 슬롯 모두에 복제합니다",
        "duplicate_btn": "공격 복제",
        "attack_desc": "모든 Attack 애니메이션 파일 이름을 PowerAttack 파일로 변경합니다",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "모든 PowerAttack 애니메이션 파일 이름을 Attack 파일로 되돌립니다",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "애니메이션 병합 도구",
        "merge_select_a": "애니메이션 json A 선택",
        "merge_select_b": "애니메이션 json B 선택",
        "merge_a_start": "애니메이션 A 시작 프레임 제거",
        "merge_a_end": "애니메이션 A 종료 프레임 제거",
        "merge_b_start": "애니메이션 B 시작 프레임 제거",
        "merge_b_end": "애니메이션 B 종료 프레임 제거",
        "select_output": "출력 위치 선택",
        "merge_btn": "애니메이션 병합",
        "reverse_tools_title": "애니메이션 반전 도구",
        "reverse_help": "단일 JSON 애니메이션을 선택하고 반전된 복사본을 저장합니다.",
        "reverse_select": "애니메이션 선택",
        "reverse_output_label": "반전 출력 파일 이름",
        "reverse_output_btn": "출력 위치 선택",
        "reverse_btn": "애니메이션 반전",
        "scale_tools_title": "애니메이션 늘리기 / 압축",
        "scale_help": "프레임 타이밍을 조정하여 애니메이션 속도를 변경합니다.",
        "scale_select": "애니메이션 선택",
        "scale_ratio_label": "비율 (0.5 = 더 빠름, 2.0 = 더 느림)",
        "scale_output_btn": "출력 위치 선택",
        "scale_btn": "애니메이션 크기 조정",
        "scale_output_label": "축소/확대 출력 파일 이름",
        "select_sidebar": "사이드바에서 카테고리를 선택하세요",
        "select_animation_a": "애니메이션 A 선택",
        "select_animation_b": "애니메이션 B 선택",
        "select_animation": "애니메이션 선택",
        "appearance": "테마",
        "appearance_help": "애플리케이션 테마를 선택하세요",
        "theme_dark": "다크",
        "theme_light": "라이트",
        "theme_system": "시스템",
        "help_title": "도움말 / 사용 안내",
        "help_text": """이 도구는 Smooth의 HKX Editor와 함께 사용하도록 제작되었습니다.

HKX 파일 도구:
• 일반 .hkx 애니메이션 파일만 필요합니다.
• 애니메이션 복제 및 Attack/PowerAttack 변환에 사용됩니다.

애니메이션 도구:
• Smooth의 HKX Editor에서 내보낸 JSON 애니메이션 파일이 필요합니다.
• 애니메이션 병합, 반전, 늘리기/압축 기능에 사용됩니다.

사용 방법:
1. Smooth의 HKX Editor에서 애니메이션을 JSON으로 내보냅니다.
2. 이 툴을 사용해 애니메이션을 수정합니다.
3. 수정된 JSON을 Smooth의 HKX Editor로 다시 가져옵니다.
4. 최종 HKX 애니메이션을 내보냅니다.""",
    },
    "日本語": {
        "title": "HKXアニメーションツール",
        "home_title": "HKXアニメーションツール",
        "home_subtitle": "サイドバーからカテゴリを選択してください",
        "ready": "準備完了",
        "settings": "設定",
        "language": "言語",
        "language_help": "UI言語を選択してください",
        "nav_home": "ホーム",
        "nav_merge": "アニメーション結合",
        "nav_reverse": "アニメーション反転",
        "nav_scale": "伸縮 / 圧縮",
        "nav_file": "HKXファイルツール",
        "nav_settings": "設定",
        "file_tools_title": "HKXファイルツール",
        "browse_hkx": "HKXを選択",
        "duplicate_desc": "選択した攻撃アニメーションを10個の攻撃スロットに複製します",
        "duplicate_btn": "攻撃を複製",
        "attack_desc": "AttackアニメーションファイルをPowerAttackファイルに変更します",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "PowerAttackアニメーションファイルをAttackファイルに戻します",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "アニメーション結合ツール",
        "merge_select_a": "アニメーションJSON Aを選択",
        "merge_select_b": "アニメーションJSON Bを選択",
        "merge_a_start": "アニメーションA開始フレーム削除",
        "merge_a_end": "アニメーションA終了フレーム削除",
        "merge_b_start": "アニメーションB開始フレーム削除",
        "merge_b_end": "アニメーションB終了フレーム削除",
        "select_output": "保存先を選択",
        "merge_btn": "アニメーション結合",
        "reverse_tools_title": "アニメーション反転ツール",
        "reverse_help": "JSONアニメーションを選択して反転コピーを保存します",
        "reverse_select": "アニメーション選択",
        "reverse_output_label": "反転後ファイル名",
        "reverse_output_btn": "保存先を選択",
        "reverse_btn": "アニメーション反転",
        "scale_tools_title": "アニメーション伸縮",
        "scale_help": "フレーム時間を変更してアニメーション速度を調整します",
        "scale_select": "アニメーション選択",
        "scale_ratio_label": "倍率 (0.5 = 高速, 2.0 = 低速)",
        "scale_output_label": "出力ファイル名",
        "scale_output_btn": "保存先を選択",
        "scale_btn": "アニメーション調整",
        "select_sidebar": "サイドバーからカテゴリを選択してください",
        "select_animation_a": "アニメーションAを選択",
        "select_animation_b": "アニメーションBを選択",
        "select_animation": "アニメーション選択",
        "appearance": "外観",
        "appearance_help": "アプリケーションのテーマを選択してください",
        "theme_dark": "ダーク",
        "theme_light": "ライト",
        "theme_system": "システム",
        "help_title": "ヘルプ / 使用方法",
        "help_text": """このツールはSmoothのHKX Editorと併用するために作成されています。

HKXファイルツール:
• 通常の.hkxアニメーションファイルのみ必要です。
• アニメーション複製やAttack/PowerAttack変換に使用します。

アニメーションツール:
• SmoothのHKX EditorからエクスポートしたJSONアニメーションが必要です。
• アニメーション結合、反転、伸縮/圧縮に使用します。

使用手順:
1. SmoothのHKX EditorからアニメーションをJSONとしてエクスポートします。
2. このツールでアニメーションを編集します。
3. 編集したJSONをSmoothのHKX Editorへ戻します。
4. 完成したHKXアニメーションを書き出します。""",
    },
    "Português": {
        "title": "Ferramenta de Animação HKX",
        "home_title": "Ferramenta de Animação HKX",
        "home_subtitle": "Selecione uma categoria na barra lateral",
        "ready": "Pronto",
        "settings": "Configurações",
        "language": "Idioma",
        "language_help": "Escolha o idioma da interface",
        "nav_home": "Início",
        "nav_merge": "Mesclar Animações",
        "nav_reverse": "Inverter Animação",
        "nav_scale": "Alongar / Comprimir",
        "nav_file": "Ferramentas de Arquivo HKX",
        "nav_settings": "Configurações",
        "file_tools_title": "Ferramentas de Arquivo HKX",
        "browse_hkx": "Selecionar HKX",
        "duplicate_desc": "Duplica a animação de ataque selecionada para todos os 10 espaços de ataque disponíveis",
        "duplicate_btn": "Duplicar Ataques",
        "attack_desc": "Renomeia todos os arquivos de animação Attack para arquivos PowerAttack",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "Renomeia todos os arquivos PowerAttack novamente para Attack",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "Ferramentas de Mesclagem de Animação",
        "merge_select_a": "Selecionar Animação JSON A",
        "merge_select_b": "Selecionar Animação JSON B",
        "merge_a_start": "Remover Frames Iniciais da Animação A",
        "merge_a_end": "Remover Frames Finais da Animação A",
        "merge_b_start": "Remover Frames Iniciais da Animação B",
        "merge_b_end": "Remover Frames Finais da Animação B",
        "select_output": "Selecionar Local de Saída",
        "merge_btn": "MESCLAR ANIMAÇÕES",
        "reverse_tools_title": "Ferramentas de Inversão de Animação",
        "reverse_help": "Selecione uma animação JSON e salve uma cópia invertida.",
        "reverse_select": "Selecionar Animação",
        "reverse_output_label": "Nome do Arquivo de Saída Invertido",
        "reverse_output_btn": "Selecionar Saída",
        "reverse_btn": "INVERTER ANIMAÇÃO",
        "scale_tools_title": "Alongar / Comprimir Animação",
        "scale_help": "Ajuste a velocidade da animação alterando o tempo dos frames.",
        "scale_select": "Selecionar Animação",
        "scale_ratio_label": "Proporção (0.5 = mais rápido, 2.0 = mais lento)",
        "scale_output_btn": "Selecionar Saída",
        "scale_btn": "AJUSTAR ANIMAÇÃO",
        "scale_output_label": "Nome do Arquivo de Saída",
        "select_sidebar": "Selecione uma categoria na barra lateral",
        "select_animation_a": "Selecionar Animação A",
        "select_animation_b": "Selecionar Animação B",
        "select_animation": "Selecionar Animação",
        "appearance": "Aparência",
        "appearance_help": "Escolha o tema da aplicação",
        "theme_dark": "Escuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "help_title": "Ajuda / Guia de Uso",
        "help_text": """Esta ferramenta foi criada para ser usada com o HKX Editor do Smooth.

Ferramentas de Arquivo HKX:
• Requerem apenas um arquivo de animação .hkx normal.
• Usadas para duplicação de animações e conversões Attack/PowerAttack.

Ferramentas de Animação:
• Requerem o formato JSON exportado pelo HKX Editor do Smooth.
• Usadas para mesclar, inverter e ajustar o tamanho/velocidade das animações.

Como usar:
1. Exporte sua animação como JSON pelo HKX Editor do Smooth.
2. Modifique a animação usando esta ferramenta.
3. Importe o JSON final novamente no HKX Editor do Smooth.
4. Exporte a animação HKX final.""",
    },
    "Español": {
        "title": "Herramienta de Animación HKX",
        "home_title": "Herramienta de Animación HKX",
        "home_subtitle": "Seleccione una categoría en la barra lateral",
        "ready": "Listo",
        "settings": "Configuración",
        "language": "Idioma",
        "language_help": "Seleccione el idioma de la interfaz",
        "nav_home": "Inicio",
        "nav_merge": "Combinar Animaciones",
        "nav_reverse": "Invertir Animación",
        "nav_scale": "Estirar / Comprimir",
        "nav_file": "Herramientas de Archivos HKX",
        "nav_settings": "Configuración",
        "file_tools_title": "Herramientas de Archivos HKX",
        "browse_hkx": "Seleccionar HKX",
        "duplicate_desc": "Duplica la animación de ataque seleccionada en los 10 espacios de ataque disponibles",
        "duplicate_btn": "Duplicar Ataques",
        "attack_desc": "Cambia el nombre de todos los archivos de animación Attack a archivos PowerAttack",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "Cambia el nombre de todos los archivos PowerAttack nuevamente a Attack",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "Herramientas de Combinación de Animaciones",
        "merge_select_a": "Seleccionar Animación JSON A",
        "merge_select_b": "Seleccionar Animación JSON B",
        "merge_a_start": "Eliminar Frames Iniciales de la Animación A",
        "merge_a_end": "Eliminar Frames Finales de la Animación A",
        "merge_b_start": "Eliminar Frames Iniciales de la Animación B",
        "merge_b_end": "Eliminar Frames Finales de la Animación B",
        "select_output": "Seleccionar Ubicación de Salida",
        "merge_btn": "COMBINAR ANIMACIONES",
        "reverse_tools_title": "Herramientas de Inversión de Animaciones",
        "reverse_help": "Seleccione una animación JSON y guarde una copia invertida.",
        "reverse_select": "Seleccionar Animación",
        "reverse_output_label": "Nombre del Archivo de Salida Invertido",
        "reverse_output_btn": "Seleccionar Salida",
        "reverse_btn": "INVERTIR ANIMACIÓN",
        "scale_tools_title": "Estirar / Comprimir Animación",
        "scale_help": "Ajusta la velocidad de la animación modificando el tiempo de los frames.",
        "scale_select": "Seleccionar Animación",
        "scale_ratio_label": "Proporción (0.5 = más rápido, 2.0 = más lento)",
        "scale_output_btn": "Seleccionar Salida",
        "scale_btn": "AJUSTAR ANIMACIÓN",
        "scale_output_label": "Nombre del Archivo de Salida",
        "select_sidebar": "Seleccione una categoría en la barra lateral",
        "select_animation_a": "Seleccionar Animación A",
        "select_animation_b": "Seleccionar Animación B",
        "select_animation": "Seleccionar Animación",
        "appearance": "Apariencia",
        "appearance_help": "Elige el tema de la aplicación",
        "theme_dark": "Oscuro",
        "theme_light": "Claro",
        "theme_system": "Sistema",
        "help_title": "Ayuda / Guía de Uso",
        "help_text": """Esta herramienta está diseñada para usarse con el HKX Editor de Smooth.

Herramientas de Archivos HKX:
• Solo requieren un archivo de animación .hkx normal.
• Se utilizan para duplicar animaciones y convertir Attack/PowerAttack.

Herramientas de Animación:
• Requieren el formato JSON exportado desde el HKX Editor de Smooth.
• Se utilizan para combinar, invertir y ajustar la velocidad/tamaño de animaciones.

Cómo usar:
1. Exporta tu animación como JSON desde el HKX Editor de Smooth.
2. Modifica la animación usando esta herramienta.
3. Importa el JSON terminado nuevamente en el HKX Editor de Smooth.
4. Exporta la animación HKX final.""",
    },
    "中文": {
        "title": "HKX动画工具",
        "home_title": "HKX动画工具",
        "home_subtitle": "请从侧边栏选择一个类别",
        "ready": "就绪",
        "settings": "设置",
        "language": "语言",
        "language_help": "选择界面语言",
        "nav_home": "主页",
        "nav_merge": "动画合并",
        "nav_reverse": "动画反转",
        "nav_scale": "拉伸 / 压缩",
        "nav_file": "HKX文件工具",
        "nav_settings": "设置",
        "file_tools_title": "HKX文件工具",
        "browse_hkx": "选择HKX",
        "duplicate_desc": "将选中的攻击动画复制到所有10个可用攻击槽位",
        "duplicate_btn": "复制攻击动画",
        "attack_desc": "将所有Attack动画文件重命名为PowerAttack文件",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "将所有PowerAttack动画文件重命名回Attack文件",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "动画合并工具",
        "merge_select_a": "选择动画JSON A",
        "merge_select_b": "选择动画JSON B",
        "merge_a_start": "删除动画A开头帧",
        "merge_a_end": "删除动画A结尾帧",
        "merge_b_start": "删除动画B开头帧",
        "merge_b_end": "删除动画B结尾帧",
        "select_output": "选择输出位置",
        "merge_btn": "合并动画",
        "reverse_tools_title": "动画反转工具",
        "reverse_help": "选择一个JSON动画并保存反转后的副本。",
        "reverse_select": "选择动画",
        "reverse_output_label": "反转输出文件名",
        "reverse_output_btn": "选择输出位置",
        "reverse_btn": "反转动画",
        "scale_tools_title": "动画拉伸 / 压缩",
        "scale_help": "通过调整帧时间来改变动画速度。",
        "scale_select": "选择动画",
        "scale_ratio_label": "比例 (0.5 = 更快, 2.0 = 更慢)",
        "scale_output_btn": "选择输出位置",
        "scale_btn": "调整动画",
        "scale_output_label": "输出文件名",
        "select_sidebar": "请从侧边栏选择一个类别",
        "select_animation_a": "选择动画A",
        "select_animation_b": "选择动画B",
        "select_animation": "选择动画",
        "appearance": "外观",
        "appearance_help": "选择应用程序主题",
        "theme_dark": "深色",
        "theme_light": "浅色",
        "theme_system": "系统",
        "help_title": "帮助 / 使用指南",
        "help_text": """此工具设计用于配合 Smooth 的 HKX Editor 使用。

HKX 文件工具:
• 只需要普通的 .hkx 动画文件。
• 用于动画复制以及 Attack/PowerAttack 转换。

动画工具:
• 需要从 Smooth 的 HKX Editor 导出的 JSON 动画格式。
• 用于动画合并、反转以及拉伸/压缩。

使用步骤:
1. 从 Smooth 的 HKX Editor 导出动画 JSON。
2. 使用此工具修改动画。
3. 将完成后的 JSON 导回 Smooth 的 HKX Editor。
4. 导出最终 HKX 动画。""",
    },
    "Русский": {
        "title": "Инструмент анимации HKX",
        "home_title": "Инструмент анимации HKX",
        "home_subtitle": "Выберите категорию на боковой панели",
        "ready": "Готово",
        "settings": "Настройки",
        "language": "Язык",
        "language_help": "Выберите язык интерфейса",
        "nav_home": "Главная",
        "nav_merge": "Объединение анимаций",
        "nav_reverse": "Обратная анимация",
        "nav_scale": "Растянуть / Сжать",
        "nav_file": "Инструменты HKX файлов",
        "nav_settings": "Настройки",
        "file_tools_title": "Инструменты HKX файлов",
        "browse_hkx": "Выбрать HKX",
        "duplicate_desc": "Копирует выбранную атаку во все 10 доступных слотов атак",
        "duplicate_btn": "Дублировать атаки",
        "attack_desc": "Переименовывает все файлы анимаций Attack в файлы PowerAttack",
        "attack_btn": "Attack → PowerAttack",
        "power_desc": "Возвращает имена файлов PowerAttack обратно в Attack",
        "power_btn": "PowerAttack → Attack",
        "merge_tools_title": "Инструменты объединения анимаций",
        "merge_select_a": "Выбрать JSON анимации A",
        "merge_select_b": "Выбрать JSON анимации B",
        "merge_a_start": "Удаление начальных кадров анимации A",
        "merge_a_end": "Удаление конечных кадров анимации A",
        "merge_b_start": "Удаление начальных кадров анимации B",
        "merge_b_end": "Удаление конечных кадров анимации B",
        "select_output": "Выбрать место сохранения",
        "merge_btn": "ОБЪЕДИНИТЬ АНИМАЦИИ",
        "reverse_tools_title": "Инструменты обратной анимации",
        "reverse_help": "Выберите одну JSON анимацию и сохраните перевёрнутую копию.",
        "reverse_select": "Выбрать анимацию",
        "reverse_output_label": "Имя перевёрнутого файла",
        "reverse_output_btn": "Выбрать место сохранения",
        "reverse_btn": "ОБРАТИТЬ АНИМАЦИЮ",
        "scale_tools_title": "Растянуть / Сжать анимацию",
        "scale_help": "Изменяет скорость анимации путем настройки времени кадров.",
        "scale_select": "Выбрать анимацию",
        "scale_ratio_label": "Соотношение (0.5 = быстрее, 2.0 = медленнее)",
        "scale_output_btn": "Выбрать место сохранения",
        "scale_btn": "ИЗМЕНИТЬ АНИМАЦИЮ",
        "scale_output_label": "Имя выходного файла",
        "select_sidebar": "Выберите категорию на боковой панели",
        "select_animation_a": "Выбрать анимацию A",
        "select_animation_b": "Выбрать анимацию B",
        "select_animation": "Выбрать анимацию",
        "appearance": "Оформление",
        "appearance_help": "Выберите тему приложения",
        "theme_dark": "Тёмная",
        "theme_light": "Светлая",
        "theme_system": "Системная",
        "help_title": "Справка / Руководство",
        "help_text": """Этот инструмент предназначен для использования вместе с HKX Editor от Smooth.

Инструменты HKX файлов:
• Требуют только обычный файл анимации .hkx.
• Используются для дублирования анимаций и преобразования Attack/PowerAttack.

Инструменты анимации:
• Требуют формат JSON, экспортированный из HKX Editor от Smooth.
• Используются для объединения, разворота и изменения скорости/размера анимаций.

Как использовать:
1. Экспортируйте анимацию в JSON из HKX Editor от Smooth.
2. Измените анимацию с помощью этого инструмента.
3. Импортируйте готовый JSON обратно в HKX Editor от Smooth.
4. Экспортируйте финальную HKX анимацию.""",
    },
}


def load_language():
    global LANGUAGE
    if os.path.exists(language_cache):
        with open(language_cache, "r", encoding="utf-8") as f:
            saved = f.read().strip()
            if saved in translations:
                LANGUAGE = saved


def save_language():
    with open(language_cache, "w", encoding="utf-8") as f:
        f.write(LANGUAGE)


def t(key):
    return translations[LANGUAGE].get(key, key)


load_language()

# Korean-safe font on Windows; okay for English too.
UI_FONT = "Malgun Gothic"


# =========================================================
# APPEARANCE / APP
# =========================================================
def load_appearance():
    global APPEARANCE

    if os.path.exists(appearance_cache):
        with open(appearance_cache, "r", encoding="utf-8") as f:
            saved = f.read().strip()

            if saved in ["Dark", "Light", "System"]:
                APPEARANCE = saved


def save_appearance():
    with open(appearance_cache, "w", encoding="utf-8") as f:
        f.write(APPEARANCE)


load_appearance()

ctk.set_appearance_mode(APPEARANCE)
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(t("title"))
app.geometry("1000x700")

selected_file = ""

animation_a = ""
animation_b = ""
merge_output = "merged.hkxproj.json"

reverse_file = ""
reverse_output = "reversed.hkxproj.json"

scale_file = ""
scale_output = "scaled.hkxproj.json"

hkx_cache = "last_hkx_folder.txt"
animation_cache = "last_animation_folder.txt"

current_page = None


def change_appearance(choice):

    global APPEARANCE

    appearance_map = {
        t("theme_dark"): "Dark",
        t("theme_light"): "Light",
        t("theme_system"): "System",
        "Dark": "Dark",
        "Light": "Light",
        "System": "System",
    }

    if choice in appearance_map:
        APPEARANCE = appearance_map[choice]

        save_appearance()

        ctk.set_appearance_mode(APPEARANCE)

        refresh_language()

        log(f"Appearance changed to {APPEARANCE}")


# =========================================================
# LOGGING
# =========================================================


def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_box.configure(state="normal")
    log_box.insert("end", f"[{timestamp}] {message}\n")
    log_box.see("end")
    log_box.configure(state="disabled")


def set_status(text):
    status.configure(text=text)


# =========================================================
# PAGE SWITCHING
# =========================================================

page_container = ctk.CTkFrame(app, corner_radius=15)
page_container.pack(side="right", expand=True, fill="both", padx=20, pady=20)


def show_page(page):
    global current_page

    if current_page:
        current_page.pack_forget()

    current_page = page
    current_page.pack(expand=True, fill="both")


# =========================================================
# FILE TOOLS
# =========================================================


def browse_hkx():
    global selected_file

    if os.path.exists(hkx_cache):
        with open(hkx_cache, "r", encoding="utf-8") as f:
            last_folder = f.read().strip()
    else:
        last_folder = os.getcwd()

    path = filedialog.askopenfilename(
        title=t("browse_hkx"),
        initialdir=last_folder,
        filetypes=[("HKX Files", "*.hkx")],
    )

    if path:
        selected_file = path

        with open(hkx_cache, "w", encoding="utf-8") as f:
            f.write(os.path.dirname(path))

        file_entry.delete(0, "end")
        file_entry.insert(0, path)

        log(f"Selected HKX: {path}")
        update_hkx_buttons()


def duplicate():
    if not selected_file:
        log("ERROR: No HKX selected")
        return

    result = duplicate_attacks(selected_file, log)
    log(result["message"])


def rename_attack():
    if not selected_file:
        log("ERROR: No HKX selected")
        return

    folder = os.path.dirname(selected_file)
    result = rename_attack_to_power(folder, log)
    log(result["message"])


def rename_power():
    if not selected_file:
        log("ERROR: No HKX selected")
        return

    folder = os.path.dirname(selected_file)
    result = rename_power_to_attack(folder, log)
    log(result["message"])


# =========================================================
# ANIMATION MERGE TOOLS
# =========================================================


def get_animation_folder():
    if os.path.exists(animation_cache):
        with open(animation_cache, "r", encoding="utf-8") as f:
            folder = f.read().strip()
            return folder if folder else os.getcwd()
    return os.getcwd()


def save_animation_folder(path):
    with open(animation_cache, "w", encoding="utf-8") as f:
        f.write(os.path.dirname(path))


def browse_animation_a():
    global animation_a

    path = filedialog.askopenfilename(
        title=t("select_animation_a"),
        initialdir=get_animation_folder(),
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        animation_a = path
        save_animation_folder(path)

        anim_a_entry.delete(0, "end")
        anim_a_entry.insert(0, path)

        log(f"Animation A: {path}")
        update_merge_button()


def browse_animation_b():
    global animation_b

    path = filedialog.askopenfilename(
        title=t("select_animation_b"),
        initialdir=get_animation_folder(),
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        animation_b = path
        save_animation_folder(path)

        anim_b_entry.delete(0, "end")
        anim_b_entry.insert(0, path)

        log(f"Animation B: {path}")
        update_merge_button()


def browse_output():
    global merge_output

    path = filedialog.asksaveasfilename(
        title=t("select_output"),
        defaultextension=".json",
        initialdir=get_animation_folder(),
        initialfile="merged.hkxproj.json",
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        merge_output = path
        save_animation_folder(path)

        output_entry.delete(0, "end")
        output_entry.insert(0, path)


def merge():
    if not animation_a or not animation_b:
        log("ERROR: Missing animations")
        return

    try:
        result = merge_animations(
            animation_a,
            animation_b,
            int(start_a_entry.get()),
            int(end_a_entry.get()),
            int(start_b_entry.get()),
            int(end_b_entry.get()),
            merge_output,
            log,
        )
        log(result["message"])
    except Exception as e:
        log(f"ERROR: {e}")


# =========================================================
# REVERSE ANIMATION TOOLS
# =========================================================


def browse_reverse_animation():
    global reverse_file

    path = filedialog.askopenfilename(
        title=t("reverse_select"),
        initialdir=get_animation_folder(),
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        reverse_file = path
        save_animation_folder(path)

        reverse_entry.delete(0, "end")
        reverse_entry.insert(0, path)

        log(f"Reverse Animation: {path}")
        update_reverse_button()


def browse_reverse_output():
    global reverse_output

    path = filedialog.asksaveasfilename(
        title=t("select_output"),
        initialdir=get_animation_folder(),
        defaultextension=".json",
        initialfile="reversed.hkxproj.json",
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        reverse_output = path
        save_animation_folder(path)

        reverse_output_entry.delete(0, "end")
        reverse_output_entry.insert(0, path)


def reverse():
    global reverse_output

    if not reverse_file:
        log("ERROR: No animation selected")
        return

    if reverse_output == "reversed.hkxproj.json":
        folder = os.path.dirname(reverse_file)
        filename = os.path.splitext(os.path.basename(reverse_file))[0]
        reverse_output = os.path.join(folder, filename + "_reversed.hkxproj.json")
        reverse_output_entry.delete(0, "end")
        reverse_output_entry.insert(0, reverse_output)

    log("Saving reversed animation to:")
    log(reverse_output)

    try:
        result = reverse_animation(reverse_file, reverse_output, log)
        log(result["message"])

        if result["success"]:
            if os.path.exists(reverse_output):
                log("SUCCESS: File created successfully.")
            else:
                log("ERROR: Function completed but file was not found.")

    except Exception as e:
        log(f"ERROR: {e}")


# =========================================================
# SCALE ANIMATION TOOLS
# =========================================================


def browse_scale_animation():
    global scale_file

    path = filedialog.askopenfilename(
        title=t("scale_select"),
        initialdir=get_animation_folder(),
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        scale_file = path
        save_animation_folder(path)

        scale_entry.delete(0, "end")
        scale_entry.insert(0, path)

        log(f"Scale Animation: {path}")
        update_scale_button()


def browse_scale_output():
    global scale_output

    path = filedialog.asksaveasfilename(
        title=t("select_output"),
        initialdir=get_animation_folder(),
        defaultextension=".json",
        initialfile="scaled.hkxproj.json",
        filetypes=[("JSON Files", "*.json")],
    )

    if path:
        scale_output = path
        save_animation_folder(path)

        scale_output_entry.delete(0, "end")
        scale_output_entry.insert(0, path)


def scale():
    if not scale_file:
        log("ERROR: No animation selected")
        return

    try:
        ratio = float(scale_ratio_entry.get())
        result = scale_animation(scale_file, ratio, scale_output, log)
        log(result["message"])

        if result["success"]:
            if os.path.exists(scale_output):
                log("SUCCESS: Scaled animation created.")
            else:
                log("ERROR: Function completed but file was not found.")

    except Exception as e:
        log(f"ERROR: {e}")


# =========================================================
# SETTINGS / LOCALIZATION
# =========================================================


def change_language(choice):
    global LANGUAGE

    if choice not in translations:
        return

    LANGUAGE = choice
    save_language()
    refresh_language()
    log(f"Language changed to {choice}")


# =========================================================
# Button Updates
# =========================================================


def update_merge_button():
    if animation_a and animation_b:
        merge_button.configure(
            state="normal",
            fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"],
        )
    else:
        merge_button.configure(
            state="disabled", fg_color="gray50", hover_color="gray50"
        )


def update_reverse_button():
    if reverse_file:
        reverse_button.configure(
            state="normal",
            fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"],
        )
    else:
        reverse_button.configure(
            state="disabled", fg_color="gray50", hover_color="gray50"
        )


def update_scale_button():
    if scale_file:
        scale_button.configure(
            state="normal",
            fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"],
        )
    else:
        scale_button.configure(
            state="disabled", fg_color="gray50", hover_color="gray50"
        )


def update_hkx_buttons():
    if selected_file:
        for button in [duplicate_button, attack_button, power_button]:
            button.configure(
                state="normal",
                fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
                hover_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"],
            )
    else:
        for button in [duplicate_button, attack_button, power_button]:
            button.configure(state="disabled", fg_color="gray50", hover_color="gray50")


# =========================================================
# PAGES
# =========================================================

home_page = ctk.CTkFrame(page_container)

home_title_label = ctk.CTkLabel(
    home_page, text=t("home_title"), font=(UI_FONT, 32, "bold")
)
home_title_label.pack(pady=100)

home_subtitle_label = ctk.CTkLabel(
    home_page, text=t("home_subtitle"), font=(UI_FONT, 16)
)
home_subtitle_label.pack()

# -------------------------
# File Page
# -------------------------

file_page = ctk.CTkFrame(page_container)

file_page_title_label = ctk.CTkLabel(
    file_page, text=t("file_tools_title"), font=(UI_FONT, 26, "bold")
)
file_page_title_label.pack(pady=20)

file_entry = ctk.CTkEntry(file_page, width=600)
file_entry.pack(pady=10)

browse_hkx_button = ctk.CTkButton(file_page, text=t("browse_hkx"), command=browse_hkx)
browse_hkx_button.pack()


duplicate_desc_label = ctk.CTkLabel(
    file_page,
    text=t("duplicate_desc"),
    font=(UI_FONT, 13),
)
duplicate_desc_label.pack(pady=(10, 2))

duplicate_button = ctk.CTkButton(
    file_page,
    text=t("duplicate_btn"),
    width=250,
    command=duplicate,
    fg_color="gray50",
    hover_color="gray50",
    state="disabled",
)
duplicate_button.pack(pady=5)

attack_desc_label = ctk.CTkLabel(
    file_page,
    text=t("attack_desc"),
    font=(UI_FONT, 13),
)
attack_desc_label.pack(pady=(10, 2))

attack_button = ctk.CTkButton(
    file_page,
    text=t("attack_btn"),
    width=250,
    command=rename_attack,
    fg_color="gray50",
    hover_color="gray50",
    state="disabled",
)
attack_button.pack(pady=5)

power_desc_label = ctk.CTkLabel(
    file_page,
    text=t("power_desc"),
    font=(UI_FONT, 13),
)
power_desc_label.pack(pady=(10, 2))

power_button = ctk.CTkButton(
    file_page,
    text=t("power_btn"),
    width=250,
    command=rename_power,
    fg_color="gray50",
    hover_color="gray50",
    state="disabled",
)
power_button.pack(pady=5)

# -------------------------
# Animation Merge Page
# -------------------------

merge_page = ctk.CTkFrame(page_container)

merge_page_title_label = ctk.CTkLabel(
    merge_page, text=t("merge_tools_title"), font=(UI_FONT, 26, "bold")
)
merge_page_title_label.pack(pady=15)

anim_a_entry = ctk.CTkEntry(merge_page, width=550)
anim_a_entry.pack()

merge_select_a_button = ctk.CTkButton(
    merge_page, text=t("merge_select_a"), command=browse_animation_a
)
merge_select_a_button.pack(pady=5)

merge_a_start_label = ctk.CTkLabel(merge_page, text=t("merge_a_start"))
merge_a_start_label.pack()

start_a_entry = ctk.CTkEntry(merge_page, width=100)
start_a_entry.insert(0, "0")
start_a_entry.pack()

merge_a_end_label = ctk.CTkLabel(merge_page, text=t("merge_a_end"))
merge_a_end_label.pack()

end_a_entry = ctk.CTkEntry(merge_page, width=100)
end_a_entry.insert(0, "0")
end_a_entry.pack()

anim_b_entry = ctk.CTkEntry(merge_page, width=550)
anim_b_entry.pack(pady=10)

merge_select_b_button = ctk.CTkButton(
    merge_page, text=t("merge_select_b"), command=browse_animation_b
)
merge_select_b_button.pack()

merge_b_start_label = ctk.CTkLabel(merge_page, text=t("merge_b_start"))
merge_b_start_label.pack()

start_b_entry = ctk.CTkEntry(merge_page, width=100)
start_b_entry.insert(0, "0")
start_b_entry.pack()

merge_b_end_label = ctk.CTkLabel(merge_page, text=t("merge_b_end"))
merge_b_end_label.pack()

end_b_entry = ctk.CTkEntry(merge_page, width=100)
end_b_entry.insert(0, "0")
end_b_entry.pack()

output_entry = ctk.CTkEntry(merge_page, width=550)
output_entry.insert(0, "merged.hkxproj.json")
output_entry.pack(pady=10)

merge_output_button = ctk.CTkButton(
    merge_page, text=t("select_output"), command=browse_output
)
merge_output_button.pack()

merge_button = ctk.CTkButton(
    merge_page,
    text=t("merge_btn"),
    width=300,
    height=45,
    command=merge,
    fg_color="gray50",
    hover_color="gray60",
    state="disabled",
)
merge_button.pack(pady=15)

# -------------------------
# Reverse Animation Page
# -------------------------

reverse_page = ctk.CTkFrame(page_container)

reverse_page_title_label = ctk.CTkLabel(
    reverse_page, text=t("reverse_tools_title"), font=(UI_FONT, 26, "bold")
)
reverse_page_title_label.pack(pady=15)

reverse_help_label = ctk.CTkLabel(
    reverse_page,
    text=t("reverse_help"),
    font=(UI_FONT, 14),
)
reverse_help_label.pack(pady=(0, 15))

reverse_entry = ctk.CTkEntry(reverse_page, width=550)
reverse_entry.pack()

reverse_select_button = ctk.CTkButton(
    reverse_page, text=t("reverse_select"), command=browse_reverse_animation
)
reverse_select_button.pack(pady=5)

reverse_output_label = ctk.CTkLabel(reverse_page, text=t("reverse_output_label"))
reverse_output_label.pack()

reverse_output_entry = ctk.CTkEntry(reverse_page, width=550)
reverse_output_entry.insert(0, "reversed.hkxproj.json")
reverse_output_entry.pack(pady=5)

reverse_output_button = ctk.CTkButton(
    reverse_page, text=t("reverse_output_btn"), command=browse_reverse_output
)
reverse_output_button.pack()

reverse_button = ctk.CTkButton(
    reverse_page,
    text=t("reverse_btn"),
    width=300,
    height=45,
    command=reverse,
    fg_color="gray50",
    hover_color="gray50",
    state="disabled",
)
reverse_button.pack(pady=15)

# -------------------------
# Scale Animation Page
# -------------------------

scale_page = ctk.CTkFrame(page_container)

scale_page_title_label = ctk.CTkLabel(
    scale_page, text=t("scale_tools_title"), font=(UI_FONT, 26, "bold")
)
scale_page_title_label.pack(pady=15)

scale_help_label = ctk.CTkLabel(
    scale_page,
    text=t("scale_help"),
    font=(UI_FONT, 14),
)
scale_help_label.pack(pady=(0, 15))

scale_entry = ctk.CTkEntry(scale_page, width=550)
scale_entry.pack()

scale_select_button = ctk.CTkButton(
    scale_page, text=t("scale_select"), command=browse_scale_animation
)
scale_select_button.pack(pady=5)

scale_ratio_label = ctk.CTkLabel(scale_page, text=t("scale_ratio_label"))
scale_ratio_label.pack()

scale_ratio_entry = ctk.CTkEntry(scale_page, width=100)
scale_ratio_entry.insert(0, "1.0")
scale_ratio_entry.pack(pady=5)

scale_output_label = ctk.CTkLabel(scale_page, text=t("scale_output_label"))
scale_output_label.pack()

scale_output_entry = ctk.CTkEntry(scale_page, width=550)
scale_output_entry.insert(0, "scaled.hkxproj.json")
scale_output_entry.pack(pady=10)

scale_output_button = ctk.CTkButton(
    scale_page, text=t("scale_output_btn"), command=browse_scale_output
)
scale_output_button.pack()

scale_button = ctk.CTkButton(
    scale_page,
    text=t("scale_btn"),
    width=300,
    height=45,
    command=scale,
    fg_color="gray50",
    hover_color="gray50",
    state="disabled",
)
scale_button.pack(pady=15)

# -------------------------
# Settings Page
# -------------------------

settings_page = ctk.CTkScrollableFrame(page_container)

settings_title_label = ctk.CTkLabel(
    settings_page, text=t("settings"), font=(UI_FONT, 26, "bold")
)
settings_title_label.pack(pady=20)


# Language Settings

settings_help_label = ctk.CTkLabel(
    settings_page,
    text=t("language_help"),
    font=(UI_FONT, 14),
)
settings_help_label.pack(pady=(0, 12))


language_label = ctk.CTkLabel(settings_page, text=t("language"), font=(UI_FONT, 16))
language_label.pack(pady=(10, 6))


language_menu = ctk.CTkOptionMenu(
    settings_page,
    values=list(translations.keys()),
    command=change_language,
)

language_menu.set(LANGUAGE)
language_menu.pack(pady=10)


# Appearance Settings

appearance_label = ctk.CTkLabel(settings_page, text=t("appearance"), font=(UI_FONT, 16))
appearance_label.pack(pady=(20, 6))


appearance_help_label = ctk.CTkLabel(
    settings_page,
    text="Choose the application theme",
    font=(UI_FONT, 14),
)
appearance_help_label.pack(pady=(0, 12))


appearance_menu = ctk.CTkOptionMenu(
    settings_page,
    values=[
        "Dark",
        "Light",
        "System",
    ],
    command=change_appearance,
)

appearance_menu.set(APPEARANCE)
appearance_menu.pack(pady=10)

# Help Section

help_title_label = ctk.CTkLabel(settings_page, text=t("help_title"), font=(UI_FONT, 16))
help_title_label.pack(pady=(25, 8))


help_text_box = ctk.CTkTextbox(settings_page, width=650, height=220, font=(UI_FONT, 13))

help_text_box.pack(pady=10)

help_text_box.insert("0.0", t("help_text"))

help_text_box.configure(state="disabled")

# =========================================================
# REFRESH LANGUAGE
# =========================================================


def refresh_language():
    app.title(t("title"))

    appearance_label.configure(text="Appearance")
    appearance_help_label.configure(text=t("appearance_help"))
    home_title_label.configure(text=t("home_title"))
    home_subtitle_label.configure(text=t("home_subtitle"))

    file_page_title_label.configure(text=t("file_tools_title"))
    browse_hkx_button.configure(text=t("browse_hkx"))
    duplicate_desc_label.configure(text=t("duplicate_desc"))
    duplicate_button.configure(text=t("duplicate_btn"))
    attack_desc_label.configure(text=t("attack_desc"))
    attack_button.configure(text=t("attack_btn"))
    power_desc_label.configure(text=t("power_desc"))
    power_button.configure(text=t("power_btn"))

    merge_page_title_label.configure(text=t("merge_tools_title"))
    merge_select_a_button.configure(text=t("merge_select_a"))
    merge_a_start_label.configure(text=t("merge_a_start"))
    merge_a_end_label.configure(text=t("merge_a_end"))
    merge_select_b_button.configure(text=t("merge_select_b"))
    merge_b_start_label.configure(text=t("merge_b_start"))
    merge_b_end_label.configure(text=t("merge_b_end"))
    merge_output_button.configure(text=t("select_output"))
    merge_button.configure(text=t("merge_btn"))

    reverse_page_title_label.configure(text=t("reverse_tools_title"))
    reverse_help_label.configure(text=t("reverse_help"))
    reverse_select_button.configure(text=t("reverse_select"))
    reverse_output_label.configure(text=t("reverse_output_label"))
    reverse_output_button.configure(text=t("reverse_output_btn"))
    reverse_button.configure(text=t("reverse_btn"))

    scale_page_title_label.configure(text=t("scale_tools_title"))
    scale_help_label.configure(text=t("scale_help"))
    scale_select_button.configure(text=t("scale_select"))
    scale_ratio_label.configure(text=t("scale_ratio_label"))
    scale_output_label.configure(text=t("scale_output_label"))
    scale_output_button.configure(text=t("scale_output_btn"))
    scale_button.configure(text=t("scale_btn"))

    settings_title_label.configure(text=t("settings"))
    settings_help_label.configure(text=t("language_help"))
    language_label.configure(text=t("language"))

    home_nav_button.configure(text=t("nav_home"))
    merge_nav_button.configure(text=t("nav_merge"))
    reverse_nav_button.configure(text=t("nav_reverse"))
    scale_nav_button.configure(text=t("nav_scale"))
    file_nav_button.configure(text=t("nav_file"))
    settings_nav_button.configure(text=t("nav_settings"))

    appearance_menu.configure(
        values=[
            t("theme_dark"),
            t("theme_light"),
            t("theme_system"),
        ]
    )
    # Refresh currently selected appearance text
    appearance_translated = {
        "Dark": t("theme_dark"),
        "Light": t("theme_light"),
        "System": t("theme_system"),
    }

    appearance_menu.set(appearance_translated.get(APPEARANCE, t("theme_dark")))

    help_title_label.configure(text=t("help_title"))

    help_text_box.configure(state="normal")
    help_text_box.delete("0.0", "end")
    help_text_box.insert("0.0", t("help_text"))
    help_text_box.configure(state="disabled")


# =========================================================
# SIDEBAR
# =========================================================

sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="HKX\nToolkit", font=(UI_FONT, 28, "bold")).pack(pady=40)

home_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_home"), command=lambda: show_page(home_page)
)
home_nav_button.pack(pady=8)

merge_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_merge"), command=lambda: show_page(merge_page)
)
merge_nav_button.pack(pady=8)

reverse_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_reverse"), command=lambda: show_page(reverse_page)
)
reverse_nav_button.pack(pady=8)

scale_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_scale"), command=lambda: show_page(scale_page)
)
scale_nav_button.pack(pady=8)

file_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_file"), command=lambda: show_page(file_page)
)
file_nav_button.pack(pady=8)

settings_nav_button = ctk.CTkButton(
    sidebar, text=t("nav_settings"), command=lambda: show_page(settings_page)
)
settings_nav_button.pack(pady=8)

# =========================================================
# LOG / STATUS
# =========================================================

log_box = ctk.CTkTextbox(app, height=120)
log_box.pack(side="bottom", fill="x", padx=10)
log_box.configure(state="disabled")

status = ctk.CTkLabel(app, text=t("ready"), anchor="w")
status.pack(side="bottom", fill="x")

# Initial language refresh
refresh_language()

show_page(home_page)
log("HKX Toolkit initialized")
app.mainloop()
