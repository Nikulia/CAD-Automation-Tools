# AutoCAD Action Recorder Foreach

An AutoLISP utility for applying a recorded AutoCAD Action Recorder operation to all paper-space layouts in the active drawing.

### Why "AD_HOC"?

*Ad hoc* is a Latin expression meaning "for this specific purpose." 
In this project, `AD_HOC` refers to a recorded AutoCAD operation created for a particular task.

## Problem

When the same design modification needs to be made on multiple layouts, performing the operation manually on every layout is repetitive and time-consuming.

AutoCAD Action Recorder can record a sequence of operations and save it as an `.actm` file, but running the recorded action on every layout still requires repeating the command manually.

## Solution

This AutoLISP command, `AD_HOC_FOREACH`, automates the process:

1. Gets all layouts in the active drawing.
2. Skips Model Space.
3. Activates each paper-space layout.
4. Runs the recorded `AD_HOC` Action Recorder command.
5. Continues until all paper-space layouts have been processed.

This makes it possible to record an operation once and apply it consistently across all layouts.

## Workflow

```text
Record operation
      ↓
Save as AD_HOC.actm
      ↓
Run AD_HOC_FOREACH
      ↓
Apply AD_HOC to every paper-space layout