import argparse
import json
import pathlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import algorithms.backtracking as backtracking
import algorithms.Forward_Checking as forward_checking
import algorithms.ac3 as ac3
import algorithms.min_conflicts as min_conflicts
from matplotlib.widgets import Button, Slider

ROOT = pathlib.Path(__file__).resolve().parent
GEOJSON_PATH = ROOT / "python.geojson"
TOPOJSON_PATH = ROOT / "DATA" / "Wards.json"

def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_polygons_from_geojson(feature):
    geom = feature.get("geometry", {})
    geom_type = geom.get("type")
    coords = geom.get("coordinates", [])
    if geom_type == "Polygon":
        return [coords]
    if geom_type == "MultiPolygon":
        return coords
    return []


def get_geojson_name_key(features):
    if not features:
        return None
    props = features[0].get("properties", {})
    candidates = ["Tỉnh thành mới", "Tên", "name", "TT hành chính"]
    for key in candidates:
        if key in props:
            return key
    return next(iter(props.keys()), None)


COLOR_NAME_MAP = {
    "red": (0.9, 0.35, 0.35, 0.8),
    "green": (0.35, 0.8, 0.35, 0.8),
    "blue": (0.35, 0.45, 0.9, 0.8),
    "yellow": (0.95, 0.85, 0.35, 0.8),
    "purple": (0.7, 0.4, 0.9, 0.8),
    "orange": (0.95, 0.55, 0.15, 0.8),
}

DEFAULT_REGION_COLOR = (0.8, 0.8, 0.8, 0.3)
HIGHLIGHT_COLORS = list(COLOR_NAME_MAP.values())


def draw_geojson_colored(ax, data, region_colors, default_color=(0.8, 0.8, 0.8, 0.3)):
    name_key = get_geojson_name_key(data.get("features", []))
    patches = []
    facecolors = []
    for feature in data.get("features", []):
        if not name_key:
            break
        name = feature.get("properties", {}).get(name_key)
        color_name = region_colors.get(name)
        facecolor = COLOR_NAME_MAP.get(color_name, default_color)
        for polygon in extract_polygons_from_geojson(feature):
            if not polygon:
                continue
            patches.append(Polygon(polygon[0], closed=True))
            facecolors.append(facecolor)
    collection = PatchCollection(
        patches,
        facecolor=facecolors,
        edgecolor=(0.2, 0.2, 0.2, 0.8),
        linewidths=0.5,
    )
    ax.add_collection(collection)


def decode_topojson_arc(arc_id, arcs):
    if arc_id < 0:
        arc_id = ~arc_id
        arc = list(reversed(arcs[arc_id]))
    else:
        arc = arcs[arc_id]
    return arc


def extract_polygons_from_topojson_geometry(geometry, arcs):
    geom_type = geometry.get("type")
    arc_groups = geometry.get("arcs", [])
    if geom_type != "Polygon":
        return []
    rings = []
    for ring_arcs in arc_groups:
        points = []
        for arc_id in ring_arcs:
            arc = decode_topojson_arc(arc_id, arcs)
            if points and arc and points[-1] == arc[0]:
                points.extend(arc[1:])
            else:
                points.extend(arc)
        rings.append(points)
    return [rings]


def polygon_patch(rings, **kwargs):
    patch = Polygon(rings[0], closed=True, **kwargs)
    return patch


def draw_geojson(ax, data):
    patches = []
    for feature in data.get("features", []):
        for polygon in extract_polygons_from_geojson(feature):
            if not polygon:
                continue
            patches.append(Polygon(polygon[0], closed=True))
    collection = PatchCollection(
        patches,
        facecolor=(0.2, 0.5, 0.9, 0.25),
        edgecolor=(0.1, 0.2, 0.4, 0.9),
        linewidths=0.6,
        label="python.geojson",
    )
    ax.add_collection(collection)


