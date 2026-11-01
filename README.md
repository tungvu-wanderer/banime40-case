# banime40-case

Low-profile, two-piece, 3D-printed case for the [banime40](https://github.com/ChrisChrisLoLo/banime40) **v2.0** PCB. The plate is part of the top, and the PCB floats between the switches and the tray with no gasket and no PCB screws.

Printed and checked: the corner coupon pair and the full case both fit the real board.

    uv run python case.py     # writes build/

Outputs in `build/`:

| File | What |
|---|---|
| `tray.stl` | bottom piece, printed floor-down |
| `top.stl` | top piece with integrated plate, already flipped to print plate-face-down |
| `case.step` | both parts assembled, for viewing |
| `coupon_tray.stl`, `coupon_top.stl` | top-left corner test pair: pillar, lap joint, USB notch, 2x2 switch holes |

All dimensions live as constants at the top of `case.py`. The frame is the typing (switch-side) view: x right, y up, origin at the PCB's bottom-left corner, z up from the bottom of the tray.

## Measured inputs

Caliper measurements of the real board and hardware. Everything else is derived from these.

| Measurement | Value |
|---|---|
| PCB outline | 190.5 x 76.2 mm (10 x 4 keys at 19.05 mm pitch), corner radius 1.6 mm |
| PCB thickness | 1.6 mm |
| PCB back face to socket tops | 3.55 mm |
| PCB back face to top of Pro Micro + USB-C | 9.05 mm (Pro Micro on a header) |
| Plate top face to PCB back face | 5.15 mm (standard MX switch) |
| USB-C overhang past the PCB edge | 0.5 mm, on the left short edge seen from the switch side |
| USB-C centre | 28.3 mm below the top edge, seen from the switch side (row 2) |
| Brass standoff | round, O3.15 mm |
| Bolt head | O4.15 mm x 0.9 mm tall (flat head) |

Layout: 4x10 grid, all 40 positions populated. The PCB's six mounting holes, the reset button and the encoders are not used.

## Derived design values

| Value | Result | How |
|---|---|---|
| Tray height | 10.6 mm | 1.2 floor + 0.35 clearance + 9.05 |
| Top height | 5.2 mm | 1.6 plate + 3.6 skirt, so plate top is 5.15-5.2 mm above the PCB back face |
| Total height | 15.8 mm | |
| Outline | 194.3 x 87.6 mm | PCB + 0.3 clearance + 1.6 wall on the short ends; 5.7 mm flush wall on the long edges |
| Floor | 2.0 mm, 1.2 mm under the Pro Micro | recess is 34.5 mm from the left wall, +-10.5 mm around the USB centre |
| Plate | 1.6 mm | |
| Switch hole | 14.2 x 14.2 mm | stock plate, from `banime40/case/stl/Plate Final.stl` |
| Switch notches | 4 per hole, 15.8 mm wide hole at the notch, 3.3 mm tall, centred 4.45 mm above and below the hole centre | stock plate |
| USB notch | 13 mm wide, open to the bottom face, up to z = 7.2 mm | |
| Pillars | 6, at x = 5, 95.25, 185.5 mm on both long edges, 2.8 mm outside the PCB edge | |
| Pillar holes | bolt hole O2.5 mm through 2.0 mm solid on each face, standoff pocket O3.4 mm, 11.8 mm long | |

All exposed flat faces are multiples of the 0.2 mm layer height.

## Print settings

- PLA, 0.2 mm layers, 0.4 mm nozzle, sparse infill.
- No supports. The tray prints floor-down and the top plate-face-down, which is how the STLs are oriented.
- Bolt heads sit proud on the flat outer faces. There are no craters.

## Hardware

- 6 brass M2 female-female round standoffs, O3.15 mm, 12 mm long. The modelled pocket is 11.8 mm and a 12 mm standoff fits in the printed case.
- 12 M2 flat-head bolts, 2 per pillar, one from each face. M2x6 gives about 4 mm of thread in the standoff.
- Thin rubber feet for the underside. The bolt heads stand 0.9 mm below the bottom face.

## Assembly

1. Clip the switches into the top's plate holes and seat the PCB on their pins, with the sockets and Pro Micro facing down.
2. Drop each standoff into a tray pocket.
3. Close the halves. The top's lip drops into the tray's rabbet.
4. Thread a bolt from each face into each standoff, finger tight.

## Credits

Switch hole and notch dimensions are taken from the stock plate in [ChrisChrisLoLo/banime40](https://github.com/ChrisChrisLoLo/banime40), which is licensed CC BY-SA 4.0.

## License

Copyright (c) 2026 Tung Vu. Licensed under [CC BY-SA 4.0](LICENSE).
