# STQ#83 schedule configuration — meeting 84544, 19–21 Oct 2026, Example Systems, Aachen.
# Read by scripts/build-schedule.ps1:   powershell -File scripts/build-schedule.ps1 -Config scripts/stq83-schedule.ps1
# Edit the data below, rebuild, and update agenda-draft.md in the SAME commit.

$Meeting = @{
  Doc       = (Resolve-Path (Join-Path $PSScriptRoot '..\Report-Template.docx')).Path
  Manifest  = 'd:\UserData\.cache\etsi-portal-tool\meetings\2026-10-19-84544\manifest.json'
  UidPrefix = 'STQ(26)083'                       # TDoc UID = prefix + short number, e.g. 'STQ(26)083' + '008a1'
  Heading   = 'Meeting schedule for STQ#83'      # heading that precedes the schedule
  Caption   = 'Schedule of STQ#83 by time slot and topic'
  EndAnchor = 'IPR Statement'                    # first paragraph after the schedule section
}

# ---- topics: fill colour (colour-blind safe, no yellow), text colour, legend label ----
$Topics = [ordered]@{
  admin     = @{ fill = '#D55E00'; text = '#000000'; label = 'Administration (opening, agenda, invitation, report, LS in) — #001, #002, #003, #004, #007' }
  covis     = @{ fill = '#E69F00'; text = '#000000'; label = 'COVIS 1-1 validation framework (TS 104 273), TTF T054 progress report — #005, #006' }
  mmeasure  = @{ fill = '#009E73'; text = '#000000'; label = 'M-Measure framework (TS 104 234) — #009' }
  unified   = @{ fill = '#D9C2E9'; text = '#000000'; label = 'Unified test methods and requirements (EG 204 110) — #008, #008a1, #010' }
  immersive = @{ fill = '#882255'; text = '#FFFFFF'; label = 'Immersive audio reproduction (TS 104 650) — 3+ documents expected, numbers assigned on registration' }
  anc       = @{ fill = '#56B4E9'; text = '#000000'; label = 'ANC headset test methods (IEC 60268-24 / TS 103 640) — no document yet' }
  plugtest  = @{ fill = '#8C564B'; text = '#FFFFFF'; label = 'Bluetooth LE Audio plugtest — no document yet' }
  mobile    = @{ fill = '#0072B2'; text = '#FFFFFF'; label = 'STQ Mobile report — no document number' }
  other     = @{ fill = '#44AA99'; text = '#000000'; label = 'Other contributions (barriers to entry; listening effort) — #011, #012' }
}

# ---- grid: header row, one row per 30-minute slot, note row (last) ----------
# Empty string = unscheduled (white). Labels matching GreyPattern are grey automatically.
# A topic's label appears once; later slots of the same block stay empty (colour carries on).
$Slots = @(
  @('Time',  'Monday – 19th October', 'Tuesday – 20th October', 'Wednesday – 21st October'),
  @('09:00', '(no meeting)', '#005', 'Bluetooth LE Audio plugtest (follow-up)'),
  @('09:30', '(no meeting)', '#006', ''),
  @('10:00', '(no meeting)', '#009', ''),
  @('10:30', '(no meeting)', 'Coffee break', ''),
  @('11:00', '(no meeting)', '#008', 'STQ Mobile report'),
  @('11:30', '(no meeting)', '', ''),
  @('12:00', '(no meeting)', '', ''),
  @('12:30', '(no meeting)', 'Lunch break', ''),
  @('13:00', 'Opening, Agenda', 'Lunch break', ''),
  @('13:30', '#004', 'TS 104 650', ''),
  @('14:00', '#007', '', ''),
  @('14:30', '#008, #008a1', 'ANC headset test methods (IEC 60268-24)', ''),
  @('15:00', '#010', '#011', ''),
  @('15:30', 'Coffee break', 'Coffee break', 'Coffee break'),
  @('16:00', 'Bluetooth LE Audio plugtest', '#012', 'Report & Meeting close'),
  @('16:30', '', 'Immersive audio demo', ''),
  @('17:00', '(no meeting)', '(no meeting)', '(no meeting)'),
  @('17:30', '(no meeting)', '(no meeting)', '(no meeting)'),
  @('19:00', '(no meeting)', 'Social event / dinner', '(no meeting)'),
  @('White cells = unscheduled. Grey cells = breaks, outside meeting hours, or the social event.', '', '', '')
)

