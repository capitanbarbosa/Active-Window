; SetTitleMatchMode, 2

; Retrieve the command-line arguments
CommandLine := DllCall("GetCommandLine", "str")
argv := StrSplit(SubStr(CommandLine, InStr(CommandLine, A_Space) + 1), A_Space)

; Retrieve the index parameter from the command-line arguments
index := argv[1]

; Define a function to send the desired key combination
SendAltWinShiftFunctionKey(index) {
    ; Define the base key combination
    baseCombination := "^#!{" . index "}"

    ; Send the Alt+Tab key combination
    SendInput !{Tab}
    Sleep(400) ; Wait for 400 milliseconds (adjust if needed)

    ; Send the key combination
    SendInput %baseCombination%
}

; Call the function with the passed index parameter
SendAltWinShiftFunctionKey(index)
