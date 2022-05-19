package main

import (
    "fmt"
    "strings"
)

func charCodeAt(st string, ni int) rune {
    for i, j := range st {
        if i == ni {
            return j
        }
    }
    return 0
}

func hexify(st string) string {
    var ok string = ""
    ltr := []string{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"}

    for cnt := 0; cnt < len(st); cnt++ {
        ok += ltr[charCodeAt(st, cnt)>>4] + ltr[charCodeAt(st, cnt)&15]
    }

    return ok
}

func encrypt(st string) string {

    var initialize int = 0
    var ot string = ""
    var val int

    for i := 0; i < len(st); i++ {
        val = int(charCodeAt(st, i))
        initialize ^= (val << 2) ^ val
        ot += string(initialize & 0xff)
        initialize >>= 8
    }

    return strings.Replace(hexify(ot), "00", "", -1)
}

func main() {
    fmt.Println(encrypt("[REDACTED FLAG]"))
}

//Hash: eae4a5b1aad7964ec9f1f0bff0229cf1a11b22b11bfefecc9922aaf4bff0dd3c88