# ---- topic per cell: "row,col" (row 1 = header, col 1 = time) ---------------
$FillMap = [ordered]@{
  '2,3'  = 'covis';     '3,3'  = 'covis'                       # Tue 09:00 #005, 09:30 #006
  '4,3'  = 'mmeasure'                                          # Tue 10:00 #009
  '6,3'  = 'unified';   '7,3'  = 'unified'                     # Tue 11:00 #008 block
  '11,3' = 'immersive'; '12,3' = 'immersive'                   # Tue 13:30 TS 104 650 (1 h)
  '13,3' = 'anc'                                               # Tue 14:30 ANC reply
  '14,3' = 'other';     '16,3' = 'other'                       # Tue 15:00 #011, 16:00 #012
  '17,3' = 'immersive'                                         # Tue 16:30 immersive demo
  '2,4'  = 'plugtest';  '3,4'  = 'plugtest'                    # Wed 09:00-09:30 plugtest follow-up
  '6,4'  = 'mobile'                                            # Wed 11:00 STQ Mobile report
  '16,4' = 'admin';     '17,4' = 'admin'                       # Wed 16:00-17:00 report and close
  '10,2' = 'admin';     '11,2' = 'admin';  '12,2' = 'admin'    # Mon 13:00 opening, 13:30 #004, 14:00 #007
  '13,2' = 'unified';   '14,2' = 'unified'                     # Mon 14:30 #008/#008a1, 15:00 #010
  '16,2' = 'plugtest';  '17,2' = 'plugtest'                    # Mon 16:00-17:00 plugtest
}

# ---- document cells: Keep = seed label stays (paragraph 1), documents go below it
$DocCells = [ordered]@{
  '10,2' = @{ Keep = $true;  Docs = @('001', '002') }
  '11,2' = @{ Keep = $false; Docs = @('004') }
  '12,2' = @{ Keep = $false; Docs = @('007') }
  '13,2' = @{ Keep = $false; Docs = @('008', '008a1') }
  '14,2' = @{ Keep = $false; Docs = @('010') }
  '2,3'  = @{ Keep = $false; Docs = @('005') }
  '3,3'  = @{ Keep = $false; Docs = @('006') }
  '4,3'  = @{ Keep = $false; Docs = @('009') }
  '6,3'  = @{ Keep = $false; Docs = @('008') }
  '16,4' = @{ Keep = $true;  Docs = @('003') }
}

# ---- merges: Row/Col 1-based; RowSpan/ColSpan default 1; ColSpan must end at the last column
$Merges = @(
  @{ Row = 2;  Col = 2; RowSpan = 8 }                 # Mon 09:00-12:30 no meeting
  @{ Row = 18; Col = 2; RowSpan = 3 }                 # Mon 17:00-19:30 no meeting
  @{ Row = 18; Col = 3; RowSpan = 2 }                 # Tue 17:00-18:00 no meeting
  @{ Row = 18; Col = 4; RowSpan = 3 }                 # Wed 17:00-19:30 no meeting
  @{ Row = 5;  Col = 3; ColSpan = 2 }                 # Tue+Wed coffee 10:30
  @{ Row = 9;  Col = 3; RowSpan = 2; ColSpan = 2 }    # Tue+Wed lunch 12:30-13:30
  @{ Row = 15; Col = 2; ColSpan = 3 }                 # all days coffee 15:30
  @{ Row = 21; Col = 1; ColSpan = 4 }                 # note row
)
