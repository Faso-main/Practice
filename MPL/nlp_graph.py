import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.lines as lines
from functools import wraps

def handle_plot_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in plotting: {str(e)}")
            plt.close('all')
            raise
    return wrapper

CONFIG = {
    'task_width': 2.5,
    'task_height': 1.0,
    'event_radius': 0.4,
    'pool_padding': 0.7,
    'lane_height': 1.0 + 2 * 0.7,
    'pool_vertical_padding': 1.5,
    'text_padding': 0.1,
    'pool1_y_center': 6.0,
    'gateway_size': 1.0
}

@handle_plot_errors
def create_bpmn_diagram():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    cfg = CONFIG
    pool2_y_center = cfg['pool1_y_center'] - cfg['lane_height'] - cfg['pool_vertical_padding']

    start_x = 1.0
    task1_x = start_x + cfg['event_radius'] + cfg['pool_padding'] + cfg['task_width'] / 2
    task2_x = task1_x + cfg['task_width'] / 2 + cfg['pool_padding'] + cfg['task_width'] / 2
    task3_x = task2_x + cfg['task_width'] / 2 + cfg['pool_padding'] + cfg['task_width'] / 2
    task4_x = task1_x
    end_x = task4_x + cfg['task_width']/2 + cfg['pool_padding'] + cfg['event_radius']
    gateway_x = task2_x + cfg['task_width'] / 2 + cfg['pool_padding'] + 0.5

    max_x_coord = max(end_x + cfg['event_radius'], task3_x + cfg['task_width']/2)
    min_x_coord = start_x - cfg['event_radius']
    pool_width = max_x_coord - min_x_coord + 2 * cfg['pool_padding']
    pool_start_x = min_x_coord - cfg['pool_padding']

    pool1_rect = patches.Rectangle((pool_start_x, cfg['pool1_y_center'] - cfg['lane_height'] / 2),
                                 pool_width, cfg['lane_height'], linewidth=1, edgecolor='black', facecolor='lightblue', alpha=0.3)
    ax.add_patch(pool1_rect)
    ax.text(pool_start_x + cfg['pool_padding'] / 2, cfg['pool1_y_center'], "Медицинский работник (Врач)",
            verticalalignment='center', horizontalalignment='left', rotation=90, fontsize=10, weight='bold')

    pool2_rect = patches.Rectangle((pool_start_x, pool2_y_center - cfg['lane_height'] / 2),
                                 pool_width, cfg['lane_height'], linewidth=1, edgecolor='black', facecolor='lightgreen', alpha=0.3)
    ax.add_patch(pool2_rect)
    ax.text(pool_start_x + cfg['pool_padding'] / 2, pool2_y_center, "Интеллектуальная система",
            verticalalignment='center', horizontalalignment='left', rotation=90, fontsize=10, weight='bold')

    start_event = patches.Circle((start_x, cfg['pool1_y_center']), cfg['event_radius'], linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(start_event)
    ax.text(start_x, cfg['pool1_y_center'], "Начало", ha='center', va='center', fontsize=8)

    end_event = patches.Circle((end_x, cfg['pool1_y_center']), cfg['event_radius'], linewidth=3, edgecolor='black', facecolor='white')
    ax.add_patch(end_event)
    ax.text(end_x, cfg['pool1_y_center'], "Конец", ha='center', va='center', fontsize=8)

    task1_rect = patches.FancyBboxPatch((task1_x - cfg['task_width']/2, cfg['pool1_y_center'] - cfg['task_height']/2), cfg['task_width'], cfg['task_height'],
                                   boxstyle="round,pad=0.1, rounding_size=0.2", linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(task1_rect)
    ax.text(task1_x, cfg['pool1_y_center'], "Загрузка/Ввод\nданных врачом", ha='center', va='center', fontsize=8)

    task2_rect = patches.FancyBboxPatch((task2_x - cfg['task_width']/2, pool2_y_center - cfg['task_height']/2), cfg['task_width'], cfg['task_height'],
                                   boxstyle="round,pad=0.1, rounding_size=0.2", linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(task2_rect)
    ax.text(task2_x, pool2_y_center, "Анализ данных\nсистемой (NLP, EDS)", ha='center', va='center', fontsize=8)

    task3_rect = patches.FancyBboxPatch((task3_x - cfg['task_width']/2, pool2_y_center - cfg['task_height']/2), cfg['task_width'], cfg['task_height'],
                                   boxstyle="round,pad=0.1, rounding_size=0.2", linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(task3_rect)
    ax.text(task3_x, pool2_y_center, "Формирование\nотчета", ha='center', va='center', fontsize=8)

    task4_rect = patches.FancyBboxPatch((task4_x - cfg['task_width']/2, cfg['pool1_y_center'] - cfg['task_height']/2), cfg['task_width'], cfg['task_height'],
                                   boxstyle="round,pad=0.1, rounding_size=0.2", linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(task4_rect)
    ax.text(task4_x, cfg['pool1_y_center'], "Просмотр и\nоценка отчета", ha='center', va='center', fontsize=8)

    gateway_points = [
        (gateway_x, pool2_y_center + cfg['gateway_size']/2),
        (gateway_x + cfg['gateway_size']/2, pool2_y_center),
        (gateway_x, pool2_y_center - cfg['gateway_size']/2),
        (gateway_x - cfg['gateway_size']/2, pool2_y_center),
        (gateway_x, pool2_y_center + cfg['gateway_size']/2)
    ]
    gateway_patch = patches.Polygon(gateway_points, linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(gateway_patch)
    ax.text(gateway_x, pool2_y_center, "X", ha='center', va='center', fontsize=10, weight='bold')
    ax.text(gateway_x, pool2_y_center - cfg['gateway_size']/2 - cfg['text_padding'], "Есть предупреждения?", ha='center', va='top', fontsize=8)

    arrow1 = patches.FancyArrowPatch((start_x + cfg['event_radius'], cfg['pool1_y_center']),
                                 (task1_x - cfg['task_width']/2, cfg['pool1_y_center']),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
    ax.add_patch(arrow1)

    arrow2 = patches.FancyArrowPatch((task1_x, cfg['pool1_y_center'] - cfg['task_height']/2),
                                 (task2_x, pool2_y_center + cfg['task_height']/2),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black', linestyle='--')
    ax.add_patch(arrow2)
    ax.text((task1_x + task2_x) / 2, (cfg['pool1_y_center'] - cfg['task_height']/2 + pool2_y_center + cfg['task_height']/2) / 2,
            "Медицинские данные", ha='center', va='bottom', fontsize=8)

    arrow3 = patches.FancyArrowPatch((task2_x + cfg['task_width']/2, pool2_y_center),
                                 (gateway_x - cfg['gateway_size']/2, pool2_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
    ax.add_patch(arrow3)

    arrow4 = patches.FancyArrowPatch((gateway_x + cfg['gateway_size']/2, pool2_y_center),
                                 (task3_x - cfg['task_width']/2, pool2_y_center),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
    ax.add_patch(arrow4)
    ax.text(gateway_x + cfg['gateway_size']/2 + cfg['text_padding'], pool2_y_center, "Нет", ha='left', va='center', fontsize=8)

    arrow5 = patches.FancyArrowPatch((task3_x + cfg['task_width']/2, pool2_y_center),
                                 (task3_x + cfg['task_width']/2 + cfg['pool_padding'], pool2_y_center),
                                 arrowstyle='-', mutation_scale=20, lw=1, color='black')
    ax.add_patch(arrow5)

    arrow6 = patches.FancyArrowPatch((task3_x, pool2_y_center + cfg['task_height']/2),
                                 (task4_x, cfg['pool1_y_center'] - cfg['task_height']/2),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black', linestyle='--')
    ax.add_patch(arrow6)
    ax.text((task3_x + task4_x) / 2, (pool2_y_center + cfg['task_height']/2 + cfg['pool1_y_center'] - cfg['task_height']/2) / 2,
            "Отчет с диагнозами и предупреждениями", ha='center', va='bottom', fontsize=8)

    arrow7 = patches.FancyArrowPatch((task4_x + cfg['task_width']/2, cfg['pool1_y_center']),
                                 (end_x - cfg['event_radius'], cfg['pool1_y_center']),
                                 arrowstyle='->', mutation_scale=20, lw=1, color='black')
    ax.add_patch(arrow7)

    data_input_x = (task1_x + task2_x) / 2
    data_input_y = (cfg['pool1_y_center'] - cfg['task_height']/2 + pool2_y_center + cfg['task_height']/2) / 2 - cfg['task_height']/2

    data_input_rect = patches.Rectangle((data_input_x - cfg['task_height']/4, data_input_y - cfg['task_height']/2), cfg['task_height']/2, cfg['task_height'], linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(data_input_rect)
    ax.text(data_input_x, data_input_y - cfg['task_height']/4, "Мед.\nданные", ha='center', va='center', fontsize=7)
    ax.add_line(lines.Line2D([task1_x, data_input_x], [cfg['pool1_y_center'] - cfg['task_height']/2, data_input_y], lw=1, color='black', linestyle=':'))
    ax.add_line(lines.Line2D([data_input_x, task2_x], [data_input_y, pool2_y_center + cfg['task_height']/2], lw=1, color='black', linestyle=':'))

    data_output_x = (task3_x + task4_x) / 2
    data_output_y = (pool2_y_center + cfg['task_height']/2 + cfg['pool1_y_center'] - cfg['task_height']/2) / 2 + cfg['task_height']/2

    data_output_rect = patches.Rectangle((data_output_x - cfg['task_height']/4, data_output_y - cfg['task_height']/2), cfg['task_height']/2, cfg['task_height'], linewidth=1, edgecolor='black', facecolor='white')
    ax.add_patch(data_output_rect)
    ax.text(data_output_x, data_output_y - cfg['task_height']/4, "Отчет", ha='center', va='center', fontsize=7)
    ax.add_line(lines.Line2D([task3_x, data_output_x], [pool2_y_center + cfg['task_height']/2, data_output_y - cfg['task_height']/2], lw=1, color='black', linestyle=':'))
    ax.add_line(lines.Line2D([data_output_x, task4_x], [data_output_y - cfg['task_height']/2, cfg['pool1_y_center'] - cfg['task_height']/2], lw=1, color='black', linestyle=':'))

    min_x = pool_start_x - cfg['pool_padding']
    max_x = pool_start_x + pool_width + cfg['pool_padding']
    min_y = pool2_y_center - cfg['lane_height'] / 2 - cfg['pool_padding']
    max_y = cfg['pool1_y_center'] + cfg['lane_height'] / 2 + cfg['pool_padding']

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    plt.title("BPMN диаграмма: Врач и ИИ-система поддержки диагностики")
    plt.show()

create_bpmn_diagram()