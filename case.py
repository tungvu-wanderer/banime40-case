"""Parametric 2-piece case for the banime40 v2.0 PCB.

Frame: switch-side (typing) view, x right, y up, origin at the PCB's
bottom-left corner, z up from the bottom of the tray. All exposed flat faces
are multiples of the 0.2 mm layer height.

    uv run python case.py          # writes build/
"""
from pathlib import Path

import cadquery as cq

# --- PCB ---------------------------------------------------------------
PITCH = 19.05
COLS, ROWS = 10, 4
PCB_W, PCB_H, PCB_R = COLS * PITCH, ROWS * PITCH, 1.6
PCB_T = 1.6

# --- height stack (z up from tray bottom) ------------------------------
FLOOR = 1.2            # under the Pro Micro
FLOOR_MAIN = 2.0       # everywhere else
TRAY_H = 10.6          # floor + clearance + PCB front parts, up to PCB back face
PLATE_T = 1.6
PLATE_TOP_TO_PCB = 5.15
TOP_H = 5.2            # plate + skirt down to the seam
TOTAL_H = TRAY_H + TOP_H
PLATE_BOT = TOTAL_H - PLATE_T
PCB_FRONT_Z = TRAY_H - PCB_T

# --- walls / seam ------------------------------------------------------
CLEAR = 0.3            # PCB to inner wall
WALL = 1.6
OUT = CLEAR + WALL     # PCB edge to outer wall
LAP_Z = 2.0            # lap joint depth
TONGUE_OFF = 1.05      # tray tongue spans offsets CLEAR..TONGUE_OFF
LIP_OFF = 1.2          # top lip spans offsets LIP_OFF..OUT
LIP_Z_GAP = 0.2

# --- switch hole (from the stock plate) --------------------------------
HOLE = 14.2
NOTCH_W, NOTCH_H = 15.8, 3.3
NOTCH_Y = 4.45          # notch centre above/below the hole centre

# --- pillars: M2 standoff (O3.15) clamped by two bolts ------------------
POCKET_D = 3.4
BOLT_D = 2.5
HEAD_D = 4.15                 # bolt heads sit proud on the flat outer faces
FLOOR_UNDER_HEAD = 2.0        # solid between each outer face and the standoff pocket
PILLAR_C = POCKET_D / 2 + CLEAR + 0.8   # pillar centre beyond the PCB edge
PILLAR_WALL = POCKET_D / 2 + 1.2        # material from pillar centre to outer face
LONG_OUT = PILLAR_C + PILLAR_WALL       # PCB edge to outer face on the long edges
PILLAR_X = [5.0, PCB_W / 2, PCB_W - 5.0]
PILLARS = [(x, y) for x in PILLAR_X for y in (-PILLAR_C, PCB_H + PILLAR_C)]
LIP_GAP_XY = 0.15

# --- USB-C -------------------------------------------------------------
USB_Y = PCB_H - 28.3
USB_W, USB_TOP = 13.0, 7.2
RECESS_X1, RECESS_HALF_Y = 34.5, 10.5   # thin-floor area under the Pro Micro

OUT_DIR = Path(__file__).parent / "build"


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def cyl(x, y, r, z0, z1):
    return (cq.Workplane("XY").workplane(offset=z0).center(x, y)
            .circle(r).extrude(z1 - z0))


def rrect(off, z0, z1):
    """PCB outline grown by `off`, extruded z0..z1."""
    return (box(-off, PCB_W + off, -off, PCB_H + off, z0, z1)
            .edges("|Z").fillet(PCB_R + off))


def outline(z0, z1):
    """Outer shape: solid, flush long-edge walls that carry the pillars."""
    return (box(-OUT, PCB_W + OUT, -LONG_OUT, PCB_H + LONG_OUT, z0, z1)
            .edges("|Z").fillet(PCB_R + OUT))


def pillar_guard(z0, z1):
    """Keeps the lap joint away from the pillars."""
    out = None
    for x, y in PILLARS:
        c = cyl(x, y, POCKET_D / 2 + 0.8, z0, z1)
        out = c if out is None else out.union(c)
    return out


def key_centres():
    return [(PITCH / 2 + PITCH * i, PITCH / 2 + PITCH * j)
            for i in range(COLS) for j in range(ROWS)]


def switch_hole(cx, cy):
    z0, z1 = PLATE_BOT - 0.1, TOTAL_H + 0.1
    h = HOLE / 2
    cut = box(cx - h, cx + h, cy - h, cy + h, z0, z1)
    for s in (1, -1):
        y_mid = cy + s * NOTCH_Y
        cut = cut.union(box(cx - NOTCH_W / 2, cx + NOTCH_W / 2,
                            y_mid - NOTCH_H / 2, y_mid + NOTCH_H / 2, z0, z1))
    return cut


def pillar_cuts(z_lo, z_hi, pocket_lo, pocket_hi):
    """Standoff pocket and bolt hole for the pillars in one half (z_lo/z_hi bound the half)."""
    out = None
    for x, y in PILLARS:
        if z_lo == 0:      # tray: bolt hole through the floor
            hole = cyl(x, y, BOLT_D / 2, -0.1, pocket_lo + 0.1)
        else:              # top: bolt hole through the plate side
            hole = cyl(x, y, BOLT_D / 2, pocket_hi - 0.1, z_hi + 0.1)
        for p in (cyl(x, y, POCKET_D / 2, pocket_lo, pocket_hi), hole):
            out = p if out is None else out.union(p)
    return out


