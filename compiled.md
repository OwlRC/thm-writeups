# ⚙️ Compiled

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Compiled](https://tryhackme.com/room/compiled) |
| **Difficulty** | 🟢 Easy |
| **Category** | Reverse Engineering |
| **Tools** | Ghidra, strings, file, chmod |

---

## 🎯 Objective

A compiled binary is provided — reverse engineer it to find the correct password and capture the flag.

---

## 🔍 Initial Analysis

Download the task file. Check what kind of file it is:

```bash
file Compiled.Compiled
# ELF 64-bit LSB executable, x86-64
```

Give it execute permissions and run it:

```bash
chmod +x Compiled.Compiled
./Compiled.Compiled
# Password: test
# Try again!
```

It asks for a password. Try extracting strings first:

```bash
strings Compiled.Compiled
```

An interesting format string appears: `DoYouEven%sCTF`

---

## 🔬 Reverse Engineering with Ghidra

Load the binary into Ghidra → Analyse → open the `main` function in the Decompiler view:

```c
undefined8 main(void) {
    int iVar1;
    char local_28 [32];
    
    fwrite("Password: ", 1, 10, stdout);
    __isoc99_scanf("DoYouEven%sCTF", local_28);
    
    iVar1 = strcmp(local_28, "__dso_handle");
    if ((-1 < iVar1) && (iVar1 = strcmp(local_28, "__dso_handle"), iVar1 < 1)) {
        printf("Try again!");
        return 0;
    }
    iVar1 = strcmp(local_28, "_init");
    if (iVar1 == 0) {
        printf("Correct!");
    } else {
        printf("Try again!");
    }
    return 0;
}
```

---

## 💥 Solution

The `scanf` format string is `DoYouEven%sCTF` — meaning whatever we type gets inserted into `DoYouEven___CTF`. The binary then checks if `local_28` equals `_init`.

So the full input needed is:
```
DoYouEven_init
```

```bash
./Compiled.Compiled
# Password: DoYouEven_init
# Correct! Enjoy Decompiling! (--;)
```

---

## 📚 Lessons Learned

- `strings` is always the first step on an unknown binary — reveals format strings, hardcoded values, and hints
- Ghidra decompiles machine code back into readable C — essential for reverse engineering
- Custom `scanf` format strings can act as implicit password prefixes/suffixes
- Always check `file` before executing an unknown binary

---
*by OwlRC 🦉 | github.com/OwlRC*
