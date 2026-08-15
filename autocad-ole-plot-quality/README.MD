# AutoCAD OLE Plot Quality Automation

A VBA macro for AutoCAD that changes the plot quality of OLE objects to monochrome across paper-space layouts.

## Problem

I frequently insert Excel OLE objects into multiple AutoCAD layouts. By default, these objects may use a complex plotting quality that makes them appear unnecessarily detailed when plotted.

Changing the OLE plot quality manually in every layout is repetitive and time-consuming.

## Solution

This macro iterates through the paper-space layouts of the current AutoCAD drawing and changes the `OlePlotQuality` property of OLE objects to `acOPQMonochrome`.

## Result

The change can be applied to all paper-space layouts at once instead of modifying each OLE object manually.

## Technology

- VBA
- AutoCAD COM/ActiveX API
- AutoCAD OLE objects

## Usage

1. Open the drawing in AutoCAD.
2. Load the VBA project containing the macro.
3. Run `ChangeOLEQualityToMonochrome`.
4. The macro processes OLE objects in the paper-space layouts.