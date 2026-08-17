# CAD Automation Tools

A collection of practical automation tools developed to improve repetitive tasks in technical drafting and CAD workflows.

These tools were created to solve real problems encountered during day-to-day work with AutoCAD, technical documentation, and project files.

## What is this repository about?

As a technical drafting specialist, I often encounter repetitive operations that are simple but time-consuming when performed manually.

Instead of repeating the same operations, I experiment with automation using AutoCAD's built-in tools, VBA, AutoLISP and PowerShell.

The goal is not to automate everything, but to identify repetitive tasks where a small script can save time, reduce manual errors, or make a workflow more consistent.

## Tools and technologies

- AutoCAD
- VBA
- AutoLISP
- PowerShell
- Excel
- Regular expressions

## Projects

### AutoCAD Automation

#### Action Recorder Foreach

An AutoLISP utility that applies a recorded AutoCAD Action Recorder operation to every paper-space layout in the active drawing.

Useful when the same sequence of editing operations needs to be performed across multiple layouts.

#### Change OLE Quality to Monochrome

A VBA macro that changes the plot quality of OLE objects imported from Excel to monochrome across paper-space layouts.

This avoids manually changing the OLE plot quality on each layout.

### PowerShell File Management

#### PowerShell-File-Management-Tools

A collection of PowerShell scripts created to automate repetitive file-management tasks, including:

- Recursive filename transformations
- Sequential PDF renaming
- DWG filename shortening
- Finding files with the same name but different sizes

These scripts were developed for practical document-management problems encountered in technical drafting workflows.

## Why I created these tools

Many of the tasks that inspired these scripts are not technically difficult. The problem is that they may need to be repeated many times.

For example:

- Renaming 15 files manually can take around 20–30 minutes and introduce mistakes.
- Applying the same AutoCAD operation to many layouts can require repetitive manual work.
- Large sets of architectural drawings may contain multiple versions without clear revision information.
- Long DWG filenames can prevent drawings from being opened.

Small automation tools can turn these repetitive tasks into quick and repeatable operations.

## Background

These tools are based on problems encountered during my work as an AutoCAD / technical drafting specialist.

My professional background includes 8+ years of experience in technical drafting and documentation, with a growing focus on CAD automation and workflow improvement.

I am currently developing my skills in AutoLISP, PowerShell and programming while building practical automation tools around real-world CAD workflows.

## Status

This repository is an ongoing collection of experiments and practical utilities.

Some tools are highly specific to the workflows that originally motivated them, while others can be adapted to similar tasks in different projects.

More tools will be added as I continue exploring CAD and workflow automation.
