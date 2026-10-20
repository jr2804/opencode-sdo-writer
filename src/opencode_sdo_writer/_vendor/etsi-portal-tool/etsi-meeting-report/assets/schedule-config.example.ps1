# Schedule configuration for one meeting — copy to the meeting's scripts/ folder,
# rename to <tc><nn>-schedule.ps1 (e.g. <tc><nn>-schedule.ps1), fill in, then run:
#   powershell -ExecutionPolicy Bypass -File scripts/build-schedule.ps1 -Config scripts/<tc><nn>-schedule.ps1
#
# Everything meeting-specific is here. The builder never needs editing.
# Worked example with all rules applied: <tc><nn>-schedule.ps1 (same folder as this file).

$Meeting = @{
  Doc       = (Resolve-Path (Join-Path $PSScriptRoot '..\Report-Template.docx')).Path  # report/agenda .docx to update
  Manifest  = 'C:\Users\<you>\.cache\etsi-portal-tool\meetings\<start-date>-<MeetingID>\manifest.json'
  UidPrefix = '<TC>(26)<nnn>'    # TDoc UID = prefix + short number, e.g. '<TC>(26)<nnn>' + '008a1' = <UID>a1
  Heading   = 'Meeting schedule for <TC>#<nn>'   # heading that precedes the schedule (paraId may change; matched by text)
  Caption   = 'Schedule of <TC>#<nn> by time slot and topic'   # plain caption, NO table counter
  EndAnchor = 'IPR Statement'  # first paragraph after the schedule section; everything in between is regenerated
  # optional (defaults shown):
  # GreyPattern  = '^\(no meeting\)$|break$|^Social event'   # labels matching this are grey automatically
  # GreyFill     = '#999999'
  # LinkColor    = '#00008B'                                  # dark blue links, readable on all fills
  # LegendHeader = 'Legend'
}

# ---- topics: one entry per block of the same colour --------------------------
# fill: colour-blind safe (Okabe-Ito extended), never yellow, never a blue background
#       (blue is reserved for hyperlinks). text: black on light fills, white on dark fills.
# label: legend text. Name the real topic and list its document numbers at the end.
# Placeholder topics without a document get a distinct colour each.
$Topics = [ordered]@{
  admin    = @{ fill = '#D55E00'; text = '#000000'; label = 'Administration (opening, agenda, invitation, report, LS in) — #001, #002' }
  topicA   = @{ fill = '#E69F00'; text = '#000000'; label = '<topic A> — #005, #006' }
  topicB   = @{ fill = '#009E73'; text = '#000000'; label = '<topic B> — #009' }
  topicC   = @{ fill = '#D9C2E9'; text = '#000000'; label = '<topic C> — #008, #008a1, #010' }
  placeA   = @{ fill = '#882255'; text = '#FFFFFF'; label = '<topic D> — no document yet' }
  placeB   = @{ fill = '#56B4E9'; text = '#000000'; label = '<topic E> — no document yet' }
  plugtest = @{ fill = '#8C564B'; text = '#FFFFFF'; label = 'Topic F — no document yet' }
  mobile   = @{ fill = '#0072B2'; text = '#FFFFFF'; label = '<TC> Mobile report — no document number' }
}

# ---- grid rows: header first, one row per 30-minute slot, note row last ------
# Each row has exactly one entry per column (time, Monday, Tuesday, Wednesday).
# '' = unscheduled (white). Repeat no label inside a block: only the first slot carries the text.
$Slots = @(
  @('Time',  'Monday – 19th October', 'Tuesday – 20th October', 'Wednesday – 21st October'),
  @('09:00', '(no meeting)', '', ''),
  @('09:30', '(no meeting)', '', ''),
  @('10:00', '(no meeting)', '', ''),
  @('10:30', '(no meeting)', 'Coffee break', ''),
  @('11:00', '(no meeting)', '', ''),
  @('11:30', '(no meeting)', '', ''),
  @('12:00', '(no meeting)', '', ''),
  @('12:30', '(no meeting)', 'Lunch break', ''),
  @('13:00', 'Opening, Agenda', 'Lunch break', ''),
  @('13:30', '', '', ''),
  @('14:00', '', '', ''),
  @('14:30', '', '', ''),
  @('15:00', '', '', ''),
  @('15:30', 'Coffee break', 'Coffee break', 'Coffee break'),
  @('16:00', '', '', ''),
  @('16:30', '', '', ''),
  @('17:00', '(no meeting)', '(no meeting)', '(no meeting)'),
  @('17:30', '(no meeting)', '(no meeting)', '(no meeting)'),
  @('19:00', '(no meeting)', 'Social event / dinner', '(no meeting)'),
  @('White cells = unscheduled. Grey cells = breaks, outside meeting hours, or the social event.', '', '', '')
)

# ---- topic per cell: "row,col" (1-based; row 1 = header, col 1 = time) -------
$FillMap = [ordered]@{
  '2,2'  = 'admin'
  '2,3'  = 'topicA';  '3,3' = 'topicA'        # two slots of one block: both coloured, label once
  '4,3'  = 'topicB'
  '6,3'  = 'topicC';  '7,3' = 'topicC'
}

# ---- document cells: Keep = label stays in paragraph 1 and documents go below it
# Docs: short numbers; a document with a docbox_url in the manifest becomes a hyperlink,
# a reserved document (no payload) stays plain text.
$DocCells = [ordered]@{
  '2,3' = @{ Keep = $false; Docs = @('005', '006') }
  '4,3' = @{ Keep = $false; Docs = @('009') }
  '6,3' = @{ Keep = $false; Docs = @('008') }
}

# ---- merges: Row/Col 1-based. RowSpan/ColSpan default 1. ColSpan must end at the last column.
$Merges = @(
  @{ Row = 2;  Col = 2; RowSpan = 8 }                  # block of out-of-hours slots, Monday
  @{ Row = 5;  Col = 3; ColSpan = 2 }                  # break across Tue+Wed
  @{ Row = 15; Col = 2; ColSpan = 3 }                  # break across all days
  @{ Row = 21; Col = 1; ColSpan = 4 }                  # note row (last row of $Slots)
)