def draw_topojson(ax, data, facecolor=(0.9, 0.8, 0.2, 0.1), edgecolor=(0.8, 0.3, 0.0, 0.9), linewidths=0.8, region_colors=None):
    arcs = data.get("arcs", [])
    patches = []
    colors = []
    for geometry in data.get("objects", {}).get("collection", {}).get("geometries", []):
        if geometry.get("type") != "Polygon":
            continue
        name = geometry.get("properties", {}).get("Tên") or geometry.get("properties", {}).get("name") or "Unknown"
        polygons = extract_polygons_from_topojson_geometry(geometry, arcs)
        patch_color = region_colors.get(name, facecolor) if region_colors else facecolor
        for polygon in polygons:
            patches.append(Polygon(polygon[0], closed=True))
            colors.append(patch_color)
    collection = PatchCollection(
        patches,
        facecolor=colors,
        edgecolor=edgecolor,
        linewidths=linewidths,
        label="Wards.json",
    )
    ax.add_collection(collection)


def load_solution_file(path):
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file giải pháp: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("File giải pháp phải là một object JSON mapping vùng -> màu")
    return data


def build_interactive_topojson(ax, data, region_colors=None, default_color=DEFAULT_REGION_COLOR, edgecolor=(0.2, 0.2, 0.2, 0.7), linewidths=0.4):
    arcs = data.get("arcs", [])
    patches = []
    for geometry in data.get("objects", {}).get("collection", {}).get("geometries", []):
        if geometry.get("type") != "Polygon":
            continue
        name = geometry.get("properties", {}).get("Tên") or geometry.get("properties", {}).get("name") or "Unknown"
        polygons = extract_polygons_from_topojson_geometry(geometry, arcs)
        for polygon in polygons:
            initial_color = region_colors.get(name, default_color) if region_colors else default_color
            patch = Polygon(
                polygon[0],
                closed=True,
                facecolor=initial_color,
                edgecolor=edgecolor,
                linewidth=linewidths,
                picker=True,
            )
            patch.region_name = name
            if name in (region_colors or {}):
                patch.color_index = list(COLOR_NAME_MAP.values()).index(initial_color) if initial_color in COLOR_NAME_MAP.values() else -1
            else:
                patch.color_index = -1
            ax.add_patch(patch)
            patches.append(patch)
    return patches


def get_topojson_bounds(data, margin_ratio=0.02):
    arcs = data.get("arcs", [])
    all_x = []
    all_y = []
    for geometry in data.get("objects", {}).get("collection", {}).get("geometries", []):
        if geometry.get("type") != "Polygon":
            continue
        for polygon in extract_polygons_from_topojson_geometry(geometry, arcs):
            for x, y in polygon[0]:
                all_x.append(x)
                all_y.append(y)
    if not all_x or not all_y:
        return None
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    dx = (max_x - min_x) * margin_ratio
    dy = (max_y - min_y) * margin_ratio
    return min_x - dx, max_x + dx, min_y - dy, max_y + dy