def build_tray():
    body = outline(0, TRAY_H).cut(rrect(CLEAR, FLOOR_MAIN, TRAY_H + 1))
    # thin the floor under the Pro Micro, which hangs down to FLOOR + 0.35
    recess = box(-CLEAR, RECESS_X1, USB_Y - RECESS_HALF_Y, USB_Y + RECESS_HALF_Y,
                 FLOOR, FLOOR_MAIN + 0.1)
    body = body.cut(recess)
    z0 = TRAY_H - LAP_Z
    # rabbet for the top's lip; closed to the outside under the thick long edges
    rabbet = (rrect(OUT + 0.1, z0, TRAY_H + 0.1)
              .cut(rrect(TONGUE_OFF, z0 - 1, TRAY_H + 1))
              .cut(outline(z0 - 1, TRAY_H + 1).cut(rrect(OUT, z0 - 2, TRAY_H + 2)))
              .cut(pillar_guard(z0 - 1, TRAY_H + 1)))
    body = body.cut(rabbet)
    pocket_lo = FLOOR_UNDER_HEAD
    body = body.cut(pillar_cuts(0, TRAY_H, pocket_lo, TRAY_H + 0.1))
    usb = (box(-6, 0, USB_Y - USB_W / 2, USB_Y + USB_W / 2, -1, USB_TOP)
           .edges("|X and >Z").fillet(2.0))
    return body.cut(usb)


def build_top():
    body = outline(TRAY_H, TOTAL_H).cut(rrect(CLEAR, TRAY_H - 1, PLATE_BOT))
    z0 = TRAY_H - LAP_Z
    lip = (rrect(OUT, z0 + LIP_Z_GAP, TRAY_H)
           .cut(rrect(LIP_OFF, z0 - 1, TRAY_H + 1))
           .cut(pillar_guard(z0 - 1, TRAY_H + 1)))
    # keep a gap to the tray's outer wall where the long edges are thick
    for y0, y1 in ((-LONG_OUT, -OUT + LIP_GAP_XY), (PCB_H + OUT - LIP_GAP_XY, PCB_H + LONG_OUT)):
        lip = lip.cut(box(-OUT - 1, PCB_W + OUT + 1, y0, y1, z0 - 1, TRAY_H + 1))
    body = body.union(lip)
    for cx, cy in key_centres():
        body = body.cut(switch_hole(cx, cy))
    pocket_hi = TOTAL_H - FLOOR_UNDER_HEAD
    return body.cut(pillar_cuts(TRAY_H, TOTAL_H, TRAY_H - 0.1, pocket_hi))


def to_print_orientation(top):
    """Plate face on the bed."""
    return top.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, PCB_H, TOTAL_H))


def keepouts():
    """Envelopes of what lives inside the case, for interference checks."""
    pcb = rrect(0, PCB_FRONT_Z, TRAY_H)
    pro_micro = box(0, 32.5, USB_Y - 9, USB_Y + 9, FLOOR + 0.35, PCB_FRONT_Z)
    usb_shell = box(-0.5, 0, USB_Y - 4.5, USB_Y + 4.5, FLOOR + 0.35, FLOOR + 0.35 + 3.4)
    parts_zone = rrect(0, PCB_FRONT_Z - 1.95, PCB_FRONT_Z)   # sockets, diodes
    return pcb.union(pro_micro).union(usb_shell).union(parts_zone)


# Top-left corner (typing view): corner radius, pillar, lap joint, USB notch, 2x2 key holes.
COUPON = (-3, 38, 38, PCB_H + LONG_OUT + 1)


def build_coupon(part, region):
    x0, x1, y0, y1 = region
    return part.intersect(box(x0, x1, y0, y1, -1, TOTAL_H + 1))


def report(name, wp):
    s = wp.val()
    bb = s.BoundingBox()
    print(f"{name:6s} vol={s.Volume()/1000:7.2f} cm3  "
          f"bbox={bb.xlen:6.1f} x {bb.ylen:5.1f} x {bb.zlen:4.1f}  valid={s.isValid()}")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    tray, top = build_tray(), build_top()
    report("tray", tray)
    report("top", top)

    for a, b, label in [(tray, top, "tray/top"),
                        (tray, keepouts(), "tray/PCB+ProMicro"),
                        (top, keepouts(), "top/PCB+ProMicro")]:
        v = a.intersect(b).val().Volume()
        print(f"overlap {label:20s} {v:8.3f} mm3")

    cq.exporters.export(tray, str(OUT_DIR / "tray.stl"), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(to_print_orientation(top), str(OUT_DIR / "top.stl"),
                        tolerance=0.01, angularTolerance=0.1)
    c_tray, c_top = build_coupon(tray, COUPON), build_coupon(top, COUPON)
    report("cp/tray", c_tray)
    report("cp/top", c_top)
    cq.exporters.export(c_tray, str(OUT_DIR / "coupon_tray.stl"), tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(to_print_orientation(c_top), str(OUT_DIR / "coupon_top.stl"),
                        tolerance=0.01, angularTolerance=0.1)
    asm = cq.Assembly().add(tray, name="tray").add(top, name="top")
    asm.save(str(OUT_DIR / "case.step"))


if __name__ == "__main__":
    main()
