#include <iostream>
#include <Windows.h>

BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam)
{
    int titleLength = GetWindowTextLengthA(hwnd);
    if (titleLength == 0)
    {
        return TRUE;
    }

    std::string windowTitle(titleLength + 1, '\0');
    int result = GetWindowTextA(hwnd, &windowTitle[0], titleLength + 1);
    if (result == 0)
    {
        std::cerr << "Failed to retrieve window title for hwnd: " << hwnd << std::endl;
        return TRUE;
    }

    if (windowTitle.find("Desktop") != std::string::npos)
    {
        std::cout << windowTitle << std::endl;
    }

    return TRUE;
}

int main()
{
    EnumWindows(EnumWindowsProc, 0);
    return 0;
}