def parse_args():
    parser = argparse.ArgumentParser(description="Hiển thị bản đồ Wards.json với UI và kết quả thuật toán tô màu")
    parser.add_argument(
        "--solution-file",
        help="Đường dẫn tới file JSON chứa mapping region -> color để hiển thị kết quả thuật toán",
        default=None,
    )
    parser.add_argument(
        "--solve",
        action="store_true",
        help="Sử dụng thuật toán CSP để tính giải pháp và hiển thị kết quả cuối cùng",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="Chạy thuật toán CSP từng bước và cập nhật bản đồ theo tiến trình",
    )
    parser.add_argument(
        "--step-delay",
        type=float,
        default=0.5,
        help="Khoảng thời gian dừng giữa các bước khi animate (giây)",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Cho phép click đổi màu các vùng trên bản đồ",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    topojson_data = load_json(TOPOJSON_PATH)

    region_colors = None
    if args.solution_file:
        region_colors = load_solution_file(args.solution_file)

    bounds = get_topojson_bounds(topojson_data, margin_ratio=0.03)
    if bounds is None:
        raise ValueError("Không tìm thấy dữ liệu phường từ Wards.json")

    # reduce total figure width/height by roughly 3cm each side
    fig, ax = plt.subplots(figsize=(12.8, 10.8))
    # maximize the window while keeping the window decorations and close button
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state('zoomed')
    except Exception:
        try:
            manager.window.showMaximized()
        except Exception:
            pass
    # shift map further left to avoid overlap with controls
    plt.subplots_adjust(bottom=0.12, left=0.0, right=0.60, top=0.98)
    x0, x1, y0, y1 = bounds
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal", adjustable="box")

    region_patches = build_interactive_topojson(
        ax,
        topojson_data,
        region_colors=region_colors,
        edgecolor=(0.2, 0.2, 0.2, 0.7),
        linewidths=0.4,
    )

    patch_by_region = {}
    for patch in region_patches:
        patch_by_region.setdefault(patch.region_name, []).append(patch)

    def update_patch_colors(assignment):
        for region, patches in patch_by_region.items():
            if region in assignment:
                color = COLOR_NAME_MAP.get(assignment[region], DEFAULT_REGION_COLOR)
            else:
                color = DEFAULT_REGION_COLOR
            for patch in patches:
                patch.set_facecolor(color)

    selected_label = ax.text(
        0.02,
        0.98,
        "Hiển thị kết quả thuật toán.",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=12,
        color="black",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )
    selected_algorithm = ["backtracking"]
    algorithm_mode_label = fig.text(
        0.02,
        0.24,
        "Thuật toán: Backtracking",
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )
    running = [False]
    step_counter = [0]
    logs = []
    MAX_LOG_LINES = 200
    auto_scroll = [True]  # track auto-scroll state like in frontend.py

    def update_algorithm_label():
        labels = {
            "backtracking": "Thuật toán: Backtracking",
            "forward_checking": "Thuật toán: Forward Checking",
            "ac3": "Thuật toán: AC-3",
            "min_conflicts": "Thuật toán: Min-Conflicts"
        }
        algorithm_mode_label.set_text(labels.get(selected_algorithm[0], "Unknown"))

    def select_algorithm(name):
        selected_algorithm[0] = name
        update_algorithm_label()
        algo_names = {
            "backtracking": "Backtracking",
            "forward_checking": "Forward Checking",
            "ac3": "AC-3",
            "min_conflicts": "Min-Conflicts"
        }
        append_log(f"Chọn thuật toán: {algo_names.get(name, 'Unknown')}")
        fig.canvas.draw_idle()

    def create_solver():
        if selected_algorithm[0] == "forward_checking":
            return forward_checking.solve_map_coloring_steps(
                path=str(TOPOJSON_PATH), colors=["red", "green", "blue", "yellow"]
            )
        elif selected_algorithm[0] == "ac3":
            return ac3.solve_map_coloring_steps(
                path=str(TOPOJSON_PATH), colors=["red", "green", "blue", "yellow"]
            )
        elif selected_algorithm[0] == "min_conflicts":
            return min_conflicts.solve_map_coloring_steps(
                path=str(TOPOJSON_PATH), colors=["red", "green", "blue", "yellow"]
            )
        return backtracking.solve_map_coloring_steps(
            path=str(TOPOJSON_PATH), colors=["red", "green", "blue", "yellow"]
        )

    solver_ref = [create_solver()]

    ax_algo_backtracking = plt.axes([0.02, 0.18, 0.18, 0.04])
    ax_algo_ac3 = plt.axes([0.02, 0.13, 0.18, 0.04])
    ax_algo_forward_checking = plt.axes([0.02, 0.08, 0.18, 0.04])
    ax_algo_min_conflicts = plt.axes([0.02, 0.03, 0.18, 0.04])

    btn_algo_backtracking = Button(ax_algo_backtracking, "Backtracking")
    btn_algo_ac3 = Button(ax_algo_ac3, "AC-3")
    btn_algo_forward_checking = Button(ax_algo_forward_checking, "Forward Check")
    btn_algo_min_conflicts = Button(ax_algo_min_conflicts, "Min-Conflicts")

    for b in (btn_algo_backtracking, btn_algo_ac3, btn_algo_forward_checking, btn_algo_min_conflicts):
        try:
            b.label.set_fontsize(9)
        except Exception:
            pass

    btn_algo_backtracking.on_clicked(lambda event: select_algorithm("backtracking"))
    btn_algo_ac3.on_clicked(lambda event: select_algorithm("ac3"))
    btn_algo_forward_checking.on_clicked(lambda event: select_algorithm("forward_checking"))
    btn_algo_min_conflicts.on_clicked(lambda event: select_algorithm("min_conflicts"))

# tạo timer nhưng CHƯA start
    timer = fig.canvas.new_timer(interval=int(args.step_delay * 1000))

    def append_log(line):
        # append new line and trim overall log size for memory
        logs.append(line)
        if len(logs) > MAX_LOG_LINES * 3:
            # keep some history but avoid unbounded growth
            del logs[0: len(logs) - MAX_LOG_LINES * 2]

        # update slider visibility
        try:
            update_slider_visibility()
        except Exception:
            pass

        # if auto_scroll is on, move slider to bottom so view auto-scrolls
        if auto_scroll[0]:
            try:
                if 'SLIDER_IS_VERTICAL' in globals() and SLIDER_IS_VERTICAL:
                    slider.set_val(0.0)
                else:
                    slider.set_val(1.0)
            except Exception:
                pass
        # refresh display according to slider position
        try:
            refresh_log_display()
        except Exception:
            # fallback: display last LOG_WINDOW_LINES lines
            visible = logs[-LOG_WINDOW_LINES:]
            try:
                log_text.set_text("\n".join(visible))
            except Exception:
                pass
            fig.canvas.draw_idle()

    def update():
        if not running[0]:
            return

        try:
            step = next(solver_ref[0])
            step_counter[0] += 1
            assignment = step.get("assignment", {})

            update_patch_colors(assignment)

            if step.get("action") == "assign":
                msg = f"Bước {step_counter[0]}: {step['var']} → {step['value']}"
                selected_label.set_text(msg)
                append_log(msg)

            elif step.get("action") == "remove":
                msg = f"Bước {step_counter[0]}: Backtrack {step['var']}"
                selected_label.set_text(msg)
                append_log(msg)

            elif step.get("action") == "goal":
                msg = "Đã tìm thấy lời giải CSP"
                selected_label.set_text(msg)
                append_log(msg)
                running[0] = False
                timer.stop()

            elif step.get("action") == "constraint_failed":
                msg = step.get("message", "Thuật toán thất bại")
                selected_label.set_text(msg)
                append_log(msg)
                running[0] = False
                timer.stop()

            fig.canvas.draw_idle()

        except StopIteration:
            running[0] = False
            msg = "Thuật toán hoàn tất"
            selected_label.set_text(msg)
            append_log(msg)
            timer.stop()

    timer.add_callback(update)

    def start_cb(event):
        solver_ref[0] = create_solver()
        step_counter[0] = 0
        for patch in region_patches:
            patch.set_facecolor(DEFAULT_REGION_COLOR)
            patch.color_index = -1
        logs.clear()
        auto_scroll[0] = True
        try:
            update_slider_visibility()
        except Exception:
            pass
        append_log("Start: solver reset and started")
        algo_names = {
            "backtracking": "Backtracking",
            "forward_checking": "Forward Checking",
            "ac3": "AC-3",
            "min_conflicts": "Min-Conflicts"
        }
        selected_label.set_text(f"Thuật toán {algo_names.get(selected_algorithm[0], 'CSP')} đang chạy...")
        running[0] = True
        timer.start()

    def continue_cb(event):
        if not running[0]:
            running[0] = True
            append_log("Continue")
            selected_label.set_text("Tiếp tục chạy thuật toán CSP...")
            timer.start()

    def stop_cb(event):
        if running[0]:
            running[0] = False
            append_log("Stop")
            selected_label.set_text("Thuật toán đã dừng")
            timer.stop()

    def reset_cb(event):
        running[0] = False
        timer.stop()
        solver_ref[0] = create_solver()
        step_counter[0] = 0
        for patch in region_patches:
            patch.set_facecolor(DEFAULT_REGION_COLOR)
            patch.color_index = -1
        logs.clear()
        auto_scroll[0] = True
        try:
            update_slider_visibility()
        except Exception:
            pass
        append_log("Reset: solver and map cleared")
        selected_label.set_text("Đã reset trạng thái và xóa log")
        fig.canvas.draw_idle()

    # Buttons: vertical column in top-right
    ax_start = plt.axes([0.84, 0.94, 0.10, 0.04])
    ax_continue = plt.axes([0.84, 0.88, 0.10, 0.04])
    ax_stop = plt.axes([0.84, 0.82, 0.10, 0.04])
    ax_reset = plt.axes([0.84, 0.76, 0.10, 0.04])

    btn_start = Button(ax_start, "Start")
    btn_continue = Button(ax_continue, "Continue")
    btn_stop = Button(ax_stop, "Stop")
    btn_reset = Button(ax_reset, "Reset")

    # reduce label font size so buttons look compact
    for b in (btn_start, btn_continue, btn_stop, btn_reset):
        try:
            b.label.set_fontsize(9)
        except Exception:
            pass

    btn_start.on_clicked(start_cb)
    btn_continue.on_clicked(continue_cb)
    btn_stop.on_clicked(stop_cb)
    btn_reset.on_clicked(reset_cb)

    # Log area: 7 cm width, 12 cm height, extended 3 cm each side, moved down 3 cm
    cm_to_in = 0.393700787
    fig_width_in = fig.get_size_inches()[0]
    fig_height_in = fig.get_size_inches()[1]
    
    # 7 cm width
    log_width_cm = 7.0
    log_width_frac = log_width_cm * cm_to_in / fig_width_in
    
    # 12 cm height, extend down (not up to cover buttons)
    log_height_cm = 12.0
    log_height_frac = log_height_cm * cm_to_in / fig_height_in
    
    # Left expansion: 3 cm
    left_expand_cm = 3.0
    left_expand_frac = left_expand_cm * cm_to_in / fig_width_in
    
    # Calculate new left position
    log_left = 0.84 - left_expand_frac
    
    # Move down 3 cm from original position, plus additional 5 cm to move away from reset button (3cm + 2cm more)
    down_shift_cm = 8.0
    down_shift_frac = down_shift_cm * cm_to_in / fig_height_in
    
    # Extend down 5 cm more to make room for 12 cm height
    extend_down_cm = 5.0
    extend_down_frac = extend_down_cm * cm_to_in / fig_height_in
    
    log_bottom = 0.70 - down_shift_frac - extend_down_frac

    ax_log = plt.axes([log_left, log_bottom, log_width_frac, log_height_frac])
    ax_log.set_facecolor((0.95, 0.95, 0.95, 1.0))
    ax_log.spines["top"].set_visible(True)
    ax_log.spines["right"].set_visible(True)
    ax_log.spines["bottom"].set_visible(True)
    ax_log.spines["left"].set_visible(True)
    ax_log.patch.set_edgecolor("black")
    ax_log.patch.set_linewidth(1.0)
    ax_log.set_xticks([])
    ax_log.set_yticks([])
    ax_log.set_title("Log", pad=6, fontsize=10)
    log_text = ax_log.text(0.01, 0.95, "", va="top", family="monospace", fontsize=8, wrap=True)
    ax_log.set_xlim(0, 1)
    ax_log.set_ylim(0, 1)

    # hide the axes box ticks labels only
    ax_log.xaxis.set_visible(False)
    ax_log.yaxis.set_visible(False)

    # Vertical slider for log scrolling (to the right of the log box)
    slider_gap = 0.002
    slider_width = 0.015
    slider_left = log_left + log_width_frac + slider_gap
    ax_slider = plt.axes([slider_left, log_bottom, slider_width, log_height_frac])
    # Use vertical slider. By convention in this UI we'll treat slider.val==0.0 as "bottom" (newest logs).
    SLIDER_IS_VERTICAL = True
    slider = Slider(ax_slider, "", 0.0, 1.0, valinit=0.0, orientation="vertical")

    # number of visible lines in the log window
    LOG_WINDOW_LINES = 25  # increased for larger 12cm height
    # internal start index (0-based) for the visible window
    log_start = [0]

    def refresh_log_display():
        # compute start index from slider value in [0,1]
        total = len(logs)
        if total <= LOG_WINDOW_LINES:
            start = 0
        else:
            max_start = total - LOG_WINDOW_LINES
            # For horizontal slider: val 0 -> top, 1 -> bottom
            # For vertical slider we display with val 0 -> bottom (newest), val 1 -> top
            if 'SLIDER_IS_VERTICAL' in globals() and SLIDER_IS_VERTICAL:
                frac = 1.0 - slider.val
            else:
                frac = slider.val
            start = int(round(frac * max_start))
        log_start[0] = start
        visible = logs[start:start + LOG_WINDOW_LINES]
        log_text.set_text("\n".join(visible))
        fig.canvas.draw_idle()

    # show or hide slider based on whether there are more lines than the window
    def update_slider_visibility():
        try:
            if len(logs) <= LOG_WINDOW_LINES:
                ax_slider.set_visible(False)
            else:
                ax_slider.set_visible(True)
        except Exception:
            pass

    def on_slider(val):
        # when slider moves manually, detect if user is at bottom
        if 'SLIDER_IS_VERTICAL' in globals() and SLIDER_IS_VERTICAL:
            # vertical slider: val <= 0.02 means near bottom (newest logs)
            if slider.val <= 0.02:
                auto_scroll[0] = True
            else:
                auto_scroll[0] = False
        else:
            # horizontal slider: val >= 0.98 means near bottom
            if slider.val >= 0.98:
                auto_scroll[0] = True
            else:
                auto_scroll[0] = False
        refresh_log_display()

    slider.on_changed(on_slider)

    def on_pick(event):
        if not args.interactive:
            return
        artist = event.artist
        if not isinstance(artist, Polygon):
            return
        if not hasattr(artist, "region_name"):
            return

        current_index = getattr(artist, "color_index", -1)
        next_index = current_index + 1
        if next_index >= len(HIGHLIGHT_COLORS):
            artist.set_facecolor(DEFAULT_REGION_COLOR)
            artist.color_index = -1
            selected_label.set_text(f"Bỏ chọn: {artist.region_name}")
        else:
            artist.set_facecolor(HIGHLIGHT_COLORS[next_index])
            artist.color_index = next_index
            color_name = list(COLOR_NAME_MAP.keys())[next_index]
            selected_label.set_text(f"Chọn: {artist.region_name} → {color_name}")

        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("pick_event", on_pick)

    if args.animate:
        title = "Bản đồ Wards HCMC - Thuật toán CSP từng bước"
    elif args.solution_file or args.solve:
        title = "Bản đồ Wards HCMC - Hiển thị kết quả thuật toán"
    elif args.interactive:
        title = "Bản đồ Wards HCMC - Tương tác đổi màu"
    else:
        title = "Bản đồ Wards HCMC - Màu mặc định"
    # đặt tiêu đề cao hơn và có khoảng đệm để tránh bị che
    ax.set_title(title, pad=20)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle="--", alpha=0.2)
    ax.tick_params(axis="both", which="major", labelsize=10)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, linestyle="--", alpha=0.2)
    ax.tick_params(axis="both", which="major", labelsize=10)

    legend_handles = [Patch(facecolor=COLOR_NAME_MAP[c], edgecolor=(0.2,0.2,0.2,0.8), label=c) for c in ["red","green","blue","yellow"]]
    # vẽ legend ở tọa độ figure (bên ngoài axes) để không che tiêu đề
    fig.legend(handles=legend_handles, title="Màu", loc="upper left", bbox_to_anchor=(0.02, 0.92), bbox_transform=fig.transFigure)

    plt.tight_layout()
    output_path = ROOT / "map_output.png"
    fig.savefig(output_path, dpi=200)
    print(f"Map created and saved to: {output_path}")
    plt.show()


if __name__ == "__main__":
    main()
