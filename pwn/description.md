Zawartość pliku `flag.txt` w katalogu bieżącym serwera: BSK{s1mpl3-r0p-1s-5imp1e}

Zacząłem od sprawdzenia włączanych zabezpieczeń pliku binarnego programu za pomocą polecenia `checksec` w `pwndbg`: 

    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

z czego wywnioskowałem, że sensownym pomysłem byłoby skorzystanie z ROPGadgetoów.

Widać, że operacja `APPEND_T` jest wadliwym miejscem programu i można to wykorzystać do przepełnienia bufora robiąc pełny `READ_T` i po nim `APPEND_T`.

Zauważyłem, że w programie po odczycie danych jest wykonywana funkcja `memfrob` na otrzymanym obiekcie, więc przed wysyłaniem danych do programu wykonuje analogiczną funkcję, ponieważ xor jest grupą 2-elementową. 

Wyłapywanie kanarka wygląda standardowo - jak na zajęciach. Z wyłączonym ASLRem i swoim libcu napisałem wywołanie shella ze stałym adresem. Po znalezieniu offseta pomiędzy kanarkiem a ROPgadgetami udało się uruchomić shella lokalnie.

Za pomocą adresu `__libc_start_main + offset` na stosie udało się wyciągnąć adres libca i zatem włączyć lokalnie ASLR. Została tylko zamiana offsetów libca, które dostałem poniższymi komandami:

```
readelf -Ws libc.so.6 | grep "system@@" && \
readelf -Ws libc.so.6 | grep "__libc_start_main@@" && \
strings -tx libc.so.6 | grep "bin/sh" && \
ROPgadget --binary libc.so.6 | grep "pop rdi ; ret"
```

Powstały po drodze skrypt w pythone jest w pliku `exploit`